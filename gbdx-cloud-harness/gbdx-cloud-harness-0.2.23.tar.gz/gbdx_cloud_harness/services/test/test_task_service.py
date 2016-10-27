import os

from gbdx_cloud_harness.test.conftest import my_vcr, TestApp
from gbdx_cloud_harness.test.auth_mock import get_mock_gbdx_session
from gbdx_cloud_harness.services.task_service import TaskService

test_app = TestApp


@my_vcr.use_cassette('gbdx_cloud_harness/services/test/vcr_cassettes/task_service.yaml', filter_headers=['authorization'])
def test_task_register_delete(test_app):

    cassette_exists = os.path.isfile(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vcr_cassettes', 'task_service.yaml')
    )

    with test_app() as app:

        if cassette_exists:
            # Use mock session, so CI doesn't fail (creds)
            test_auth = get_mock_gbdx_session()
            task_service = TaskService(auth=test_auth)
        else:
            # Create real session
            task_service = TaskService()

        code, message = task_service.register_task(app.task.json())
        assert 'not registered' not in message
        assert code == 200

        code, message = task_service.delete_task(app.task.name)
        assert 'not deleted' not in message
        assert code == 200
