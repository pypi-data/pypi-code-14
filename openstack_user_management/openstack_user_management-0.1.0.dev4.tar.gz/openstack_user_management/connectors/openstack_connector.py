#!/usr/bin/env python
# osc-lib.py - Example using OSC as a library

# Copyright 2016 TUBITAK B3LAB
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from keystoneauth1 import exceptions as ka_exceptions
from keystoneauth1 import loading
from keystoneauth1 import session
from keystoneclient import exceptions as ks_exceptions
from neutronclient.v2_0 import client as neutron_client
from neutronclient.common import exceptions as n_exceptions
from openstackclient.api import auth
from openstackclient.common import clientmanager
from openstack_user_management.utils import log
from os_client_config import config as cloud_config

LOG = log.get_logger()

__neutronclient_version__ = '2'


class OpenstackConnector:
    def __init__(self):
        cc = cloud_config.OpenStackConfig()
        LOG.debug("defaults: %s", cc.defaults)

        # clouds.yaml file should either be in the
        # current directory or
        # ~/.config/openstack directory or
        # /etc/openstack directory.
        # And it should contain cloud-admin
        # connection properties, or modify the following line.
        cloud = cc.get_one_cloud('cloud-admin')
        LOG.debug("cloud cfg: %s", cloud.config)

        self.client_manager = self.get_client_manager(cloud)
        auth.get_plugin_list()
        type(self.client_manager.auth_ref)

        # We still need to use neutronclient until openstackclient
        # is able to add interface router
        self.neutron_manager = self.get_neutron_manager(cloud)

    @staticmethod
    def get_client_manager(cloud):

        api_version = {"identity": "3",
                       "compute": "2",
                       "volume": "2",
                       "network": "2"}
        return clientmanager.ClientManager(
            cli_options=cloud,
            api_version=api_version,
        )

    @staticmethod
    def get_neutron_manager(cloud):

        auth_param = cloud.config['auth']
        auth_url = auth_param['auth_url']
        username = auth_param['username']
        password = auth_param['password']
        project_name = auth_param['project_name']
        project_domain_name = auth_param['project_domain_name']
        user_domain_name = auth_param['user_domain_name']

        identity_api_version = cloud.config['identity_api_version']
        if identity_api_version == '3':
            loader = loading.get_plugin_loader('password')
            auth = loader.load_from_options(
                                auth_url=auth_url,
                                username=username,
                                password=password,
                                project_name=project_name,
                                user_domain_name=user_domain_name,
                                project_domain_name=project_domain_name)
            sess = session.Session(auth=auth)
            return neutron_client.Client(session=sess)
        elif identity_api_version == '2':
            return neutron_client.Client(username,
                                         password,
                                         project_name,
                                         auth_url)

    def check_username_availability(self,
                                    user_name,
                                    domain_name="default"):
        try:
            domain = self.client_manager.identity.domains.find(
                                                        name=domain_name)
            user = self.client_manager.identity.users.find(name=user_name,
                                                           domain=domain)
            if user is not None:
                return False
        except ka_exceptions.NotFound:
            return True

    def check_projectname_availability(self,
                                       project_name,
                                       domain_name="default"):
        try:
            domain = self.client_manager.identity.domains.find(
                name=domain_name)
            project = self.client_manager.identity.projects.find(
                name=project_name,
                domain=domain)
            if project is not None:
                return False
        except ka_exceptions.NotFound:
            return True

    def create_project(self, domain_name, description, project_name,
                       prop_key, prop_value, enabled=False):
        try:
            domain = self.client_manager.identity.domains.find(
                                             name=domain_name)
            self.client_manager.identity.projects.create(
                                             name=project_name,
                                             domain=domain,
                                             description=description,
                                             enabled=enabled,
                                             prop_key=prop_value)
        except ka_exceptions.ClientException as ex:
            LOG.error("Project not created. Error: " + ex.message)
            return False
        return True

    def create_user(self, domain_name, email,
                    user_name, password, enabled=False):
        try:
            domain = self.client_manager.identity.domains.find(
                                                      name=domain_name)
            self.client_manager.identity.users.create(name=user_name,
                                                      domain=domain,
                                                      email=email,
                                                      password=password,
                                                      enabled=enabled)
        except ka_exceptions.ClientException as ex:
            LOG.error("User not created. Error: " + ex.message)
            return False
        return True

    def pair_user_with_project(self, user_name, project_name,
                               role_name, domain_name="default"):
        try:
            domain = self.client_manager.identity.domains.find(
                                                        name=domain_name)
            user = self.client_manager.identity.users.find(name=user_name,
                                                           domain=domain)
            project = self.client_manager.identity.projects.find(
                                                        name=project_name,
                                                        domain=domain)
            role = self.client_manager.identity.roles.find(name=role_name)
            self.client_manager.identity.roles.grant(role=role,
                                                     project=project,
                                                     user=user)
        except ks_exceptions.ClientException as ex:
            LOG.error("User not paired with project. Error: " +
                      str(ex.message))
            return False
        return True

    def update_project_status(self, project_name, enabled,
                              domain_name="default"):
        try:
            domain = self.client_manager.identity.domains.find(
                                                        name=domain_name)
            project = self.client_manager.identity.projects.find(
                                                        name=project_name,
                                                        domain=domain)
            self.client_manager.identity.projects.update(project=project,
                                                         enabled=enabled)
        except ka_exceptions.ClientException as ex:
            LOG.error("Project status not updated. Error: " + ex.message)
            return False
        return True

    def update_user_status(self, user_name, enabled, domain_name="default"):
        try:
            domain = self.client_manager.identity.domains.find(
                                                        name=domain_name)
            user = self.client_manager.identity.users.find(name=user_name,
                                                           domain=domain)
            self.client_manager.identity.users.update(user=user,
                                                      enabled=enabled)
        except ka_exceptions.ClientException as ex:
            LOG.error("User status not updated. Error: " + ex.message)
            return False
        return True

    def update_user_password(self, user_name, password,
                             domain_name="default"):
        try:
            domain = self.client_manager.identity.domains.find(
                                                        name=domain_name)
            user = self.client_manager.identity.users.find(name=user_name,
                                                           domain=domain)
            self.client_manager.identity.users.update(user=user,
                                                      password=password)
        except ka_exceptions.ClientException as ex:
            LOG.error("User password not updated. Error: " + ex.message)
            return False
        return True

    def init_network(self, project_name, external_network_name,
                     dns_nameservers, subnet_cidr, subnet_gateway_ip,
                     domain_name="default"):
        net_name = "private"
        subnet_name = "private"
        router_name = "router"
        try:
            domain = self.client_manager.identity.domains.find(
                                                        name=domain_name)
            project = self.client_manager.identity.projects.find(
                                                        name=project_name,
                                                        domain=domain)

            # CREATE NETWORK

            # opestackclient method
            # net = self.client_manager.network.create_network(
            #                                           name=net_name,
            #                                           tenant_id=project.id,
            #                                           admin_state_up=True)

            network_param = {'name': net_name,
                             'admin_state_up': True,
                             'tenant_id': project.id}
            network = self.neutron_manager.create_network(
                                            {'network': network_param})

            # CREATE SUBNET

            # opestackclient method
            # subnet = self.client_manager.network.create_subnet(
            #                                name=subnet_name,
            #                                network_id=net.id,
            #                                gateway_ip=subnet_gateway_ip,
            #                                enable_dhcp=True,
            #                                ip_version=4,
            #                                cidr=subnet_cidr,
            #                                dns_nameservers=dns_nameservers)

            subnet_param = {'name': subnet_name,
                            'network_id': network['network']['id'],
                            'tenant_id': project.id,
                            'dns_nameservers': dns_nameservers,
                            'gateway_ip': subnet_gateway_ip,
                            'ip_version': 4,
                            'cidr': subnet_cidr}
            subnet = self.neutron_manager.create_subnet(
                {'subnet': subnet_param})

            # CREATE ROUTER
            # router = self.client_manager.network.create_router(
            #                                     name=router_name,
            #                                     tenant_id=project.id,
            #                                     admin_state_up=True)
            ext_net_id = [e for e in self.neutron_manager.list_networks(
                          )['networks'] if
                          e['name'] == external_network_name][0]['id']
            router_param = {
                'name': router_name,
                'admin_state_up': True,
                'external_gateway_info': {"network_id": ext_net_id},
                'tenant_id': project.id}
            router = self.neutron_manager.create_router(
                {'router': router_param})

            self.neutron_manager.add_interface_router(
                router['router']['id'],
                {'subnet_id': subnet['subnet']['id'],
                 'tenant_id': project.id})

        except n_exceptions.NeutronException as ex:
            LOG.error("Project's initial network could not be defined. "
                      "Error: " + str(ex.message))
            return False
        except ka_exceptions.ClientException as ex:
            LOG.error("Project's initial network could not be defined. "
                      "Error: " + str(ex.message))
            return False
        return True
