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

"""cubicweb-celerytask views/forms/actions/components for web ui"""

import logging
import json

import six
from logilab.mtconverter import xml_escape


from cubicweb import tags
from cubicweb.view import EntityView
from cubicweb.predicates import is_instance, match_view, adaptable
from cubicweb.web.views import uicfg, tabs
from cubicweb.web.views.cwsources import LogTable, LogTableLayout
from cubicweb.web.views.json import JsonMixIn

_ = six.text_type
from cubes.celerytask import STATES


_pvs = uicfg.primaryview_section
_pvs.tag_attribute(('CeleryTask', 'task_name'), 'hidden')


class CeleryTaskTabbedPrimaryView(tabs.TabbedPrimaryView):
    """Tabbed primary view for CeleryTask"""
    __select__ = tabs.TabbedPrimaryView.__select__ & is_instance('CeleryTask')
    tabs = [
        _('celerytask.task_general_information'),
        _('celerytask.task_logs'),
    ]
    default_tab = 'celerytask.task_general_information'


class CeleryTaskPrimaryTab(tabs.PrimaryTab):
    """Main tab for CeleryTask"""
    __regid__ = 'celerytask.task_general_information'
    __select__ = EntityView.__select__ & is_instance('CeleryTask')

    def entity_call(self, entity):
        self._cw.add_js(('cubicweb.htmlhelpers.js', 'cubicweb.ajax.js',
                         'cubes.celerytask.js'))
        self._cw.add_onload('cw.celerytask.autorefreshprimary()')
        if not entity.cw_adapt_to('ICeleryTask').finished:
            entity.view('celerytask.task_progress_bar', w=self.w)
        super(CeleryTaskPrimaryTab, self).entity_call(entity)


class CeleryTaskLogs(tabs.TabsMixin, EntityView):
    """View for CeleryTask logs, only displayed if there are some"""
    __regid__ = 'celerytask.task_logs'
    __select__ = EntityView.__select__ & is_instance('CeleryTask')
    default_level = 'Debug'

    def entity_call(self, entity):
        logs = entity.cw_adapt_to('ICeleryTask').logs
        if logs:
            logs = xml_escape(logs).decode('utf-8', errors='ignore')
            self._cw.view('celerytask.task_logs.table',
                          pyvalue=log_to_table(logs), paginate=True,
                          default_level=self.default_level, w=self.w)


class CeleryTaskLogTableLayout(LogTableLayout):
    __select__ = match_view('celerytask.task_logs.table')


class CeleryTaskLogTable(LogTable):
    __regid__ = 'celerytask.task_logs.table'
    headers = [_('severity'), _('date'), _('time'), _('message')]


SEVERITY_LVL = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'FATAL': logging.FATAL,
}


def log_to_table(logs):
    rows = []
    for line in logs.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            severity, date, time, info = line.split(None, 3)
            severity = SEVERITY_LVL[severity]
            rows.append([severity, date, time, info])
        except (ValueError, KeyError):
            rows[-1][-1] += '\n' + line
    return rows


class CeleryTaskProgressBarView(EntityView):
    __select__ = EntityView.__select__ & adaptable('ICeleryTask')
    __regid__ = 'celerytask.task_progress_bar'

    def entity_call(self, entity, **kwargs):
        adapted = entity.cw_adapt_to('ICeleryTask')
        if not adapted.finished:
            self._cw.add_js(('cubicweb.htmlhelpers.js', 'cubicweb.ajax.js',
                             'cubes.celerytask.js'))
            self._cw.add_onload(
                'cw.celerytask.autorefreshprogress(%s, "%s");'
                % (entity.eid, adapted.state))
        progratio = adapted.progress
        progress = u'%.0f %%' % (100 * progratio)
        self.w(
            tags.tag('progress')(progress, min=u'0', max=u'1',
                                 value=unicode(progratio),
                                 id=u'js-cw-celerytask-%s' % entity.eid))


class CeleryTaskJsonView(JsonMixIn, EntityView):
    __select__ = EntityView.__select__ & adaptable('ICeleryTask')
    __regid__ = 'celerytask.jsonexport'

    def entity_call(self, entity, **kwargs):
        adapted = entity.cw_adapt_to('ICeleryTask')
        state = adapted.state
        if state == STATES.PENDING:
            progress = None
        elif adapted.finished:
            progress = 1
        else:
            progress = adapted.progress
        result = {'eid': entity.eid,
                  'task_id': adapted.task_id,
                  'task_name': adapted.task_name,
                  'state': state,
                  'progress': progress,
                  }
        self.wdata(result)


class CeleryTaskInContextView(EntityView):
    __regid__ = 'incontext'
    __select__ = EntityView.__select__ & adaptable('ICeleryTask')

    def entity_call(self, entity):
        adapted = entity.cw_adapt_to('ICeleryTask')
        state, finished = adapted.state or _('unknown state'), adapted.finished
        html = [tags.a(self._cw._(state),
                       klass='celerytask-%s' % state.lower(),
                       href=entity.absolute_url())]
        if not finished:
            self._cw.add_js(('cubicweb.htmlhelpers.js', 'cubicweb.ajax.js',
                             'cubes.celerytask.js'))
            self._cw.add_onload('cw.celerytask.setupincontext(%s, %s);'
                                % (entity.eid, json.dumps(state)))
            html.append(entity.view('celerytask.task_progress_bar', w=None))
        self.w(tags.div('\n'.join(html),
                        id='js-celerytask-incontext-%s' % entity.eid))
