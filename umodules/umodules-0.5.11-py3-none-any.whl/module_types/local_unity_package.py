#   Copyright 2016, SpockerDotNet LLC

import logging

from umodules.module_type import IModuleType


def _pull(project, module):
    raise Exception('** Not Yet Implemented **')


class LocalUnityPackage(IModuleType):

    def __init__(self):
        super().__init__()
        self.name = 'local_unity_package'

    def install(self, project):
        super().install(project)

    def status(self, project, module):
        return super().status(project, module)

    def pull(self, project, module):
        super().pull(project, module)
        _pull(project, module)
