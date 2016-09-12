import os
import json
import uuid

from gbdx_task_template.port import Port, InputPort, OutputPort


class Task(object):
    """
    Class to encapsulate the Task configuration
    """

    def __init__(self, name, **kwargs):
        self._task_name = name
        self._task_type = "CloudHarness_Anonymous_Task"

        # JSON for this task only.
        self._task_wf_json = {
            "inputs": [],
            "outputs": [],
            "properties": {"timeout": 7200},
            "taskType": self._task_type,
            "name": '%s_%s' % (self._task_type.lower(), str(uuid.uuid4()))
        }

        if 'timeout' in kwargs.keys():
            self._task_wf_json['timeout'] = kwargs['timeout']

        if 'impersonation_allowed' in kwargs.keys():
            self._task_wf_json['impersonation_allowed'] = kwargs['impersonation_allowed']

        if 'callback' in kwargs.keys():
            self._task_wf_json['callback'] = kwargs['callback']

        # Add default source bundle port
        port_name = "source_bundle"
        dest_path = os.path.join(os.getcwd(), port_name)
        srcbundle = InputPort(value=dest_path)
        srcbundle.name = port_name
        srcbundle.multiplex = False
        self.source_bundle = srcbundle

    def __setattr__(self, key, value):
        # Check if key already exists
        if Port.is_port(value):
            value.name = key
            self.add_port(value)

        super(Task, self).__setattr__(key, value)

    @property
    def definition(self):
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'task_definition.json'
        )

        with open(filename, 'r') as f:
            return json.loads(f.read())

    @property
    def src_path(self):
        return self.source_bundle.value

    @property
    def type(self):
        return self._task_type

    @property
    def name(self):
        return self._task_name

    @name.setter
    def name(self, value):
        self._task_name = value

    @property
    def input_ports(self):
        return self._task_wf_json['inputs']

    @property
    def output_ports(self):
        return self._task_wf_json['outputs']

    @property
    def ports(self):
        return self._task_wf_json['inputs'], self._task_wf_json['outputs']

    def json(self):
        return json.dumps(self._task_wf_json, cls=CustomEncoder, indent=2)

    def add_port(self, new_port):
        if not Port.is_port(new_port):
            raise TypeError("Task ports must be of type Port")

        if new_port.direction == 'Input':
            self._task_wf_json['inputs'].append(new_port)
        elif new_port.direction == 'Output':
            self._task_wf_json['outputs'].append(new_port)

    def is_valid(self, remote=False):
        """
        Check cloud-harness code is valid. task schema validation is
        left to the API endpoint.
        :param remote: Flag indicating if the task is being ran on the platform or not.
        :return: is valid or not.
        """

        if len(self.input_ports) < 1:
            return False

        if remote:
            # Ignore output ports as value will overriden.
            ports = [
                port for port in self.input_ports if port.type == 'directory'
                ]
            for port in ports:
                # Will raise exception if the port is invalid.
                port.is_valid_s3_url(port.value)
        else:
            all_ports = self.ports[0] + self.ports[1]
            ports = [
                port for port in all_ports if port.type == 'directory' and port.name != 'source_bundle'
                ]
            for port in ports:
                # Will raise exception if the port is invalid.
                port.is_valid_filesys(port.value)

        return True


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        # For Port instances
        if isinstance(obj, Port):
            return obj.json
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
