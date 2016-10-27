import os
import pytest
import vcr

from gbdx_cloud_harness.test.auth_mock import get_mock_gbdx_session
from gbdx_task_template import TaskTemplate, Task, InputPort, OutputPort


# So vcr doesn't record Amazon requests, moto will mock this.
my_vcr = vcr.VCR(
    ignore_hosts=['s3.amazonaws.com', '169.254.169.254'],  # This IP address is a temp fix.
)


@pytest.fixture(scope='module')
def mock_auth():
    return get_mock_gbdx_session()


@pytest.fixture(scope='module')
def test_path():
    return os.path.dirname(os.path.abspath(__file__))


# Test class
class BasicApp(TaskTemplate):

    task = Task("MyCustomTask")  # Create the Task
    task.properties = {
        "timeout": 9600,
        "isPublic": False
    }  # Update Properties

    task.first_port = InputPort(port_type="string", value="Hello")
    task.second_port = InputPort(value="~/mydata/input/")

    task.output_port = OutputPort(value="~/mydata/output/")
    task.output_param = OutputPort(port_type="string", value="~/mydata/output/")

    def invoke(self):
        print("\n\tHello, World!")


@pytest.fixture()
def TestApp():
    return BasicApp




