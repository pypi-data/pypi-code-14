# Copyright 2016 Formation Data Systems, Inc. All Rights Reserved.
#
import json
from model.task.completion_status import CompletionStatus
from model.task.safeguard_task_status import SafeGuardTaskStatus, SafeGuardTaskType

class SafeGuardTaskConverter(object):
    '''Helper class for marshalling between SafeGuardTaskStatus and JSON formatted string.

    The term 'to marshal' means to convert some data from internal to external form
    (in an RPC buffer for instance). The term 'unmarshalling' refers to the reverse
    process. We presume that the server will use reflection to create a Java object
    given the JSON formatted string.
    '''

    @staticmethod
    def to_json_string(task_with_status):
        '''Converts ``model.task.SafeGuardTaskStatus`` object into a JSON formatted string.

        We presume that the recipient (a server) uses a package like Gson and passes the type
        literal when deserializing the JSON formatted string.

        Parameters
        ----------
        :type task_with_status: ``model.task.SafeGuardTaskStatus`` object

        Returns
        -------
        :type string
        '''
        d = dict()

        d["uuid"] = task_with_status.uuid
        d["description"] = task_with_status.description
        d["volume_id"] = int(task_with_status.volume_id)
        d["completionState"] = str(task_with_status.status)
        d["type"] = str(task_with_status.task_type)

        result = json.dumps(d)
        return result;

    @staticmethod
    def build_from_json(j_str):
        '''Produce a ``model.task.SafeGuardTaskStatus`` object from deserialized server response

        Parameters
        ----------
        :type j_str: dict or json-encoded string representing a JSON object

        Returns
        -------
        :type ``model.task.SafeGuardTaskStatus``
        '''
        task_with_status = SafeGuardTaskStatus()

        # If given argument not a dict, decode to a dict
        if not isinstance(j_str, dict):
            j_str = json.loads(j_str)

        task_with_status.uuid = j_str.pop("uuid", task_with_status.uuid)
        task_with_status.volume_id = int(j_str.pop("volumeId", task_with_status.volume_id))
        if "description" in j_str:
            task_with_status.description = j_str.pop("description", task_with_status.description)
        status_str = j_str.pop("completionState", "unknown")
        for s in CompletionStatus:
            if str(s) == str(status_str.lower()):
                task_with_status.status = s
                break

        type_str = j_str.pop("type", "unknown")
        for t in SafeGuardTaskType:
            if str(t) == str(type_str.lower()):
                task_with_status.task_type = t
                break

        return task_with_status
