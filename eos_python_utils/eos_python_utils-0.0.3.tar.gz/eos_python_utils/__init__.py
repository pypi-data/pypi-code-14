#!user/bin/env python3
def get_params(route_map, request_path):
    routes = list(route_map.keys())
    for route in routes:
        params = match_route(route, request_path)
        if params != None:
            return { 'params': params, 'path': route }
    return None

def match_route(route, request_path):
    params = {}
    route_list = remove_whitespace(route.split('/'))
    request_list = remove_whitespace(request_path.split('/'))
    if len(route_list) != len(request_list):
        return None
    for idx, name in enumerate(route_list):
        if name[0] == '{' and name[-1] == '}':
            params[name[1:-1]] = request_list[idx]
        elif name != request_list[idx]:
            return None
    return params

def remove_whitespace(path):
    start = 1 if path[0] == '' else None
    end = -1 if path[-1] == '' else None
    return path[start:end]
