import papi.fp as fp

def join_path(path):
    return '/' + '/'.join(fp.flatten(path))

def hateoas(path, item, page=None):
    if item == '':
        item = {'_value': item}
    try:
        item = dict(item)
    except TypeError:
        item = {'_value': item}
    except ValueError:
        item = {'_value': item}
    return fp.assocs([
        ('_self', { 'href': join_path(path) }),
        ('_parent', { 'href': join_path(fp.drop_end(1, path)) })
    ], item)
