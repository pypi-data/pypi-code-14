import requests


def get_events(url='', bucket='', start_date='', end_date='', filter='', timeout=60):
    return requests.get(
        url + "/events/?bucket=%s&start=%s&end=%s&filter=%s" % (bucket, start_date, end_date, filter),
        headers={"Accept": "application/json"},
        timeout=timeout
    ).json()