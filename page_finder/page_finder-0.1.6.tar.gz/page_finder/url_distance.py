from six.moves.urllib_parse import urlparse, unquote, parse_qs

def levenshtein_array(s1, s2):
    """
    Levenstein distance where insertion and deletions cost double as substitutions
    """
    if len(s1) < len(s2):
        return levenshtein_array(s2, s1)

    if len(s2) == 0:
        return len(s1) * 2

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # j+1 instead of j since previous_row and current_row are one character longer
            insertions = previous_row[j + 1] + 2
            deletions = current_row[j] + 2       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def dict_distance(prep, dict1, dict2):
    distance = 0
    checkedkeys = 0
    for k in dict1:
        if k in dict2:
            checkedkeys += 1
            distance += sorted(map(prep, dict1[k])) != sorted(map(prep, dict2[k]))
        else:
            distance += 1

    return distance + len(dict2) - checkedkeys

def url_distance(preprocessor, url1, url2):
    url1 = urlparse(url1)
    url2 = urlparse(url2)

    process_fn = lambda s: preprocessor(unquote(s))
    path1 = map(process_fn, url1.path.strip('/').split('/'))
    path2 = map(process_fn, url2.path.strip('/').split('/'))
    path_distance = levenshtein_array(path1, path2)

    query_distance = dict_distance(preprocessor,
        parse_qs(url1.query, True),
        parse_qs(url2.query, True)
    )

    domain_distance = 4 * levenshtein_array(
        (url1.hostname or '').split('.'),
        (url2.hostname or '').split('.')
    )

    return (
        domain_distance +
        path_distance +
        query_distance +
        (url1.fragment != url2.fragment)
    )

