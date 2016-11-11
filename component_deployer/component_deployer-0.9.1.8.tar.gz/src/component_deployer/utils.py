import yaml


def parse_versions(stream, release):
    f = yaml.load(stream)
    versions = {}
    for item in f['items']:

        if item['kind'] != 'Deployment':
            continue
        if release not in item['metadata']['name']:
            continue

        containers = item['spec']['template']['spec']['containers']
        if not isinstance(containers, list):
            containers = [containers]

        for container in containers:
            image, tag = container['image'].split(':')
            versions[image] = tag

    return versions
