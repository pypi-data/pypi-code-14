#!/usr/bin/env python
# coding: utf-8

from six.moves.urllib import parse

try:
    import simplejson as json
except ImportError:
    import json

from opsviewclient import base


class ServiceGroup(base.Resource):

    def __repr__(self):
        return '<ServiceGroup: %s>' % self.name

    def update(self, **kwds):
        return self.manager.update(self, **kwds)

    def delete(self):
        return self.manager.delete(self)


class ServiceGroupManager(base.Manager):

    resource_class = ServiceGroup

    def get(self, group):
        return self._get('/config/servicegroup/%s' % base.get_id(group))

    def update(self, group, **kwds):
        body = group._info
        body.update(kwds)
        return self._update('/config/servicegroup/%s' % base.get_id(group),
                            body=body)

    def create(self, name, servicechecks=None):
        body = {'name': name}

        if servicechecks is not None:
            if not isinstance(servicechecks, list):
                servicechecks = [servicechecks]

            body['servicechecks'] = [base.nameref(s) for s in servicechecks]

        return self._create('/config/servicegroup', body=body)

    def delete(self, group):
        return self._delete('/config/servicegroup/%s' % base.get_id(group))

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

        return self._list('/config/servicegroup%s' % qstring)
