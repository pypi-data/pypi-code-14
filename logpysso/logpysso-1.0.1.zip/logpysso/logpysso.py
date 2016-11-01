'''
Created on 2016. 8. 4.

Logpresso Python Client

@author: hando.kim
'''
__all__ = ['os', 'jpype', 'pandas']

import os
import jpype
import pandas as pd


api_server = ""
api_port = ""
api_key = ""


def connect(addr, port, user, password):
    jarpath = os.path.join(os.path.abspath(".\\"), "araqne-logdb-client-1.0.5-package.jar")
    jpype.startJVM(jpype.getDefaultJVMPath(), '-Djava.class.path=%s' % jarpath)
    logpressoPkg = jpype.JPackage("org").araqne.logdb.client
    client = logpressoPkg.LogDbClient()
    client.connect(addr, port, user, password)
    assert isinstance(client, object)
    return client


def connect2(addr, port, apikey):
    # apikey = "2ff257d0-7821-5f7c-5391-cdb6dfc5a1ca"
    # sample qry = http://hostname:port/logpresso/httpexport/query?_apikey=sample-apikey&_q=logdb+tables
    global api_server
    global api_port
    global api_key
    api_server = addr
    api_port = port
    api_key = apikey
    return "Get logpresso connect infomation!"


def query(client, qry):
    qid = client.createQuery(qry)
    client.startQuery(qid)
    rows = client.getResult(qid, 0, 2147483647)
    fields = []
    data_row = []
    try :
        for f in rows.get("field_order") :
            fields.append(f)
    except TypeError as e:
        print(e)

    for row in rows.get("result") :
        if len(fields) == 0 :
            for i in row :
                fields.append(i)

        tmp_dict = {}
        for cell in fields :
            tmp_dict[cell] = row.get(cell)
        data_row.append(tmp_dict)

    cursor = pd.DataFrame(data_row)
    client.stopQuery(qid)
    return cursor


# def api_query(qry):
#    url = "http://"+api_server+":"+api_port+"/logpresso/httpexport/query.csv?_apikey="+ api_key + "&_q="+ qry


def close(client):
    client.close()
    jpype.shutdownJVM()


#if __name__ == '__main__':
#    client = connect("106.248.68.179", 8888, "root", "!1jadncJADNC")
#    cursor = query(client,"table Meta_Industry 	| fields code, industry")
#    print(cursor)
#    close(client)
