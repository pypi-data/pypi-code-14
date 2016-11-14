# Copyright (c) 2016, Formation Data Systems, Inc. All Rights Reserved.
#
from model.task.completion_status import CompletionStatus

from enum import Enum, unique

@unique
class SafeGuardTaskType(Enum):
    unknown                   = 0
    volume_export             = 1
    incremental_volume_export = 2
    volume_import             = 3
    remote_clone              = 4
    incremental_remote_clone  = 5

    def __str__(self):
        if self.value == SafeGuardTaskType.volume_export.value:
            return "export"
        if self.value == SafeGuardTaskType.volume_import.value:
            return "import"
        if self.value == SafeGuardTaskType.incremental_volume_export.value:
            return "incremental"
        return self.name

class SafeGuardTaskStatus(object):
    '''A point-in-time status for a SafeGuard data migration task.

    Attributes
    ----------
    :type __uuid:

    :type __description: string
    :attr __description: A description of the task

    :type __volume_id: int

    :type __status: ``model.task.CompletionStatus``

    :type __task_type: ``model.task.SafeGuardTaskType``
    '''
    def __init__(self, uuid=-1, description=None, volume_id=-1, status=None,
        task_type=None):

        self.uuid = uuid
        self.description = description
        self.volume_id = volume_id
        self.status = status
        if self.status is None:
            self.status = CompletionStatus.unknown
        self.task_type = task_type
        if self.task_type is None:
            self.task_type = SafeGuardTaskType.unknown

    @property
    def uuid(self):
        return self.__uuid

    @uuid.setter
    def uuid(self, uuid):
        self.__uuid = uuid

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description
 
    @property
    def volume_id(self):
        return self.__volume_id

    @volume_id.setter
    def volume_id(self, volume_id):
        self.__volume_id = volume_id

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def task_type(self):
        return self.__task_type

    @task_type.setter
    def task_type(self, task_type):
        self.__task_type = task_type
