#!/usr/bin/env python
# coding: utf-8

from six.moves.urllib import parse

try:
    import simplejson as json
except ImportError:
    import json

from opsviewclient import base


class Host(base.Resource):

    def __repr__(self):
        return '<Host: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)

    def update(self, **kwds):
        return self.manager.update(self, **kwds)


class HostManager(base.Manager):

    resource_class = Host

    def get(self, host):
        return self._get('/config/host/%s' % base.get_id(host))

    def delete(self, host):
        return self._delete('/config/host/%s' % base.get_id(host))

    def list(self, rows='all', page=None, cols=None, order=None,
             search=None, in_use=None, is_parent=None, include_ms=None,
             include_encrypted=None, monitored_by_id=None, template_id=None,
             template_name=None, bsm_component_id=None, with_snmpifs=False,
             kwds=None):

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
        if is_parent is not None:
            qparams['is_parent'] = 1 if is_parent else 0
        if include_ms is not None:
            qparams['include_ms'] = 1 if include_ms else 0
        if include_encrypted is not None:
            qparams['include_encrypted'] = 1 if include_encrypted else 0
        if monitored_by_id:
            qparams['s.monitored_by.id'] = int(monitored_by_id)
        if template_id:
            qparams['s.hosttemplates.id'] = int(template_id)
        if template_name:
            qparams['s.hosttemplates.name'] = str(template_name)
        if bsm_component_id:
            qparams['s.business_components.id'] = int(bsm_component_id)
        if with_snmpifs:
            if 'cols' in qparams:
                qparams['cols'] += ',+snmpinterfaces'
            else:
                qparams['cols'] = '+snmpinterfaces'

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/host%s' % qstring)

    def update(self, host, params=None, **kwds):
        body = host._info
        body.update(kwds)
        return self._update('/config/host/%s' % base.get_id(host),
                            body=body, params=params)

    def create_many(self, _list, params=None):
        if isinstance(_list, list):
            _list = {'list': _list}

        return self._create('/config/host', body=_list, params=params,
                            return_raw=True)

    def create(self, name, address, alias=None, check_attempts=None,
               check_command=None, check_interval=None, check_period=None,
               enable_snmp=None, event_handler_always_exec=None,
               event_handler=None, flap_detection_enabled=None,
               hostattributes=None, hostgroup=None, hosttemplates=None,
               icon=None, keywords=None, monitored_by=None,
               notification_interval=None, notification_options=None,
               notification_period=None, other_addresses=None, parents=None,
               rancid_autoenable=None, rancid_connection_type=None,
               rancid_username=None, rancid_vendor=None,
               retry_check_interval=None, servicechecks=None,
               snmp_extended_throughput_data=None, snmp_max_msg_size=None,
               snmp_port=None, snmp_version=None, snmpv3_authprotocol=None,
               snmpv3_privprotocol=None, snmpv3_username=None,
               tidy_ifdescr_level=None, use_rancid=None, params=None,
               body_only=False):

        body = {
            'name': name,
            'ip': address,
        }

        if alias is not None:
            body['alias'] = alias

        if check_attempts is not None:
            body['check_attempts'] = base.fmt_str(check_attempts)

        if check_command is not None:
            body['check_command'] = base.nameref(check_command)

        if check_interval is not None:
            body['check_interval'] = base.fmt_str(check_interval)

        if check_period is not None:
            body['check_period'] = base.nameref(check_period)

        if enable_snmp is not None:
            body['enable_snmp'] = base.fmt_str(enable_snmp)

        if event_handler is not None:
            body['event_handler'] = event_handler

        if event_handler_always_exec is not None:
            body['event_handler_always_exec'] = \
                base.fmt_str(event_handler_always_exec)

        if flap_detection_enabled is not None:
            body['flap_detection_enabled'] = \
                base.fmt_str(flap_detection_enabled)

        if hostattributes is not None:
            if not isinstance(hostattributes, list):
                hostattributes = [hostattributes]

            body['hostattributes'] = hostattributes

        if hostgroup is not None:
            body['hostgroup'] = base.nameref(hostgroup)

        if hosttemplates is not None:
            if not isinstance(hosttemplates, list):
                hosttemplates = [hosttemplates]

            body['hosttemplates'] = []
            for template in hosttemplates:
                body['hosttemplates'].append(base.nameref(template))

        if icon is not None:
            if isinstance(icon, str):
                key = 'path' if icon[0] == '/' else 'name'

                body['icon'] = {key: icon}
            else:
                body['icon'] = icon

        if keywords is not None:
            if not isinstance(keywords, list):
                keywords = [keywords]

            body['keywords'] = []
            for keyword in keywords:
                body['keywords'].append(base.nameref(keyword))

        if monitored_by is not None:
            body['monitored_by'] = base.nameref(monitored_by)

        if notification_interval is not None:
            body['notification_interval'] = base.fmt_str(notification_interval)

        if notification_options is not None:
            body['notification_interval'] = notification_options

        if notification_period is not None:
            body['notification_period'] = base.nameref(notification_period)

        if other_addresses is not None:
            if isinstance(other_addresses, list):
                other_addresses = ','.join(other_addresses)

            body['other_addresses'] = other_addresses

        if parents is not None:
            if not isinstance(parents, list):
                parents = [parents]

            body['parents'] = []
            for parent in parents:
                body['parents'].append(base.nameref(parent))

        if rancid_autoenable is not None:
            body['rancid_autoenable'] = base.fmt_str(rancid_autoenable)

        if rancid_connection_type is not None:
            body['rancid_connection_type'] = rancid_connection_type

        if rancid_username is not None:
            body['rancid_username'] = rancid_username

        if rancid_vendor is not None:
            body['rancid_vendor'] = rancid_vendor

        if retry_check_interval is not None:
            body['retry_check_interval'] = base.fmt_str(retry_check_interval)

        if servicechecks is not None:
            if not isinstance(servicechecks, list):
                servicechecks = [servicechecks]

            body['servicechecks'] = []
            for check in servicechecks:
                if isinstance(check, str):
                    body['servicechecks'].append(base.nameref(check))
                else:
                    body['servicechecks'].append(check)

        if snmp_extended_throughput_data is not None:
            body['snmp_extended_throughput_data'] = \
                base.fmt_str(snmp_extended_throughput_data)

        if snmp_max_msg_size is not None:
            body['snmp_max_msg_size'] = base.fmt_str(snmp_max_msg_size)

        if snmp_port is not None:
            body['snmp_port'] = base.fmt_str(snmp_port)

        if snmp_version is not None:
            body['snmp_version'] = base.fmt_str(snmp_version)

        if snmpv3_authprotocol is not None:
            body['snmpv3_authprotocol'] = snmpv3_authprotocol

        if snmpv3_privprotocol is not None:
            body['snmpv3_privprotocol'] = snmpv3_privprotocol

        if snmpv3_username is not None:
            body['snmpv3_username'] = snmpv3_username

        if tidy_ifdescr_level is not None:
            body['tidy_ifdescr_level'] = base.fmt_str(tidy_ifdescr_level)

        if use_rancid is not None:
            body['use_rancid'] = base.fmt_str(use_rancid)

        if body_only:
            return body

        return self._create('/config/host', body=body, params=params)
