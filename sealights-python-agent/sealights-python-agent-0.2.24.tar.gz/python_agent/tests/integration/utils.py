from python_agent.packages import requests
from python_agent.packages import semantic_version


def bump_version(old_version, default=None):
    default = default or str(semantic_version.Version("1", partial=True))
    try:
        version = semantic_version.Version(old_version, partial=True)
    except:
        version = semantic_version.Version("0", partial=True)

    try:
        next_build = version.next_patch()
        return str(next_build)
    except:
        pass

    try:
        next_build = version.next_minor()
        return str(next_build)
    except:
        pass

    try:
        next_build = version.next_major()
        return str(next_build)
    except:
        return default


def get_next_build_number(customer_id, app_name, server):
    default_next_build = str(semantic_version.Version("1", partial=True))
    url = server + "/v1/dashboard/builds"
    params = {
        "customerId": customer_id,
        "apps": app_name,
        "buildsPerComponent": "latest"
    }
    response = requests.get(url, params=params)
    if not response.ok:
        print "Failed Getting Build From Server. Using Default Next Build: %s. Error: %s" % (params, default_next_build)
        return default_next_build

    builds = response.json().get("data")
    if not builds:
        return default_next_build
    build_num = builds[0].get("component", {}).get("name")
    return bump_version(build_num, default=default_next_build)


def get_build(customer_id, app_name, server):
    url = server + "/v1/dashboard/builds"
    params = {
        "customerId": customer_id,
        "apps": app_name,
        "buildsPerComponent": "latest",
        "fields": "environments,environment_Coverage,environment_QualityHoles,environment_TestCount,build_Coverage"
    }

    response = requests.get(url, params=params)
    if not response.ok:
        print "Failed Getting Build From Server. URL: %s. Params: %s. Error: %s" % (url, params, response.content)
        return {}
    builds = response.json().get("data")
    if not builds:
        return {}
    return builds[0]