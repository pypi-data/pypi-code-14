def determine_url(host, project):
    """
    Determine the URL to use when connecting to a host.

    :param host: Full host name.
    :param project: Project name.
    :return: String with the URL to use.
    """
    host = host if host is None else host.strip()
    if host is not None and len(host) > 0:
        return host
    project = project if project is None else project.strip()
    if project is not None and len(project) > 0:
        return 'https://' + project + '.citrination.com'
    return 'https://citrination.com'
