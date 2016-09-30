#!/usr/bin/env python
# Licensed to the Brocade, Inc. ('Brocade') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os.path

from setuptools import setup, find_packages
from dist_utils import fetch_requirements
from dist_utils import apply_vagrant_workaround

PROJECT = 'bwc-cli'

# Change docs/sphinx/conf.py too!
# requirements.txt path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REQUIREMENTS_FILE = os.path.join(BASE_DIR, 'requirements.txt')

install_reqs, dep_links = fetch_requirements(REQUIREMENTS_FILE)


def get_version_string():
    version = None
    sys.path.insert(0, BASE_DIR)
    from bwc_cli import __version__
    version = __version__
    sys.path.pop(0)
    return version


apply_vagrant_workaround()
setup(
    name=PROJECT,
    version=get_version_string(),
    description='Brocade Workflow Composer CLI',
    author='Brocade',
    author_email='support@brocade.com',
    url='https://github.com/StackStorm/bwc-cli',
    keywords = ['workflow', 'composer', 'cli', 'stackstorm'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],

    scripts=[],
    provides=[],
    install_requires=install_reqs,
    dependency_links=dep_links,
    namespace_packages=[],
    packages=find_packages(exclude=['setuptools', 'tests']),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'bwc = bwc_cli.shell:main'
        ],

        'bwc.ipf': [
            'ipf_show_config_bgp = bwc_cli.ipf.show:ShowConfigBGP',
            'ipf_show_topology = bwc_cli.ipf.show:ShowTopology',

            'ipf_inventory_register = bwc_cli.ipf.inventory:InventoryAdd',
            'ipf_inventory_delete = bwc_cli.ipf.inventory:InventoryDelete',
            'ipf_inventory_list = bwc_cli.ipf.inventory:InventoryList',
            'ipf_inventory_update = bwc_cli.ipf.inventory:InventoryUpdate',
            'ipf_inventory_show_lldp = bwc_cli.ipf.inventory:InventoryShowLLDP',
            'ipf_inventory_show_vcs_links = bwc_cli.ipf.inventory:InventoryShowVcs',

            'ipf_fabric_add = bwc_cli.ipf.fabric:FabricAdd',
            'ipf_fabric_delete = bwc_cli.ipf.fabric:FabricDelete',
            'ipf_fabric_list = bwc_cli.ipf.fabric:FabricList',
            'ipf_fabric_config_show = bwc_cli.ipf.fabric:FabricConfigShow',
            'ipf_fabric_config_set = bwc_cli.ipf.fabric:FabricConfigSet',
            # Note: Add has been deprecated and is here for backward compatibility reasons
            'ipf_fabric_config_add = bwc_cli.ipf.fabric:FabricConfigSet',
            'ipf_fabric_config_delete = bwc_cli.ipf.fabric:FabricConfigDelete',

            'ipf_workflow_bgp = bwc_cli.ipf.workflow:WorkflowBGP'
        ],
    },

    zip_safe=False,
)
