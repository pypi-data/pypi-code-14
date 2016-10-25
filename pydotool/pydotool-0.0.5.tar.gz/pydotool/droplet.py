import json


class Droplet:

    def __init__(self, config):
        self.config = config

    def get_name(self):
        return self.config.get('name')

    def get_id(self):
        return self.config.get('id')

    def get_status(self):
        return self.config.get('status')

    def get_ipv4(self, ip_type):
        networks = self.config.get('networks')
        v4_networks = networks.get('v4')
        for a_network in v4_networks:
            if a_network.get('type') == ip_type:
                return a_network.get('ip_address')

    def __str__(self):
        return json.dumps(self.config)
