from json import dumps, loads


def main():
    pass


def tri(val, last):
    if len(val) == 3:
        return val
    return tuple(val) + (last,)


def coordinate(val, refs):
    """
    val = (start, end, step)
    refs = (start, end, step)
    """
    (start, end, step) = tri(val, 1)
    value_count = (end - start) // step

    (r_start, r_end, r_dir) = tri(refs, 1)
    r_step = (r_end - r_start) // value_count
    if value_count == 1:
        return tuple()

    ret = []
    for i in range(value_count):
        a = r_start + r_step * i
        b = a + r_step
        c = start + step * i
        ret.append((a, b, c))
    ret[0] = (None, ret[0][1], ret[0][2])
    ret[-1] = (ret[-1][0], None, ret[-1][2])
    return tuple(ret)


def scale(css):
    defs = loads(css[css.find('/*') + 2: css.find('*/')])
    media_queries = []
    for def_ in defs:
        css = []
        for coord in coordinate(def_['value'], def_['width']):
            min_width, max_width, value = coord
            conditions = []
            if min_width is not None:
                conditions.append("(min-width: {min_width}px)".format(min_width=min_width))
            if max_width is not None:
                conditions.append("(max-width: {max_width}px)".format(max_width=max_width - 1))
            css.append(" ".join(["@media", " and ".join(conditions), "{"]))
            css.append("    " + def_["css"] % dict(value=value))
            css.append("}")
        if css:
            media_queries.append("\n".join(css))

    defs_json = dumps(defs, indent=4, sort_keys=True)
    return "\n\n".join(["/*\n{defs}\n*/".format(defs=defs_json)] + media_queries) + "\n"
