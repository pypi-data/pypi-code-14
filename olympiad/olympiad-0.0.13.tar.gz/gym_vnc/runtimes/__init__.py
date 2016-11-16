import os
import sys
import yaml

from gym_vnc.runtimes.registration import register_runtime

with open(os.path.join(os.path.dirname(__file__), '../../runtimes.yml')) as f:
    spec = yaml.load(f)

register_runtime(
    id='vnc-core-envs',
    kind='docker',
    image='docker.openai.com/vnc-core-envs:{}'.format(spec['vnc-core-envs']['tag']),
)

host_config = {
    'cap_add': ['NET_ADMIN'],
    'ipc_mode': 'host'
}

# TODO: may need --privileged for docker-machine on mac
if sys.platform.startswith("darwin"):
    host_config['cap_add'].append('SYS_ADMIN')

register_runtime(
    id='vnc-flashgames',
    kind='docker',
    image='docker.openai.com/vnc-flashgames:{}'.format(spec['vnc-flashgames']['tag']),
    host_config=host_config,
    environment=['OPENAI_LIVESTREAM_URL'],
    server_registry_file=os.path.join(os.path.dirname(__file__), 'vnc-flashgames.json'),
)

register_runtime(
    id='vnc-world-of-bits',
    kind='docker',
    image='docker.openai.com/vnc-world-of-bits:{}'.format(spec['vnc-world-of-bits']['tag']),
    host_config={
        'cap_add': ['NET_ADMIN', 'SYS_ADMIN'],
        'ipc_mode': 'host'
    })

register_runtime(
    id='vnc-minecraft',
    kind='docker',
    image='docker.openai.com/tambet/malmo:{}'.format(spec['vnc-minecraft']['tag']),
    host_config={
        'cap_add': ['NET_ADMIN', 'SYS_ADMIN'],
        'ipc_mode': 'host'
    })

register_runtime(
    id='vnc-windows',
    kind='windows',
)

register_runtime(
    id='vnc-starcraft',
    kind='docker',
    image='docker.openai.com/vnc-starcraft:{}'.format(spec['vnc-starcraft']['tag']),
    host_config={
        'cap_add': ['NET_ADMIN'],
    },
    environment=['OPENAI_LIVESTREAM_URL'],
)

del spec
