# -*- coding: utf-8 -*-
# copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-celerytask entity's classes"""
import six

import celery
from celery.result import AsyncResult

from cubicweb.entities import AnyEntity, fetch_config
from cubicweb.view import EntityAdapter
from cubicweb.predicates import is_instance
from cubicweb.server.hook import DataOperationMixIn, Operation

from cw_celerytask_helpers import redislogger as loghelper

from cubes.celerytask import STATES, FINAL_STATES


_TEST_TASKS = {}


def get_tasks():
    """Return tasks to be run (for use in cubicweb test mode)"""
    return _TEST_TASKS


def run_all_tasks():
    """Run all pending tasks (for use in cubicweb test mode)"""
    results = {}
    for task_eid, task in _TEST_TASKS.items():
        results[task_eid] = task.delay()
    return results


def start_async_task(cnx, task, *args, **kwargs):
    """Create and start a new task

    `task` can be either a task name, a task object or a task signature
    """
    task_name = six.text_type(celery.signature(task).task)
    entity = cnx.create_entity('CeleryTask', task_name=task_name)
    entity.cw_adapt_to('ICeleryTask').start(task, *args, **kwargs)
    return entity


def task_in_backend(task_id):
    app = celery.current_app
    if app.conf.CELERY_ALWAYS_EAGER:
        return False
    else:
        backend = app.backend
        return backend.get(backend.get_key_for_task(task_id)) is not None


class StartCeleryTaskOp(DataOperationMixIn, Operation):

    def postcommit_event(self):
        global _TEST_TASKS
        if self.cnx.vreg.config.mode == 'test':
            # In test mode, task should run explicitly with run_all_tasks()
            _TEST_TASKS = self.cnx.transaction_data.get('celerytask', {})
        else:
            for eid in self.get_data():
                task = self.cnx.transaction_data.get('celerytask', {}).get(eid)
                if task is not None:
                    task.delay()


class CeleryTask(AnyEntity):
    __regid__ = 'CeleryTask'
    fetch_attrs, cw_fetch_order = fetch_config(('task_name',))

    def dc_title(self):
        return self.task_name


class ICeleryTask(EntityAdapter):
    __regid__ = 'ICeleryTask'
    __abstract__ = True

    def start(self, name, *args, **kwargs):
        eid = self.entity.eid
        task = self.get_task(name, *args, **kwargs)
        self._cw.transaction_data.setdefault('celerytask', {})[eid] = task
        StartCeleryTaskOp.get_instance(self._cw).add_data(eid)

    def get_task(self, name, *args, **kwargs):
        """Should return a celery task / signature or None

        This method run in a precommit event
        """
        return celery.signature(name, args=args, kwargs=kwargs)

    @staticmethod
    def on_event(cnx, event):
        """Triggered by celery-monitor"""
        pass

    @staticmethod
    def on_monitor_start(cnx):
        """Triggered by celery-monitor"""
        pass

    @property
    def task_id(self):
        raise NotImplementedError

    @property
    def task_name(self):
        raise NotImplementedError

    @property
    def logs(self):
        return loghelper.get_task_logs(self.task_id) or b''

    @property
    def result(self):
        return AsyncResult(self.task_id)

    @property
    def progress(self):
        if celery.current_app.conf.CELERY_ALWAYS_EAGER:
            return 1.
        result = self.result
        if result.info and 'progress' in result.info:
            return result.info['progress']
        elif result.state == STATES.SUCCESS:
            return 1.
        else:
            return 0.

    @property
    def state(self):
        return self.result.state

    @property
    def finished(self):
        return self.state in FINAL_STATES


def get_task_id(task):

    result = task.freeze()
    if hasattr(result, 'task_id'):
        return result.task_id
    else:
        # Group
        return get_task_id(task.tasks[-1])


class CeleryTaskAdapter(ICeleryTask):
    """Base adapter that store task call args in the transaction"""

    __select__ = ICeleryTask.__select__ & is_instance('CeleryTask')

    tr_map = {
        'task-failed': 'fail',
        'task-succeeded': 'finish',
        'task-received': 'enqueue',
        'task-started': 'start',
        'task-revoked': 'fail',
    }

    def attach_task(self, task, seen, parent=None):
        task_id = six.text_type(get_task_id(task))
        if parent is None:
            parent = self.entity
        if self.entity.task_id is None:
            self.entity.cw_set(task_id=task_id)
        elif task_id not in seen:
            task_name = six.text_type(task.task)
            parent = self._cw.create_entity('CeleryTask',
                                            task_id=six.text_type(task_id),
                                            task_name=task_name,
                                            parent_task=parent)
        seen.add(task_id)
        if hasattr(task, 'body'):
            self.attach_task(task.body, seen, parent)
        if hasattr(task, 'tasks'):
            for subtask in task.tasks:
                self.attach_task(subtask, seen, parent)

    def get_task(self, name, *args, **kwargs):
        task = super(CeleryTaskAdapter, self).get_task(
            name, *args, **kwargs)
        self.attach_task(task, set())
        return task

    @property
    def task_id(self):
        return self.entity.task_id

    @property
    def task_name(self):
        return self.entity.task_name

    @staticmethod
    def on_event(cnx, event):
        tr_map = CeleryTaskAdapter.tr_map
        if event['type'] in tr_map:
            entity = cnx.find('CeleryTask', task_id=event['uuid']).one()
            transition = tr_map[event['type']]
            entity.cw_adapt_to('IWorkflowable').fire_transition(
                transition, event.get('exception'))
            CeleryTaskAdapter.info('<CeleryTask %s (task_id %s)> %s',
                                   entity.eid, entity.task_id, transition)

    @staticmethod
    def on_monitor_start(cnx):
        for task_eid, task_id in cnx.execute((
            'Any T, TID WHERE '
            'T is CeleryTask, T task_id TID, T in_state S, '
            'S name in ("waiting", "queued", "running")'
        )):
            result = AsyncResult(task_id)
            transition = {
                STATES.SUCCESS: 'finish',
                STATES.FAILURE: 'fail',
                STATES.STARTED: 'running',
            }.get(result.state)
            if transition is not None:
                wf = cnx.entity_from_eid(task_eid).cw_adapt_to('IWorkflowable')
                wf.fire_transition(transition, result.traceback)
                CeleryTaskAdapter.info('<CeleryTask %s (task_id %s)> %s',
                                       task_eid, task_id, transition)

    @property
    def logs(self):
        task_logs = self.entity.task_logs
        if task_logs is not None:
            task_logs.seek(0)
            return task_logs.read()
        else:
            return super(CeleryTaskAdapter, self).logs

    @property
    def state(self):
        if task_in_backend(self.task_id):
            return super(CeleryTaskAdapter, self).state
        db_state = self.entity.cw_adapt_to('IWorkflowable').state
        state_map = {'done': STATES.SUCCESS, 'failed': STATES.FAILURE}
        return state_map.get(db_state, STATES.PENDING)


def registration_callback(vreg):
    vreg.register_all(six.itervalues(globals()), __name__)
    if vreg.config.mode == 'test':
        conf = celery.current_app.conf
        conf['CELERY_ALWAYS_EAGER'] = True
        conf['CELERY_EAGER_PROPAGATES_EXCEPTIONS'] = True
