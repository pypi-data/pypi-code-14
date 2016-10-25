import sys
import json
import uuid
import itertools
import time

from gbdx_cloud_harness.services.account_storage_service import AccountStorageService


class Workflow(object):
    """
    Class for building workflow objects that can generate a workflow definition
    from the cloud-harness object.
        Requirements:
            - build json workflow
            - execute workflow
            - succeeded property
            - complete property
            - monitor function
    """

    URL = "https://geobigdata.io/workflows/v1/workflows"
    STAGE_TO_S3 = {'inputs': [], 'taskType': 'StageDataToS3', 'name': 'StageToS3_%s' % str(uuid.uuid4())}

    def __init__(self, task, auth=None):

        if auth is None:
            self.storage = AccountStorageService()
            self.gbdx = self.storage.auth
        else:
            # Testing
            self.gbdx = auth
            self.storage = AccountStorageService(is_test=True)

        self.task_template = task

        self.id = None
        self.status = None

    @property
    def json(self):
        return self._build_worklfow_json()

    def _build_worklfow_json(self):
        """
        Build a workflow definition from the cloud_harness task.
        """
        wf_json = {'tasks': [], 'name': 'cloud-harness_%s' % str(uuid.uuid4())}

        task_def = json.loads(self.task_template.json())

        d = {
            "name": task_def['name'],
            "outputs": [],
            "inputs": [],
            "taskType": task_def['taskType']
        }

        # Add input ports
        for port in self.task_template.input_ports:
            port_value = port.value

            if port_value is False:
                port_value = 'false'
            if port_value is True:
                port_value = 'true'

            d['inputs'].append({
                "name": port._name,
                "value": port_value
            })

        # Add output ports
        for port in self.task_template.output_ports:
            d['outputs'].append({
                "name": port._name
            })

        # Add task to workflow
        wf_json['tasks'].append(d)

        # Add port to be saved
        for port in self.task_template.output_ports:
            # Add save data locations
            if hasattr(port, 'stageToS3') and port.stageToS3:
                save_location = '{customer_storage}/{run_name}/{port}'.format(
                    customer_storage=self.storage.location,
                    run_name=self.task_template.run_name,
                    port=port.name
                )
                new_task = dict(**self.STAGE_TO_S3)
                new_task['inputs'] = [
                    {'name': 'data', 'source': '%s:%s' % (task_def['name'], port._name)},
                    {'name': 'destination', 'value': save_location}
                ]
                wf_json['tasks'].append(new_task)

        return wf_json

    def execute(self, override_wf_json=None):
        """
        Execute the cloud_harness task.
        """
        r = self.gbdx.post(
            self.URL,
            json=self.json if override_wf_json is None else override_wf_json
        )

        try:
            r.raise_for_status()
        except:
            print("GBDX API Status Code: %s" % r.status_code)
            print("GBDX API Response: %s" % r.text)
            self.id = None
            return

        self.id = r.json()['id']
        self._refresh_status()

    @property
    def succeeded(self):
        self._refresh_status()
        return self.status['state'] == 'complete' and self.status['event'] == 'succeeded'

    @property
    def complete(self):
        self._refresh_status()
        return self.status['state'] == 'complete'

    def _refresh_status(self):
        r = self.gbdx.get('%s/%s' % (self.URL, self.id))
        self.status = r.json()['state']

    def monitor_run(self):  # pragma: no cover
        """
        Monitor the workflows events and display spinner while running.
        :param workflow: the workflow object
        """

        spinner = itertools.cycle(['-', '/', '|', '\\'])

        while not self.complete:
            for i in xrange(300):
                sys.stdout.write(spinner.next())
                sys.stdout.flush()
                sys.stdout.write('\b')
                time.sleep(0.03)

        if self.succeeded:
            sys.stdout.write("\nWorkflow completed successfully\n")
            return True
        else:
            sys.stdout.write("\nWorkflow failed: %s\n" % self.status)
            return False
