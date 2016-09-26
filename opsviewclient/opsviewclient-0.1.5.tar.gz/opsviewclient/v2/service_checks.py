#!/usr/bin/env python
# coding: utf-8

from six.moves.urllib import parse

try:
    import simplejson as json
except ImportError:
    import json

from opsviewclient import base


class ServiceCheck(base.Resource):

    def __repr__(self):
        return '<ServiceCheck: %s>' % self.name

    def update(self, **kwds):
        return self.manager.update(self, **kwds)

    def delete(self):
        return self.manager.delete(self)


class ServiceCheckManager(base.Manager):

    resource_class = ServiceCheck

    def get(self, check):
        return self._get('/config/servicecheck/%s' % base.get_id(check))

    def delete(self, check):
        return self._delete('/config/servicecheck/%s' % base.get_id(check))

    def update(self, check, **kwds):
        body = check._info
        body.update(kwds)
        return self._update('/config/servicecheck/%s' % base.get_id(check),
                            body=body)

    def create(self, name, plugin, servicegroup,
               checktype='Active Plugin', args=None,
               notification_options='w,c,r,u,f',
               retry_check_interval=60,
               sensitive_arguments=True,
               check_interval=300,
               invertresults=False,
               stale_threshold_seconds=3600,
               check_attempts=3,
               alert_from_failure=None,
               attribute=None,
               calculated_rate=None,
               cascaded_from=None,
               check_freshness=None,
               check_period=None,
               critical_comparison=None,
               critical_value=None,
               dependencies=None,
               description=None,
               event_handler=None,
               event_handler_always_exec=None,
               flap_detection_enabled=None,
               freshness_type=None, hosts=None,
               hosttemplates=None,
               keywords=None,
               label=None,
               markdown_filter=None,
               notification_interval=None,
               notification_period=None,
               oid=None,
               snmptraprules=None, stale_state=None,
               stale_text=None,
               stalking=None,
               volatile=None,
               warning_comparison=None,
               warning_value=None
               ):

        body = {
            'name': name,
            'plugin': base.nameref(plugin)
        }

        if alert_from_failure is not None:
            body['alert_from_failure'] = base.fmt_str(alert_from_failure)

        if args is not None:
            body['args'] = args

        if attribute is not None:
            body['attribute'] = base.nameref(attribute)

        if calculated_rate is not None:
            body['calculated_rate'] = calculated_rate

        if cascaded_from is not None:
            body['cascaded_from'] = base.nameref(cascaded_from)

        if check_attempts is not None:
            body['check_attempts'] = base.fmt_str(check_attempts)

        if check_freshness is not None:
            body['check_freshness'] = base.fmt_str(check_freshness)

        if check_interval is not None:
            body['check_interval'] = base.fmt_str(check_interval)

        if check_period is not None:
            body['check_period'] = base.nameref(check_period)

        if checktype is not None:
            body['checktype'] = base.nameref(checktype)

        # TODO:handle these
        if critical_comparison is not None:
            body['critical_comparison'] = critical_comparison
        if critical_value is not None:
            body['critical_value'] = critical_value

        if dependencies is not None:
            if not isinstance(dependencies, list):
                dependencies = [dependencies]

            body['dependencies'] = [base.nameref(d) for d in dependencies]

        if description is not None:
            body['description'] = description

        if event_handler is not None:
            body['event_handler'] = event_handler

        if event_handler_always_exec is not None:
            body['event_handler_always_exec'] = \
                base.fmt_str(event_handler_always_exec)

        if flap_detection_enabled is not None:
            body['flap_detection_enabled'] = \
                base.fmt_str(flap_detection_enabled)

        if freshness_type is not None:
            body['freshness_type'] = freshness_type

        if hosts is not None:
            if not isinstance(hosts, list):
                hosts = [hosts]

            body['hosts'] = [base.nameref(h) for h in hosts]

        if hosttemplates is not None:
            if not isinstance(hosttemplates, list):
                hosttemplates = [hosttemplates]

            body['hosttemplates'] = [base.nameref(h) for h in hosttemplates]

        if invertresults is not None:
            body['invertresults'] = base.fmt_str(invertresults)

        if keywords is not None:
            if not isinstance(keywords, list):
                keywords = [keywords]

            body['keywords'] = [base.nameref(k) for k in keywords]

        # TODO:handle this
        if label is not None:
            body['label'] = label

        if markdown_filter is not None:
            body['markdown_filter'] = base.fmt_str(markdown_filter)

        if notification_interval is not None:
            body['notification_interval'] = base.fmt_str(notification_interval)

        if notification_options is not None:
            body['notification_options'] = notification_options

        if notification_period is not None:
            body['notification_period'] = base.nameref(notification_period)

        # TODO:handle this
        if oid is not None:
            body['oid'] = oid

        if retry_check_interval is not None:
            body['retry_check_interval'] = base.fmt_str(retry_check_interval)

        if sensitive_arguments is not None:
            body['sensitive_arguments'] = base.fmt_str(sensitive_arguments)

        if servicegroup is not None:
            body['servicegroup'] = base.nameref(servicegroup)

        # TODO:handle this
        if snmptraprules is not None:
            body['snmptraprules'] = [base.nameref(s) for s in snmptraprules]

        if stale_state is not None:
            body['stale_state'] = base.fmt_str(stale_state)

        if stale_text is not None:
            body['stale_text'] = stale_text

        if stale_threshold_seconds is not None:
            body['stale_threshold_seconds'] = \
                base.fmt_str(stale_threshold_seconds)

        if stalking is not None:
            body['stalking'] = base.fmt_str(stalking)

        if volatile is not None:
            body['volatile'] = base.fmt_str(volatile)

        # TODO:handle this
        if warning_comparison is not None:
            body['warning_comparison'] = warning_comparison
        if warning_value is not None:
            body['warning_value'] = warning_value

        return self._create('/config/servicecheck', body=body)

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

        return self._list('/config/servicecheck%s' % qstring)
