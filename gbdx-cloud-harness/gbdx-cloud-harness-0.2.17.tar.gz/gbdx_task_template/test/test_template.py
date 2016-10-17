import json

from gbdx_task_template.test.test_base import TestBase, MyBasicApp, BadTaskApp
from gbdx_task_template import TaskTemplate


class TestApplicationTemplate(TestBase):

    def test_app(self):
        with MyBasicApp() as task:
            task.invoke()
            task.reason = "All ok"

            self.assertTrue(self._is_json_valid(task.task.json()))

    def test_bad_app(self):
        try:
            with BadTaskApp() as task:
                task.invoke()
        except Exception as e:
            self.assertIn('MyCustomTask', e.message)

    def test_no_task(self):

        class NewTask(TaskTemplate):
            pass

        try:
            with NewTask() as t:
                pass
        except ValueError as e:
            assert 'A task must be initialized before running a TaskTemplate subclass.' == e.message

    @staticmethod
    def _is_json_valid(json_str):
        try:
            json.loads(json_str)
            return True
        except:
            return False
