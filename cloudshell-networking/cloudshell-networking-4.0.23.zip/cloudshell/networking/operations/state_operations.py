import os
import platform
from abc import abstractmethod
import re
from cloudshell.networking.operations.interfaces.state_operations_interface import StateOperationsInterface


class StateOperations(StateOperationsInterface):
    def __init__(self):
        self.max_allowed_packet_loss = 20
        pass

    @property
    @abstractmethod
    def logger(self):
        pass

    @property
    @abstractmethod
    def resource_name(self):
        pass

    @property
    @abstractmethod
    def cli(self):
        pass

    @property
    @abstractmethod
    def api(self):
        pass

    def health_check(self):
        """Handle apply connectivity changes request json, trigger add or remove vlan methods,
        get responce from them and create json response

        :return Serialized DriverResponseRoot to json
        :rtype json
        """

        self.logger.info('Start health check on {} resource'.format(self.resource_name))
        success = False
        api_response = 'Online'
        try:
            self.cli.send_command('')
            success = True
        except Exception:
            pass

        result = 'Health check on resource {}'.format(self.resource_name)

        if success:
            result += ' passed.'
        else:
            api_response = 'Error'
            result += ' failed.'

        try:
            self.api.SetResourceLiveStatus(self.resource_name, api_response, result)
        except Exception as e:
            self.logger.error('Cannot update {} resource status on portal'.format(self.resource_name))

        self.logger.info('Health check on {} resource completed'.format(self.resource_name))
        return result

    @abstractmethod
    def shutdown(self):
        pass

    def reload(self):
        pass
