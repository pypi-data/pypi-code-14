#!/usr/bin/env python
# coding: utf-8

from six.moves.urllib import parse

try:
    import simplejson as json
except ImportError:
    import json

from opsviewclient import base


class HostTemplate(base.Resource):

    def __repr__(self):
        return '<HostTemplate: %s>' % self.name

    def update(self, **kwds):
        return self.manager.update(self, **kwds)

    def delete(self):
        return self.manager.delete(self)


class HostTemplateManager(base.Manager):

    resource_class = HostTemplate

    def get(self, template):
        return self._get('/config/hosttemplate/%s' % base.get_id(template))

    def create(self, name, description=None, hosts=None, managementurls=None,
               servicechecks=None):

        body = {'name': name}

        if description is not None:
            body['description'] = description

        if hosts is not None:
            if not isinstance(hosts, list):
                hosts = [hosts]

            body['hosts'] = []
            for host in hosts:
                body['hosts'].append(base.nameref(host))

        if managementurls is not None:
            if not isinstance(managementurls, list):
                managementurls = [managementurls]

            body['managementurls'] = []
            for url in managementurls:
                body['managementurls'].append(base.nameref(url))

        if servicechecks is not None:
            if not isinstance(servicechecks, list):
                servicechecks = [servicechecks]

            body['servicechecks'] = []
            for check in servicechecks:
                body['servicechecks'].append(base.nameref(check))

        return self._create('/config/hosttemplate', body=body)

    def update(self, template, **kwds):
        body = template._info
        body.update(kwds)
        self._update('/config/hosttemplate/%s' % base.get_id(template),
                     body=body)

    def delete(self, template):
        return self._delete('/config/hosttemplate/%s' % base.get_id(template))

    def list(self, rows='all', page=None, cols=None, order=None, search=None,
             in_use=None, kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/hosttemplate%s' % qstring)
