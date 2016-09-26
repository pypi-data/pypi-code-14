from constants import START_TEST_COMMAND, TEST_STEP_COMMAND, END_TEST_COMMAND, executionReportUrl


class PerfectoReportiumClient:
    def __init__(self, perfecto_execution_context):
        self.perfecto_execution_context = perfecto_execution_context
        self.webdriver = perfecto_execution_context.webdriver
        self.current_test_id = None

    def test_start(self, name, context):
        params = {}
        job = self.perfecto_execution_context.job

        if job is not None:
            params['jobName'] = job.name
            params['jobNumber'] = job.number

        project = self.perfecto_execution_context.project

        if project is not None:
            params['projectName'] = project.name
            params['projectVersion'] = project.version

        params['name'] = name
        params['tags'] = context.tags

        test_tags = self.perfecto_execution_context.context_tags

        if test_tags is not None:
            params['tags'] += test_tags

        self.current_test_id = self.execute_script(START_TEST_COMMAND, params)
        return self.current_test_id

    def test_step(self, description):
        params = {'name': description}
        return self.execute_script(TEST_STEP_COMMAND, params)

    def test_stop(self, test_result):
        if not self.current_test_id:
            return False
        params = {'success': test_result.is_successful()}

        if test_result.is_successful() is False:
            params['failureDescription'] = test_result.get_message()

        self.execute_script(END_TEST_COMMAND, params)
        return True

    def report_url(self):
        url = ''
        if hasattr(self.webdriver, 'capabilities'):
            url = str(self.webdriver.capabilities[executionReportUrl])
        else:
            raise 'WebDriver instance is assumed to have Selenium Capabilities'
        return url

    def execute_script(self, script, params):
        return self.webdriver.execute_script(script, params)
