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

import traceback

import celery
from celery.events import EventReceiver
from kombu import Connection as BrokerConnection

from cubicweb.toolsutils import Command
from cubicweb.server.serverconfig import ServerConfiguration
from cubicweb.cwctl import CWCTL


class CeleryMonitorCommand(Command):
    """Synchronize celery task statuses"""

    name = 'celery-monitor'
    arguments = '<instance>'
    min_args = max_args = 1
    options = (
        ('loglevel',
         {'short': 'l', 'type': 'choice', 'metavar': '<log level>',
          'default': 'info', 'choices': ('debug', 'info', 'warning', 'error')},
         ),
    )

    def run(self, args):
        from cubicweb import repoapi
        from cubicweb.cwctl import init_cmdline_log_threshold
        config = ServerConfiguration.config_for(args[0])
        config.global_set_option('log-file', None)
        config.log_format = '%(levelname)s %(name)s: %(message)s'
        init_cmdline_log_threshold(config, self['loglevel'])
        repo = repoapi.get_repository(config=config)
        repo.hm.call_hooks('server_maintenance', repo=repo)
        self.repo = repo
        with repo.internal_cnx() as cnx:
            self.on_monitor_start(cnx)
        self.celery_monitor()

    @staticmethod
    def on_monitor_start(cnx):
        for adapter in cnx.vreg['adapters']['ICeleryTask']:
            adapter.on_monitor_start(cnx)
        cnx.commit()

    def on_event(self, event):
        with self.repo.internal_cnx() as cnx:
            for adapter in cnx.vreg['adapters']['ICeleryTask']:
                adapter.on_event(cnx, event)
            cnx.commit()

    def celery_monitor(self):
        result_backend = celery.current_app.conf['CELERY_RESULT_BACKEND']
        while True:
            try:
                with BrokerConnection(result_backend) as conn:
                    recv = EventReceiver(
                        conn,
                        handlers={
                            'task-failed': self.on_event,
                            'task-succeeded': self.on_event,
                            'task-sent': self.on_event,
                            'task-received': self.on_event,
                            'task-revoked': self.on_event,
                            'task-started': self.on_event,
                            # '*': self.on_event,
                        })
                    recv.capture(limit=None, timeout=None)
            except (KeyboardInterrupt, SystemExit):
                traceback.print_exc()
                break


CWCTL.register(CeleryMonitorCommand)
