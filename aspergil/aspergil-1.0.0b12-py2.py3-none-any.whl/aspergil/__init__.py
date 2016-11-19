from __future__ import print_function

import re
import os 
import sys
import jinja2
import shutil

from datetime import datetime as dt
from functools import partial, reduce


def backup_file_name(file):
    basename = os.path.basename(file)
    dirname = os.path.dirname(file)
    return os.path.abspath(os.path.join(dirname, \
        "{0}.bck_{1}".format(basename, re.sub(r'[^0-9T]', \
            '', dt.now().isoformat()))))


def load_template(elem):
    with open(elem['template_path'], 'rb') as fd:
        template_text = fd.read().decode()
        elem['template'] = jinja2.Template(template_text)
    return elem


def get_template_path(templates_dir, elem):
    path = os.path.join(templates_dir, elem['template_name'])
    elem['template_path'] = path
    return elem


def backup_target(elem):
    target_file = elem['target_file']
    if os.path.exists(target_file):
        shutil.move(target_file, backup_file_name(target_file))
        elem['backup_status'] = 'ok'
    else:
        elem['backup_status'] = 'skipped'
    return elem


def get_context(vm_name, address_offset=2):
    ip_address_eth0 = '10.0.2.{}'.format(address_offset)
    ip_address_eth1 = '192.168.56.{}'.format(address_offset)
    return {
        'adapters': [
            {
                'name': 'eth0',
                'address': ip_address_eth0,
                'broadcast': '10.0.2.255',
                'netmask': '255.255.255.0',
                'gateway': '10.0.2.1',
                'dns_nameservers': '10.0.2.1',
            },
            {
                'name': 'eth1',
                'address': ip_address_eth1,
                'broadcast': '192.168.56.255',
                'netmask': '255.255.255.0',
                # it seems /etc/network/interfaces can't have more than one 'gateway' - tbc                                             
                # (see http://raspberrypi.stackexchange.com/questions/13895/solving-rtnetlink-answers-file-exists-when-running-ifup)
                # 'gateway': '192.168.56.1',
                'dns_nameservers': '192.168.56.1',
            },
        ],
        'ip_address_eth0': ip_address_eth0,
        'ip_address_eth1': ip_address_eth1,
        'vm_name': vm_name
    }


def prepare_directory(target_file):
    parent_dir = os.path.abspath(os.path.dirname(target_file))
    # print("parent_dir = {}".format(parent_dir))
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)


def render_template(context, elem):
    prepare_directory(elem['target_file'])
    with open(elem['target_file'], 'w') as fd: 
        fd.write(elem['template'].render(context))
        fd.write(os.linesep)
    elem['render_status'] = 'ok'
    return elem


def check_results(acc, elem):
    return elem['render_status'] if elem['render_status'] != 'ok' else acc


def abort(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


def main():

    if len(sys.argv) < 3: 
        abort("invalid arguments")
    
    vm_name=sys.argv[1]
    address_offset=sys.argv[2]

    if not address_offset.isdigit(): 
        abort("invalid address_offset")

    prefix = ''
    
    if len(sys.argv) >= 4:
         prefix = os.path.abspath(sys.argv[2]).rstrip()

    base_dir = os.path.abspath(os.path.dirname(__file__))

    templates = [
        {
            'template_name': 'hosts.template', 
            'target_file': '{0}/etc/hosts'.format(prefix)
        },
        {
            'template_name': 'hostname.template', 
            'target_file': '{0}/etc/hostname'.format(prefix)
        },
        {
            'template_name': 'interfaces.template', 
            'target_file': '{0}/etc/network/interfaces'.format(prefix)
        },
    ]

    templates_dir = os.path.join(base_dir, 'templates')

    context = get_context(vm_name, address_offset=address_offset)

    # import pdb; pdb.set_trace()

    job = map(partial(get_template_path, templates_dir), templates)
    job = map(load_template, job)
    job = map(backup_target, job)
    job = map(partial(render_template, context), job)

    rc = reduce(check_results, job, 'ok')

    print('job completed (rc={0})'.format(repr(rc)))


if __name__ == '__main__':
    main()
