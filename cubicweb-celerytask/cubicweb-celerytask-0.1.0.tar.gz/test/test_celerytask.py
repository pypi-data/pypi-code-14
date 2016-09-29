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

"""cubicweb-celerytask automatic tests"""

import os
import sys
import multiprocessing
import time
import unittest

import redis
import celery
import celery.result
from celery.bin.worker import worker as celery_worker

from cubicweb.devtools import testlib

from cubes.celerytask.entities import (start_async_task, StartCeleryTaskOp,
                                       run_all_tasks)
from cubes.celerytask.ccplugin import CeleryMonitorCommand

import cw_celerytask_helpers.redislogger as loghelper


class CeleryTaskTC(testlib.CubicWebTC):

    @classmethod
    def setUpClass(cls):
        super(CeleryTaskTC, cls).setUpClass()
        REDIS_URL = os.environ.get('PIFPAF_REDIS_URL',
                                   'redis://localhost:6379/1')
        redis_client = redis.Redis.from_url(REDIS_URL)
        redis_client.flushall()
        task_module_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'tasks')
        sys.path.insert(0, task_module_path)
        conf = celery.current_app.conf
        conf.BROKER_URL = REDIS_URL
        conf.CELERY_RESULT_BACKEND = REDIS_URL
        conf.CUBICWEB_CELERYTASK_REDIS_URL = REDIS_URL
        conf.CELERY_ALWAYS_EAGER = False
        conf.CELERY_TASK_SERIALIZER = 'json'
        conf.CELERY_RESULT_SERIALIZER = 'json'
        conf.CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
        conf.CELERY_IMPORTS = ('cw_celerytask_helpers.redislogger', 'tasks')
        import tasks  # noqa
        cls.worker = multiprocessing.Process(target=cls.start_worker)
        cls.worker.start()

    @classmethod
    def tearDownClass(cls):
        super(CeleryTaskTC, cls).tearDownClass()
        cls.worker.terminate()
        cls.worker.join()

    @staticmethod
    def start_worker():
        app = celery.current_app
        worker = celery_worker(app)
        worker.run_from_argv("worker", ['-P', 'solo', '-c', '1', '-l', 'info'])

    def setUp(self):
        super(CeleryTaskTC, self).setUp()
        conf = celery.current_app.conf
        conf.CELERY_ALWAYS_EAGER = False

    def wait_async_task(self, cnx, task_id, timeout=5):
        result = celery.result.AsyncResult(task_id)
        start = time.time()
        while abs(time.time() - start) < timeout:
            if result.ready():
                CeleryMonitorCommand.on_monitor_start(cnx)
                return result
            if not self.worker.is_alive():
                # will be joined in tearDown
                raise RuntimeError("Celery worker terminated")
            time.sleep(.1)
        raise RuntimeError("Timeout")

    def test_success_task(self):
        with self.admin_access.repo_cnx() as cnx:
            cwtask_eid = start_async_task(cnx, 'success', 42).eid
            cnx.commit()
            cwtask = cnx.entity_from_eid(cwtask_eid)
            run_all_tasks()
            self.wait_async_task(cnx, cwtask.task_id)
            result = cwtask.cw_adapt_to('ICeleryTask').result
            self.assertEqual(result.get(), 42)
            wf = cwtask.cw_adapt_to('IWorkflowable')
            self.assertEqual(wf.state, 'done')

    def test_fail_task(self):
        with self.admin_access.repo_cnx() as cnx:
            cwtask_eid = start_async_task(cnx, 'fail').eid
            cnx.commit()
            run_all_tasks()
            cwtask = cnx.entity_from_eid(cwtask_eid)
            self.wait_async_task(cnx, cwtask.task_id)
            result = cwtask.cw_adapt_to('ICeleryTask').result
            tb = result.traceback
            self.assertTrue(result.failed())
            self.assertTrue(tb.startswith('Traceback (most recent call last)'))
            self.assertTrue(tb.endswith('RuntimeError: fail\n'))
            wf = cwtask.cw_adapt_to('IWorkflowable')
            self.assertEqual(wf.state, 'failed')

    def test_api(self):
        with self.admin_access.repo_cnx() as cnx:
            run = cnx.create_entity('Run', name=u'success', i=12)
            cnx.commit()

            run = cnx.entity_from_eid(run.eid)
            self.assertIsNone(run.result)
            run.cw_adapt_to('IWorkflowable').fire_transition('start')
            cnx.commit()
            run_all_tasks()

            run = cnx.entity_from_eid(run.eid)
            self.wait_async_task(cnx, run.task_id)
            cnx.commit()
            self.assertEqual(run.cw_adapt_to('IWorkflowable').state, 'done')
            self.assertEqual(run.result, 12)

    def test_start_celerytask_op(self):
        with self.admin_access.repo_cnx() as cnx:
            # Task must run even if there is no data on current transaction
            task = celery.signature("success", kwargs={"n": 10})
            task_id = task.freeze().task_id
            cnx.transaction_data['celerytask'] = {42: task}
            StartCeleryTaskOp.get_instance(cnx).add_data(42)
            cnx.commit()
            run_all_tasks()
            result = self.wait_async_task(cnx, task_id)
            self.assertEqual(result.get(), 10)

    def test_logs(self):
        with self.admin_access.repo_cnx() as cnx:
            cwtask_eid = start_async_task(cnx, 'log').eid
            cnx.commit()
            run_all_tasks()
            cwtask = cnx.entity_from_eid(cwtask_eid)
            self.wait_async_task(cnx, cwtask.task_id)

            # logs should be flushed from redis to database
            redis_logs = loghelper.get_task_logs(cwtask.task_id)
            self.assertIsNone(redis_logs)
            cwtask.task_logs.seek(0)
            task_logs = cwtask.task_logs.read()
            logs = cwtask.cw_adapt_to('ICeleryTask').logs
            self.assertEqual(task_logs, logs)

            self.assertIn(b'out should be in logs', logs)
            self.assertIn(b'err should be in logs', logs)
            self.assertIn(b'cw warning should be in logs', logs)
            for name in (b'cw', b'celery'):
                for key in (b'error', b'critical', b'exception'):
                    self.assertIn(name + b' ' + key + b' should be in logs',
                                  logs)
            self.assertIn(b'cw critical should be in logs', logs)
            self.assertNotIn(b'should not be in logs', logs)
            self.assertIn(b'raise Exception("oops")', logs)

    @unittest.skipIf(celery.VERSION.major == 3, "not supported with celery 3")
    def test_workflow_chain(self):
        with self.admin_access.repo_cnx() as cnx:
            s = celery.signature
            task = celery.chain(s("add", (2, 2)), s("add", (4,)))
            cwtask = start_async_task(cnx, task)
            cnx.commit()
            run_all_tasks()
            result = self.wait_async_task(cnx, cwtask.task_id)
            self.assertEqual(result.get(), 8)

            children = cwtask.reverse_parent_task
            self.assertEqual(len(children), 1)
            result = children[0].cw_adapt_to('ICeleryTask').result
            self.assertEqual(result.get(), 4)

    def test_workflow_group(self):
        with self.admin_access.repo_cnx() as cnx:
            s = celery.signature
            task = celery.group(s("add", (2, 2)), s("add", (4, 4)))
            cwtask = start_async_task(cnx, task)
            cnx.commit()
            self.assertEqual(cwtask.task_name, u'celery.group')
            run_all_tasks()
            result = self.wait_async_task(cnx, cwtask.task_id)
            # Group task return the latest subtask
            self.assertEqual(result.get(), 8)

            children = cwtask.reverse_parent_task
            self.assertEqual(len(children), 1)
            self.assertEqual(children[0].task_name, u'add')
            task_id = children[0].cw_adapt_to('ICeleryTask').task_id
            result = self.wait_async_task(cnx, task_id)
            self.assertEqual(result.get(), 4)

    def test_workflow_chord(self):
        with self.admin_access.repo_cnx() as cnx:
            s = celery.signature
            task = celery.chord([s("success", (i,)) for i in range(10)],
                                s("tsum", []))
            cwtask = start_async_task(cnx, task)
            cnx.commit()
            self.assertEqual(cwtask.task_name, u'celery.chord')
            run_all_tasks()
            result = self.wait_async_task(cnx, cwtask.task_id)
            self.assertEqual(result.get(), 45)

            children = cwtask.reverse_parent_task
            self.assertEqual([child.task_name for child in children],
                             [u'success'] * 10)
            self.assertCountEqual(
                [t.cw_adapt_to('ICeleryTask').result.get() for t in children],
                range(10))


if __name__ == '__main__':
    from unittest import main
    main()
