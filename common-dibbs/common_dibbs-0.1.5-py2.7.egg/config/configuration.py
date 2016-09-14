

class Configuration(object):

    def __init__(self):
        pass

    def get_appliance_registry_url(self):
        return "http://127.0.0.1:8003"

    def get_operation_registry_url(self):
        return "http://127.0.0.1:8000"

    def get_operation_manager_url(self):
        return "http://127.0.0.1:8001"

    def get_resource_manager_url(self):
        return "http://127.0.0.1:8002"

    def get_operation_manager_agent_url(self):
        return "http://127.0.0.1:8011"

    def get_resource_manager_agent_url(self):
        return "http://127.0.0.1:8012"

    def get_central_authentication_service_url(self):
        return "http://127.0.0.1:7000"
