import os
import time

import base.base_service.constants
import base

from upfluence.thrift import version


class BaseHandler(object):
    def __init__(self, unit_name=None, interface_modules=[]):
        self._unit_name = unit_name or os.environ.get('UNIT_NAME')
        self._spawn_date = int(time.time())
        self._interface_modules = interface_modules + [base]

    def getName(self):
        return self._unit_name

    def getVersion(self):
        return version

    def getStatus(self):
        return base.base_service.constants.status.ALIVE

    def aliveSince(self):
        return self._spawn_date

    def getInterfaceVersion(self):
        def reduce_versions(acc, module):
            acc[module.__name__.split('.')[0]] = module.base_version
            return acc

        return reduce(reduce_versions, self._interface_modules, {})
