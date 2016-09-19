import json
import os.path
from os.path import expanduser


home = expanduser("~")
# configuration_file_path = "%s/dibbs.json" % (home)
configuration_file_path = "/etc/dibbs/dibbs.json"

class Configuration(object):

    def __init__(self):
        self._reload_config()
        pass

    def _reload_config(self):
        self.configuration = {
            "address": "127.0.0.1"
        }
        if os.path.exists(configuration_file_path):
            with open(configuration_file_path) as data_file:
                try:
                    self.configuration = json.load(data_file)
                except:
                    print("""Found a configuration in "%s", but I could not understand it.""" % (configuration_file_path))

    def get_ip_address(self):
        return self.configuration["address"]

    def get_appliance_registry_url(self):
        self._reload_config()
        return "http://%s:8003" % (self.get_ip_address())

    def get_operation_registry_url(self):
        self._reload_config()
        return "http://%s:8000" % (self.get_ip_address())

    def get_operation_manager_url(self):
        self._reload_config()
        return "http://%s:8001" % (self.get_ip_address())

    def get_resource_manager_url(self):
        self._reload_config()
        return "http://%s:8002" % (self.get_ip_address())

    def get_operation_manager_agent_url(self):
        self._reload_config()
        return "http://%s:8011" % (self.get_ip_address())

    def get_resource_manager_agent_url(self):
        self._reload_config()
        return "http://%s:8012" % (self.get_ip_address())

    def get_central_authentication_service_url(self):
        self._reload_config()
        return "http://%s:7000" % (self.get_ip_address())
