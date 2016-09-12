import json
import os

from gbdx_task_template.test.test_base import TestBase
from gbdx_task_template.task import Task


class TestTask(TestBase):

    def test_bad_port_obj(self):
        try:
            self.task.bad_port = "Not a Port"
        except TypeError as e:
            assert "Task ports must be of type Port" == e.message

    def test_task_adders(self):
        new_task = Task(
            "ThisTask",
            timeout=1,
            callback='my_func',
            impersonation_allowed=True
        )
        task_json = json.loads(new_task.json())
        assert task_json['timeout'] == 1
        assert task_json['callback'] == 'my_func'
        assert task_json['impersonation_allowed'] is True

    def test_task_json(self):
        print('=====', os.environ.get('REMOTE_WORK_PATH'))
        task_wf = json.loads(self.task.json())
        assert self.task.type.lower() in task_wf['name']
        assert self.task.type == task_wf['taskType']

        # Check Ports
        self.assertEqual(len(task_wf['inputs']), 3)
        for port in task_wf['inputs']:
            self.assertIn(port['name'], self.basic_inport_names)

        self.assertEqual(len(task_wf['outputs']), 1)
        for port in task_wf['outputs']:
            self.assertIn(port['name'], self.basic_outport_names)

    def test_task_validate_local(self):
        print('=====', os.environ.get('REMOTE_WORK_PATH'))
        self.assertTrue(self.task.is_valid())
