import time

from googleapiclient.errors import HttpError

from googleapiwrapper.Exceptions import translate_exception, check_operation_status, ResourceNotFoundException


class DeploymentManager:
    def __init__(self, api):
        self._api = api

    def wait_for_operation(self, project: str, operation_name: str):
        while True:
            operation_status = self._api.operations().get(project=project, operation=operation_name).execute()
            operation_result = check_operation_status(operation_status)
            if operation_result is not None:
                return operation_result
            else:
                time.sleep(1)

    def deployment_exists(self, project: str, deployment_name: str):
        try:
            try:
                self._api.deployments().get(project=project, deployment=deployment_name).execute()
                return True
            except HttpError as e:
                translate_exception(e)
        except ResourceNotFoundException:
            return False
        except HttpError as e:
            translate_exception(e)

    def create_deployment(self,
                          project: str,
                          deployment_name: str,
                          description: str,
                          configuration_path: str,
                          imports: list):
        configuration_fd = open(configuration_path, 'r')
        try:
            configuration_content = configuration_fd.read()
        finally:
            configuration_fd.close()

        try:
            operation = self._api.deployments().insert(project=project,
                                                       body={
                                                           'name': deployment_name,
                                                           'description': description,
                                                           'target': {
                                                               'imports': imports,
                                                               'config': {
                                                                   'content': configuration_content
                                                               }
                                                           }
                                                       }).execute()
            self.wait_for_operation(project, operation['name'])
        except HttpError as e:
            translate_exception(e)

    def update_deployment(self,
                          project: str,
                          deployment_name: str,
                          description: str,
                          configuration_path: str,
                          imports: list):
        try:
            get_deployment_result = self._api.deployments().get(project=project, deployment=deployment_name).execute()
            fingerprint = get_deployment_result['fingerprint']
        except HttpError as e:
            translate_exception(e)
            return

        configuration_fd = open(configuration_path, 'r')
        try:
            configuration_content = configuration_fd.read()
        finally:
            configuration_fd.close()

        try:
            operation = self._api.deployments().update(project=project,
                                                       deployment=deployment_name,
                                                       deletePolicy='DELETE',
                                                       createPolicy='CREATE_OR_ACQUIRE',
                                                       body={
                                                           'name': deployment_name,
                                                           'description': description,
                                                           'fingerprint': fingerprint,
                                                           'target': {
                                                               'imports': imports,
                                                               'config': {
                                                                   'content': configuration_content
                                                               }
                                                           }
                                                       }).execute()
            self.wait_for_operation(project, operation['name'])
        except HttpError as e:
            translate_exception(e)
