# coding=utf8
import copy
import json
import sys

if sys.version < "3":
    from urllib import urlencode
    import urllib2 as http
else:
    from urllib.parse import urlencode
    from urllib import request as http

import pandas

from csf import config


def chk_type(obj, typlst):
    if sys.version < "3" and str in typlst:
        typlst.append(unicode)
    return isinstance(obj, tuple(typlst))


def url_get(path, params=None, method="GET"):
    params = params if params else {}

    header = {
        "access_key": config.token.access_key,
        "t": config.token.time,
        "token": config.token.token,
    }

    _params = {}
    for name, obj in params.items():
        if obj not in [None, ""]:
            _params[name] = obj
    params = _params

    path = "/datasupply" + path[4:] if config.debug else path
    __base_url = config.DEBUG_BASE_URL if config.debug else config.BASE_URL

    if method == "GET":
        url = "%s%s?%s" % (__base_url, path, urlencode(params))
        req = http.Request(url, headers=header)
    else:
        data = params
        url = "%s%s" % (__base_url, path)

        if sys.version > "3":
            req = http.Request(url, headers=header, data=bytes(urlencode(data), encoding=config.ENCODING))
        else:
            req = http.Request(url, headers=header, data=urlencode(data))
        req.add_header("Content-Type", "application/x-www-form-urlencoded")

    if config.debug:
        print(url)

    data = http.urlopen(req).read()
    try:
        if isinstance(data, bytes):
            result = json.loads(data.decode(config.ENCODING))
        else:
            result = json.loads(data)

        if result["type"] != "SUCCESS":
            raise RuntimeError(result["type"])

        return result["message"]
    except RuntimeError as e:
        raise e
    except Exception:
        raise RuntimeError("RUNTIME_EXCEPTION")


def return_format(df, ret_fields, field=None, renames=None, index=None):
    rdf = df.rename(columns=renames) if renames else df

    if df.empty:
        return df

    if index and field and index in field:
        field.remove(index)

    rdf = rdf.drop_duplicates().reset_index(drop=True)
    rdf = rdf.ix[:, ret_fields]
    if index:
        rdf = rdf.set_index(index)
        try:
            rdf.index = pandas.DatetimeIndex(rdf.index)
            rdf = rdf.sort_index()
        except:
            pass

    rdf = rdf.ix[:, field] if field else rdf
    return rdf


def format_param(name, values):
    if values == None:
        return values

    if not isinstance(values, (list, tuple, set)):
        values = [values]

    def format_code(name, value):
        if len(value) >= 6 and value[-6:] in ["_SH_EQ", "_SZ_EQ"]:
            return value

        return value + "_SH_EQ" if value[:2] == "60" else value + "_SZ_EQ"

    result = []
    for value in values:
        if name in ["codes", "code"]:
            result.append(format_code(name, value))
        else:
            result.append(str(value))
    return ",".join(result)


def get_dataframe(
        path,
        params,
        method="GET",
):
    params["version"] = config.version
    json_objs = url_get(path, params, method=method)
    json_objs = format_json_obj(json_objs)
    dfs = pandas.DataFrame(json_objs)
    if dfs.empty:
        pass  # raise EmptyException
    return dfs


def format_json_obj(jobj, pobj=None, names=None, _results=None):
    results = _results if _results != None else list()
    pobj = pobj if pobj else dict()

    if not names: names = []

    def check_raw_dict_and_format(_dict):
        is_raw = True
        for name, obj in _dict.items():
            if obj in [{}, []]:
                _dict[name] = None
                continue
            if not isinstance(obj, (list, dict)):
                continue
            is_raw = False

        return is_raw

    def process_raw_obj(jobj, pobj, names, results):
        if isinstance(jobj, dict):
            for name, obj in jobj.items():
                pobj["_".join(names + [name])] = obj
        else:
            pobj["_".join(names)] = jobj

        if check_raw_dict_and_format(pobj):
            results.append(pobj.copy())
        else:
            format_json_obj(pobj, _results=results)

    if jobj and isinstance(jobj, dict):
        r_jobj = dict()
        _jobj = dict()

        for sname, sobj in jobj.items():
            if isinstance(sobj, (dict, list)):
                _jobj[sname] = sobj
                continue
            if sobj in [[], {}]:
                r_jobj["_".join(names + [sname])] = None
                continue

            r_jobj["_".join(names + [sname])] = sobj

        for sname, sobj in _jobj.items():
            cobj = copy.deepcopy(pobj) if pobj else copy.deepcopy(jobj)
            cobj.update(r_jobj)
            p_cobj = cobj
            for name in names:
                if p_cobj.__contains__(name):
                    p_cobj = p_cobj[name]
            if p_cobj.__contains__(sname):
                p_cobj.pop(sname)

            format_json_obj(sobj, cobj, names + [sname], _results=results)

        if not _jobj:
            process_raw_obj(jobj, pobj, names, results)


    elif jobj and isinstance(jobj, list):
        for obj in jobj:
            if len(jobj) > 1:
                cobj = copy.deepcopy(pobj) if pobj else None
            else:
                cobj = pobj
            if names:
                cobj["_".join(names)] = obj
            format_json_obj(obj, cobj, names, _results=results)

    else:
        process_raw_obj(jobj, pobj, names, results)

    if _results == None:
        return results
