__author__ = "Kiran Vemuri"
__email__ = "kkvemuri@uh.edu"
__status__ = "Development"
__maintainer__ = "Kiran Vemuri"

import requests
import json


class OSSession(object):
    """
    OpenStack session
    """

    def __init__(self, openstack_ip, username, password):
        """

        :param openstack_ip: <str> IP address of the openstack node you're trying to connect to
        :param username: <str> username for authentication
        :param password: <str> password for authentication
        """
        self.username = username
        self.password = password
        self.openstack_ip = openstack_ip

        self.identity_url = 'http://' + openstack_ip + ':5000/v3/'
        self.compute_url = None
        self.image_url = None
        self.networking_url = None

        self.Identity = _Identity(self.identity_url, self.username, self.password, domain='default')
        self.scoped_token = self.Identity.fetch_scoped_token()
        self.auth_token = self.scoped_token.headers['X-Subject-Token']
        self.catalog = self.scoped_token.json()['token']['catalog']
        self._fetch_endpoint_urls()

        self.Compute = _Compute(self.compute_url, self.auth_token)
        self.Networking = _Networking(self.networking_url, self.auth_token)
        self.Image = _Image(self.image_url, self.auth_token)

    def _fetch_endpoint_urls(self):
        """
        Fetch endpoints for OpenStack services
        :return: None
        """
        for endpoint in self.catalog:
            if endpoint['name'] == 'nova':
                for detail in endpoint['endpoints']:
                    if detail['interface'] == 'public':
                        self.compute_url = detail['url']
            elif endpoint['name'] == 'glance':
                for detail in endpoint['endpoints']:
                    if detail['interface'] == 'public':
                        self.image_url = detail['url']
            elif endpoint['name'] == 'neutron':
                for detail in endpoint['endpoints']:
                    if detail['interface'] == 'public':
                        self.networking_url = detail['url']
            elif endpoint['name'] == 'glance':
                for detail in endpoint['endpoints']:
                    if detail['interface'] == 'public':
                        self.image_url = detail['url']


class _Compute(object):
    """
    Interface to interact with nova service using REST
    """

    def __init__(self, url, auth_token):
        """
        :param url: <str> URL to reach the compute service
        :param auth_token: <str> auth_token to authorize the compute requests
        """
        self.url = url
        self.auth_token = auth_token
        self.request_headers = {"Content-type": "application/json",
                                "X-Auth-Token": self.auth_token}

    # Servers

    def list_servers(self):
        """
        List existing servers(instances)
        :return: response object returned by the list_servers request
        """
        response = requests.get(self.url + "/servers",
                                headers=self.request_headers)
        return response

    def create_server(self,
                      server_name,
                      image_uuid,
                      flavor_uuid,
                      availability_zone,
                      network_uuid,
                      security_group=None):
        """
        Create a server
        :param server_name: <str> name for the server that is being created
        :param image_uuid: <uuid> UUID of the image that is to be used to boot the server
        :param flavor_uuid: <uuid> UUID of the flavor for the instance
        :param availability_zone: <str> availability_zone to boot the instance in
        :param network_uuid: <uuid> UUID of the network to be associated to the server
        :param security_group: <str> name of the security group to be associated with the instance
        :return: response object returned by the create_Server request
        """
        request_data = json.dumps({
            "server": {
                "name": server_name,
                "imageRef": image_uuid,
                "flavorRef": flavor_uuid,
                "availability_zone": availability_zone,
                "networks": [{
                    "uuid": network_uuid
                }]
            }
        })
        response = requests.post(self.url + "/servers",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    def create_multiple_servers(self):
        pass
        # TODO

    def show_server(self, server_uuid):
        """
        Show server details
        :param server_uuid: <uuid> UUID of the server
        :return: response object returned by the show_server request
        """
        response = requests.get(self.url + "/servers/{}".format(server_uuid),
                                headers=self.request_headers)
        return response

    def delete_server(self, server_uuid):
        """
        Delete a server
        :param server_uuid: <uuid> UUID of the server
        :return: response object returned by the delete_server request
        """
        response = requests.delete(self.url + "/servers/{}".format(server_uuid),
                                   headers=self.request_headers)
        return response

    def reboot_server(self):
        pass
        # TODO

    def live_migrate_server(self):
        pass
        # TODO

    # Floating IP

    def associate_floatingip(self):
        pass
        # TODO

    def disassociate_floatingip(self):
        pass
        # TODO

    # Flavors

    def list_flavors(self):
        """
        List existing flavors
        :return: response object returned by the list_flavors request
        """
        response = requests.get(self.url + "/flavors",
                                headers=self.request_headers)
        return response

    def list_flavors_detail(self):
        """
        List flavors with details
        :return: response object returned by the list_flavors_detail request
        """
        response = requests.get(self.url + "/flavors/detail",
                                headers=self.request_headers)
        return response

    def create_flavor(self, flavor_name, ram, vcpu_count, disk):
        """
        Create a flavor
        :param flavor_name: <str> name for the flavor that is being created
        :param ram: <int> RAM Size
        :param vcpu_count: <int> Number of vcpu's
        :param disk: <int> Size of the disk
        :return: response object returned by the create_flavor request
        """
        request_data = json.dumps({
            "flavor": {
                "name": flavor_name,
                "ram": ram,
                "vcpus": vcpu_count,
                "disk": disk
            }
        })
        response = requests.post(self.url + "/flavors",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    def delete_flavor(self, flavor_uuid):
        """
        Delete a flavor
        :param flavor_uuid: <uuid> UUID of the flavor that is to be deleted
        :return: response object returned by the delete_flavor request
        """
        response = requests.delete(self.url + "/flavors/{}".format(flavor_uuid),
                                   headers=self.request_headers)
        return response

    def show_flavor_details(self, flavor_uuid):
        """
        Show flavor details
        :param flavor_uuid: <uuid> UUID of the flavor whose details are being requested
        :return: response object returned by the show_flavor_details request
        """
        response = requests.get(self.url + "/flavors/{}".format(flavor_uuid),
                                headers=self.request_headers)
        return response

    # Key pairs

    def list_keypairs(self):
        """
        List existing keypairs
        :return: response object returned by the list_keypairs request
        """
        response = requests.get(self.url + "/os-keypairs",
                                headers=self.request_headers)
        return response

    def delete_keypair(self, keypair_name):
        """
        Delete a keypair
        :param keypair_name: <str> name of the keypair that is to be created
        :return: response object returned by the delete_keypair request
        """
        response = requests.delete(self.url + "/os-keypairs/{}".format(keypair_name),
                                   headers=self.request_headers)
        return response

    def create_import_keypair(self, keypair_name, public_key=None):
        """
        Create/Import a keypair
        :param keypair_name: <str> Name for the keypair that is being created
        :param public_key: <str> public_key for the keypair that is being imported. Default = None
        :return: response object returned by the create_import_keypair request
        """
        if public_key:
            request_data = json.dumps({
                "keypair": {
                    "name": keypair_name,
                    "public_key": public_key
                }
            })
        else:
            request_data = json.dumps({
                "keypair": {
                    "name": keypair_name
                }
            })

        response = requests.post(self.url + "/os-keypairs",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    # Images

    def list_images(self):
        """
        List existing images
        :return: response object returned by the list_images request
        """
        response = requests.get(self.url + "/images",
                                headers=self.request_headers)
        return response

    def list_images_detail(self):
        """
        List images with details
        :return: response object returned by the list_images_detail request
        """
        response = requests.get(self.url + "/images/detail",
                                headers=self.request_headers)
        return response

    def show_image_details(self, image_uuid):
        """
        Show image details
        :param image_uuid: <uuid> UUID of the image whose details are being requested
        :return: response object returned by the show_image_details request
        """
        response = requests.get(self.url + "/images/{}".format(image_uuid),
                                headers=self.request_headers)
        return response

    def delete_image(self, image_uuid):
        """
        Delete image
        :param image_uuid: <uuid> UUID of the image that is to be deleted
        :return: response object returned by the delete_image request
        """
        response = requests.delete(self.url + "/images/{}".format(image_uuid),
                                   headers=self.request_headers)
        return response

    # Availability zones

    def get_availability_zone_info(self):
        """
        Get availability zone info
        :return: response object returned by the availability_zone request
        """
        response = requests.get(self.url + "/os-availability-zone",
                                headers=self.request_headers)
        return response

    def get_availability_zone_info_details(self):
        """
        Get availability zone info with details
        :return: response object returned by the availability_zone_detail request
        """
        response = requests.get(self.url + "/os-availability-zone/detail",
                                headers=self.request_headers)
        return response

    # Ping instances

    def ping_all(self):
        """
        Ping all instances and list the instances that are alive
        :return: response object returned by the ping_all request
        """
        response = requests.get(self.url + "/os-fping",
                                headers=self.request_headers)
        return response

    def ping_instance(self, instance_uuid):
        """
        Ping a specific instance and return the status of the instance
        :param instance_uuid: <uuid> UUID of the instance to be pinged
        :return: response object returned by the ping_instance request
        """
        response = requests.get(self.url + "/os-fping/{}".format(instance_uuid),
                                headers=self.request_headers)
        return response

    # Security groups

    def list_secutity_groups(self):
        """
        List existing security groups
        :return: response object returned by the list_security_groups request
        """
        response = requests.get(self.url + "/os-security-groups",
                                headers=self.request_headers)
        return response

    def create_security_group(self):
        pass
        # TODO

    def show_security_group(self):
        pass
        # TODO

    def update_security_group(self):
        pass
        # TODO

    def delete_security_group(self):
        pass
        # TODO

    # Default security group rules | Not currently supported by neutron driver

    """
    def list_default_security_group_rules(self):
        request_headers = {"Content-type": "application/json",
                           "X-Auth-Token": self.auth_token}
        response = requests.get(self.url + "/os-security-group-default-rules",
                                headers=request_headers)
        return response.json()

    def create_default_security_group_rule(self):
        pass

    def delete_default_security_group_rule(self):
        pass

    """

    # Rules for security group

    def create_security_group_rule(self):
        pass
        # TODO

    def delete_security_group_rule(self):
        pass
        # TODO


class _Identity(object):
    """
        Interface to interact with keystone service using REST
        """

    def __init__(self, url, username, password, domain='default'):
        self.url = url
        self.username = username
        self.password = password
        self.domain = domain
        self.unscoped_token = self.fetch_unscoped_token()
        self.user_id = self.unscoped_token.json()['token']['user']['id']
        self.project_json = self.fetch_user_projects().json()

    # Authentication and Token Management

    def fetch_unscoped_token(self):
        """
        Fetch token from keystone server
        :return: <tuple> token_json, auth_json from response returned by tokens request
        """

        request_data = json.dumps({"auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": self.username,
                        "domain": {
                            "name": "Default"
                        },
                        "password": self.password
                    }
                }
            }
        }
        })
        request_headers = {"Content-type": "application/json"}
        response = requests.post(self.url + "auth/tokens",
                                 data=request_data,
                                 headers=request_headers)

        return response

    def fetch_scoped_token(self):
        """
        Fetch service endpoints from the keystone server
        :return: json response returned by endpoints request
        """
        request_data = json.dumps({"auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": self.username,
                        "domain": {
                            "name": "Default"
                        },
                        "password": self.password
                    }
                }
            },
            "scope": {
                "project": {
                    "id": self.project_json['projects'][0]['id']
                }
            }
        }
        })
        request_headers = {"Content-type": "application/json"}
        response = requests.post(self.url + "/auth/tokens",
                                 headers=request_headers,
                                 data=request_data)
        return response

    # Users
    def fetch_user_projects(self):
        """
        Fetch project details
        :return: json response returned by projects request
        """
        request_headers = {
            "Content-type": "application/json",
            "X-Auth-Token": self.unscoped_token.headers['X-Subject-Token']
        }
        response = requests.get(self.url + "/users/" + self.user_id + "/projects",
                                headers=request_headers)

        return response


class _Image(object):
    """
    Interface to interact with OpenStack image service using v2 REST API
    """

    def __init__(self, url, auth_token):
        """

        :param url: <str> URL to reach image service
        :param auth_token: <str> auth_token to authorize the request
        """
        self.url = url
        self.auth_token = auth_token
        self.request_headers = {"Content-type": "application/json",
                                "X-Auth-Token": self.auth_token}

    def create_image(self):
        # TODO
        pass

    def show_image_details(self, image_uuid):
        response = requests.get(self.url + "/v2/images/{}".format(image_uuid),
                                headers=self.request_headers)
        return response

    def list_images(self):
        response = requests.get(self.url + "/v2/images",
                                headers=self.request_headers)
        return response

    def delete_image(self, image_uuid):
        response = requests.delete(self.url + "/v2/images/{}".format(image_uuid),
                                   headers=self.request_headers)
        return response

    def deactivate_image(self, image_uuid):
        response = requests.post(self.url + "/v2/images/{}/actions/deactivate".format(image_uuid),
                                 headers=self.request_headers)
        return response

    def reactivate_image(self, image_uuid):
        response = requests.post(self.url + "/v2/images/{}/actions/reactivate".format(image_uuid),
                                 headers=self.request_headers)
        return response


class _Networking(object):

    """
    Interface to interact with neutron service using REST
    """

    def __init__(self, url, auth_token):
        """

        :param url: <str> URL to reach networking service
        :param auth_token: <str> auth_token to authorize the request
        """
        self.url = url
        self.auth_token = auth_token
        self.request_headers = {"Content-type": "application/json",
                                "X-Auth-Token": self.auth_token}

    # Internal Network

    def list_networks(self):
        """
        List existing networks
        :return: response object received from list_networks request
        """
        response = requests.get(self.url + "/v2.0/networks",
                                headers=self.request_headers)
        return response

    def show_network(self, network_uuid):
        """
        Show network details
        :param network_uuid: <uuid> UUID of the network to fetch network details
        :return: response object from show_network request
        """
        response = requests.get(self.url + "/v2.0/networks/{}".format(network_uuid),
                                headers=self.request_headers)
        return response

    # def create_network(self, **kwargs):
    def create_network(self, network_name, admin_state=True, shared=False, external=False):
        """
        Create a network
        :param network_name: <str> Name for the new network being created
        :param admin_state: <bool> boolean flag for admin_state up/down. Default = True
        :param shared: <bool> boolean flag to indicate network shared true/false. Default = False
        :param external: <bool> boolean flag to indicate whether the network is external true/false. Default = False
        :return: response object from create_network request
        """
        # request_data = json.dumps(get_network_dict(kwargs))

        request_data = json.dumps({
            "network": {
                "name": network_name,
                "admin_state_up": admin_state,
                "shared": shared,
                "router:external": external
            }
        })

        response = requests.post(self.url + "/v2.0/networks",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    def update_network(self, network_uuid, network_name):
        """
        Update a network
        :param network_uuid: <uuid> UUID of the network to be updated
        :param network_name: <str> New name to be updated for the network
        :return: response object returned by the update_network request
        """
        request_data = json.dumps({
            "network": {
                "name": network_name
            }
        })
        response = requests.put(self.url + "/v2.0/networks/{}".format(network_uuid),
                                headers=self.request_headers,
                                data=request_data)
        return response

    def delete_network(self, network_uuid):
        """
        Delete a network
        :param network_uuid: <UUID> UUID of the network to be deleted
        :return: Response object generated by the network_delete request. Error Codes: 409, 404, 204, 401
        """
        response = requests.delete(self.url + "/v2.0/networks/{}".format(network_uuid),
                                   headers=self.request_headers)
        return response

    # External Network

    # Subnets

    def list_subnets(self):
        """
        List existing subnets
        :return: response object generated by the list_subnets request.
        """
        response = requests.get(self.url + "/v2.0/subnets",
                                headers=self.request_headers)
        return response

    def create_subnet(self, subnet_name, network_uuid, cidr, ip_version=4, **kwargs):
        """
        Create a subnet attached to a network
        :param subnet_name: <str> name for the subnet being created
        :param network_uuid: <UUID> UUID of the network to which the subnet is to be associated
        :param cidr: <cidr> valid subnet CIDR
        :param ip_version: <int> ip protocol version 4/6. default = 4
        :param kwargs:
            enable_dhcp: <bool> True/False

            dns_nameservers: <list> list of IP addresses for dns servers

            allocation_pools: [{start : '', end: ''}] list of allocation pool dictionaries with 'start' and 'end' keys
            with values being IP addresses in string format

            gateway_ip: <str> IP address

        :return: response object returned by create_subnet request
        """
        subnet_dict = {
            "subnet": {
                "name": subnet_name,
                "network_id": network_uuid,
                "ip_version": ip_version,
                "cidr": cidr
            }
        }

        subnet_elements = ["enable_dhcp",
                           "dns_nameservers",
                           "allocation_pools",
                           "host_routes",
                           "gateway_ip"]

        for args_key in kwargs:
            if args_key in subnet_elements:
                subnet_dict["subnet"][args_key] = kwargs[args_key]

        print subnet_dict
        request_data = json.dumps(subnet_dict)
        response = requests.post(self.url + "/v2.0/subnets",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    def show_subnet(self, subnet_uuid):
        """
        Show subnet details
        :param subnet_uuid: <UUID> UUID of the subnet whose details are being requested
        :return: response object returned by the show_subnet request
        """
        response = requests.get(self.url + "/v2.0/subnets/{}".format(subnet_uuid),
                                headers=self.request_headers)
        return response

    def update_subnet(self, subnet_uuid, subnet_name):
        """
        Update subnet
        :param subnet_uuid: <uuid> uuid of the subnet that is to be updated
        :param subnet_name: <str> new name for the subnet
        :return: response object returned by the update_subnet request
        """
        request_data = json.dumps({
            "subnet": {
                "name": subnet_name
            }
        })
        response = requests.put(self.url + "/v2.0/subnets/{}".format(subnet_uuid),
                                headers=self.request_headers,
                                data=request_data)
        return response

    def delete_subnet(self, subnet_uuid):
        """
        Delete a subnet
        :param subnet_uuid: <UUID> UUID of the subnet that is to be deleted
        :return: response object returned by the delete_subnet request
        """
        response = requests.delete(self.url + "/v2.0/subnets/{}".format(subnet_uuid),
                                   headers=self.request_headers)
        return response

    # Ports

    def list_ports(self):
        """
        List existing ports
        :return: response object returned by list_ports request
        """
        response = requests.get(self.url + "/v2.0/ports",
                                headers=self.request_headers)
        return response

    def show_port(self, port_uuid):
        """
        Show port details
        :param port_uuid: <uuid> UUID of the port
        :return: response object returned by the show_port request
        """
        response = requests.get(self.url + "/v2.0/ports/{}".format(port_uuid),
                                headers=self.request_headers)
        return response

    def create_port(self):
        pass
        # TODO

    def delete_port(self, port_uuid):
        """
        Delete a port
        :param port_uuid: <uuid> UUID of the port that is to be deleted
        :return: response object returned by the delete_port request
        """
        response = requests.delete(self.url + "/v2.0/ports/{}".format(port_uuid),
                                   headers=self.request_headers)
        return response

    # Routers

    def list_routers(self):
        """
        List existing routers
        :return: response object returned by the list_routers request
        """
        request_headers = {"Content-type": "application/json",
                           "X-Auth-Token": self.auth_token}
        response = requests.get(self.url + "/v2.0/routers",
                                headers=request_headers)
        return response

    def show_router(self, router_uuid):
        """
        Show router details
        :param router_uuid: <UUID> UUID of the router whose details are to be requested
        :return: response object returned by the show_router request
        """
        response = requests.get(self.url + "/v2.0/routers/{}".format(router_uuid),
                                headers=self.request_headers)
        return response

    def create_router(self, router_name, admin_state=True):
        """
        Create a router
        :param router_name: <str> Name for the router that is being created
        :param admin_state: <bool> boolean flag to represent if the admin_state of the router is up/down.
                            Default = True
        :return: response object returned by the create_router request
        """
        request_data = json.dumps({
            "router": {
                "name": router_name,
                "admin_state_up": admin_state
            }
        })
        response = requests.post(self.url + "/v2.0/routers",
                                 headers=self.request_headers,
                                 data=request_data)
        return response

    def update_router(self, router_uuid, router_name):
        """
        Update router
        :param router_uuid: <uuid> uuid of the router that is to be updated
        :param router_name: <str> new name for the router
        :return: response object returned by the update_router request
        """
        request_data = json.dumps({
            "router": {
                "name": router_name
            }
        })
        response = requests.put(self.url + "/v2.0/routers/{}".format(router_uuid),
                                headers=self.request_headers,
                                data=request_data)
        return response

    def delete_router(self, router_uuid):
        """
        Delete router
        :param router_uuid: <uuid> UUID of the router that is to be deleted
        :return: response object returned by the delete_router request
        """
        response = requests.delete(self.url + "/v2.0/routers/{}".format(router_uuid),
                                   headers=self.request_headers)
        return response

    def add_router_interface(self, router_uuid, subnet_uuid):
        """
        Add a router interface from a subnet to the router
        :param router_uuid: <uuid> UUID of the router
        :param subnet_uuid: <uuid> UUID of the subnet to which a router_interface will be added
        :return: response object returned by the add_router_interface request
        """
        request_data = json.dumps({
            "subnet_id": subnet_uuid
        })
        response = requests.put(self.url + "/v2.0/routers/{}/add_router_interface".format(router_uuid),
                                headers=self.request_headers,
                                data=request_data)
        return response

    def remove_router_interface(self, router_uuid, subnet_uuid):
        """
        Remove a router interface from a subnet
        :param router_uuid: <uuid> UUID of the router
        :param subnet_uuid: <uuid> UUID of the subnet to which a router_interface will be added
        :return: response object returned by the add_router_interface request
        """
        request_data = json.dumps({
            "subnet_id": subnet_uuid
        })
        response = requests.put(self.url + "/v2.0/routers/{}/remove_router_interface".format(router_uuid),
                                headers=self.request_headers,
                                data=request_data)
        return response
