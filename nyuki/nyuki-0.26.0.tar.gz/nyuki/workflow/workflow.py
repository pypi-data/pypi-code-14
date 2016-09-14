import asyncio
from datetime import datetime
import logging
from tukio import Engine, TaskRegistry, get_broker, EXEC_TOPIC
from tukio.workflow import (
    TemplateGraphError, Workflow, WorkflowTemplate, WorkflowExecState
)

from nyuki import Nyuki
from nyuki.bus import reporting
from nyuki.websocket import websocket_ready

from .api.factory import (
    ApiFactoryRegex, ApiFactoryRegexes, ApiFactoryLookup, ApiFactoryLookups,
    ApiFactoryLookupCSV
)
from .api.templates import (
    ApiTasks, ApiTemplates, ApiTemplate, ApiTemplateVersion, ApiTemplateDraft
)
from .api.workflows import (
    ApiWorkflow, ApiWorkflows, ApiWorkflowsHistory, ApiWorkflowHistory,
    serialize_wflow_exec
)

from .storage import MongoStorage
from .tasks import *
from .tasks.utils import runtime


log = logging.getLogger(__name__)


class BadRequestError(Exception):
    pass


def sanitize_workflow_exec(obj):
    """
    Replace any object value by 'internal data' string to store in Mongo.
    """
    types = [dict, list, tuple, str, int, float, bool, type(None), datetime]
    if type(obj) not in types:
        obj = 'Internal server data: {}'.format(type(obj))
    elif isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = sanitize_workflow_exec(value)
    elif isinstance(obj, list):
        for item in obj:
            item = sanitize_workflow_exec(item)
    return obj


class WorkflowInstance:

    """
    Holds a workflow pair of template/instance.
    Allow retrieving a workflow exec state at any moment.
    """

    def __init__(self, template, instance):
        self._template = template
        self._instance = instance

    @property
    def template(self):
        return self._template

    def report(self):
        """
        Merge a workflow exec instance report and its template.
        """
        return {
            **self._template,
            **self._instance.report()
        }


class WorkflowNyuki(Nyuki):

    """
    Generic workflow nyuki allowing data storage and manipulation
    of tukio's workflows.
    https://github.com/optiflows/tukio
    """

    CONF_SCHEMA = {
        'type': 'object',
        'required': ['mongo'],
        'properties': {
            'mongo': {
                'type': 'object',
                'required': ['host'],
                'properties': {
                    'host': {'type': 'string', 'minLength': 1},
                    'database': {'type': 'string', 'minLength': 1}
                }
            },
            'topics': {
                'type': 'array',
                'items': {'type': 'string', 'minLength': 1}
            }
        }
    }
    HTTP_RESOURCES = Nyuki.HTTP_RESOURCES + [
        ApiTasks,  # /v1/workflows/tasks
        ApiTemplates,  # /v1/workflows/templates
        ApiTemplate,  # /v1/workflows/templates/{uid}
        ApiTemplateDraft,  # /v1/workflows/templates/{uid}/draft
        ApiTemplateVersion,  # /v1/workflows/templates/{uid}/{version}
        ApiWorkflows,  # /v1/workflows
        ApiWorkflow,  # /v1/workflows/{uid}
        ApiWorkflowsHistory,  # /v1/workflows/history
        ApiWorkflowHistory,  # /v1/workflows/history/{uid}
        ApiFactoryRegexes,  # /v1/workflows/regexes
        ApiFactoryRegex,  # /v1/workflows/regexes/{uid}
        ApiFactoryLookups,  # /v1/workflows/lookups
        ApiFactoryLookup,  # /v1/workflows/lookups/{uid}
        ApiFactoryLookupCSV,  # /v1/workflows/lookups/{uid}/csv
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_schema(self.CONF_SCHEMA)
        self.migrate_config()
        self.engine = None
        self.storage = None
        # Stores workflow instances with their template data
        self.running_workflows = {}

        self.AVAILABLE_TASKS = {}
        for name, value in TaskRegistry.all().items():
            self.AVAILABLE_TASKS[name] = getattr(value[0], 'SCHEMA', {})

        runtime.bus = self.bus
        runtime.config = self.config

    @property
    def mongo_config(self):
        return self.config['mongo']

    @property
    def topics(self):
        return self.config.get('topics', [])

    async def setup(self):
        self.engine = Engine(loop=self.loop)
        await self.reload_from_storage()
        for topic in self.topics:
            asyncio.ensure_future(self.bus.subscribe(
                self.bus.publish_topic(topic), self.workflow_event
            ))
        # Enable workflow exec follow-up
        get_broker().register(self.report_workflow, topic=EXEC_TOPIC)
        # Set workflow serializer
        self.websocket.serializer = serialize_wflow_exec

    async def reload(self):
        await self.reload_from_storage()

    async def teardown(self):
        if self.engine:
            await self.engine.stop()

    @websocket_ready
    async def websocket_ready(self, token):
        """
        Immediately send all instances of workflows to the client.
        """
        return [
            workflow.report()
            for workflow in self.running_workflows.values()
        ]

    def new_workflow(self, template, instance):
        """
        Keep in memory a workflow template/instance pair.
        """
        wflow = WorkflowInstance(template, instance)
        self.running_workflows[instance.uid] = wflow
        return wflow

    async def report_workflow(self, event):
        """
        Send all worklfow updates to the clients.
        """
        source = event.source._asdict()
        exec_id = source['workflow_exec_id']
        wflow = self.running_workflows[exec_id]
        # Workflow ended, clear it from memory
        if event.data['type'] in [
            WorkflowExecState.end.value,
            WorkflowExecState.error.value
        ]:
            # Sanitize objects to store the finished workflow instance
            asyncio.ensure_future(self.storage.instances.insert(
                sanitize_workflow_exec(wflow.report())
            ))
            del self.running_workflows[exec_id]

        payload = {
            'type': event.data['type'],
            'data': event.data.get('content') or {},
            'source': source
        }

        # Is workflow begin, also send the full template.
        if event.data['type'] == WorkflowExecState.begin.value:
            payload['template'] = wflow.template

        await self.websocket.broadcast(payload)

    async def workflow_event(self, efrom, data):
        """
        New bus event received, trigger workflows if needed.
        """
        templates = {}
        # Retrieve full workflow templates
        wf_templates = self.engine.selector.select(efrom)
        for wftmpl in wf_templates:
            template = await self.storage.templates.get(
                wftmpl.uid,
                draft=False,
                with_metadata=True
            )
            templates[wftmpl.uid] = template[0]
        # Trigger workflows
        instances = await self.engine.data_received(data, efrom)
        for instance in instances:
            self.new_workflow(templates[instance.template.uid], instance)

    async def reload_from_storage(self):
        """
        Check mongo, retrieve and load all templates
        """
        self.storage = MongoStorage(**self.mongo_config)

        templates = await self.storage.templates.get_all(
            latest=True,
            with_metadata=False
        )

        for template in templates:
            try:
                await self.engine.load(WorkflowTemplate.from_dict(template))
            except Exception as exc:
                # Means a bad workflow is in database, report it
                reporting.exception(exc)
