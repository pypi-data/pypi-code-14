from collections import OrderedDict

def _fetch_all_group_values(olist, group_name):
    values = set()
    for o in olist:
        values.add(getattr(o, group_name))
    return list(values)

def group_by(olist, group_names, sort_key=None):
    """Groups list elements."""
    if not isinstance(group_names, list):
        group_names = [group_names]

    if len(group_names) == 0:
        return olist

    group_name = group_names[0]
    vals = _fetch_all_group_values(olist, group_name)
    vals.sort(key=sort_key)
    grouped = OrderedDict([(v, []) for v in vals])

    for o in olist:
        v = getattr(o, group_name)
        grouped[v].append(o)

    for (k, tl) in grouped.iteritems():
        grouped[k] = group_by(tl, group_names[1:])

    return grouped

def traverse_dict(d, visit_func, opt=None):
    """Recursively visits each dict value."""
    opts = visit_func(d, opt)
    if isinstance(d, dict):
        i = 0
        for v in d.itervalues():
            traverse_dict(v, visit_func, opts[i] if opts else None)
            i += 1
