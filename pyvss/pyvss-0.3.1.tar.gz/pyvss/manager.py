#!/usr/bin/env python

"""
This module simply sends request to the EIS RESTful API,
and returns their response as a dict.
"""
import os
import requests
from pyvss import __version__
from time import sleep
import json as json_module
from requests.auth import HTTPBasicAuth

API_ENDPOINT = 'https://vss-api.eis.utoronto.ca:8001/v2'
TOKEN_ENDPOINT = 'https://vss-api.eis.utoronto.ca:8001/auth/request-token'


class VssError(RuntimeError):
    pass


class VssManager(object):
    def __init__(self, tk):
        self.api_endpoint = API_ENDPOINT
        self.api_token = tk

    def get_token(self):
        username = os.environ.get('VSS_API_USER')
        password = os.environ.get('VSS_API_USER_PASS')
        tk_request = self.request_v2(TOKEN_ENDPOINT,
                                     method='POST',
                                     auth=HTTPBasicAuth(username, password))
        if tk_request.get('token'):
            self.api_token = tk_request.get('token')
            return self.api_token
        else:
            raise VssError('Could not generate token')

    # User Management methods
    def get_user_roles(self):
        json = self.request_v2('/user/role', method='GET')
        return json.get('data')

    def get_user_token(self, token_id):
        json = self.request_v2('/user/token/' + str(token_id),
                               method='GET')
        return json.get('data')

    def disable_user_token(self, token_id):
        json = self.request_v2('/user/token/' + str(token_id),
                               method='PUT')
        return json

    def get_user_tokens(self, **kwargs):
        json = self.request_v2('/user/token', params=kwargs,
                               method='GET')
        return json

    def delete_user_token(self, token_id):
        json = self.request_v2('/user/token/' + str(token_id),
                               method='DELETE')
        return json

    def get_user_email_settings(self):
        json = self.request_v2('/user/setting/email', method='GET')
        return json.get('data')

    def disable_user_email(self):
        json = self.update_user_email_settings(attribute='none',
                                               value=True)
        return json

    def enable_user_email(self):
        json = self.update_user_email_settings(attribute='all',
                                               value=True)
        return json

    def enable_user_email_error(self):
        json = self.update_user_email_settings(attribute='error',
                                               value=True)
        return json

    def update_user_email_settings(self, attribute, value):
        json_payload = dict(attribute=attribute, value=value)
        json = self.request_v2('/user/setting/email', method='PUT',
                               payload=json_payload)
        json.update(self.get_user_email_settings())
        return json

    def whoami(self):
        json = self.request_v2('/user')
        return json.get('data')

    # Operating systems
    def get_os(self, **kwargs):
        json = self.request_v2('/os', params=kwargs, method='GET')
        return json.get('data')

    # inventory management
    def create_inventory_file(self, props=None):
        props = ['Uuid'] if not props else props.split(',')
        json_payload = {'properties': props}
        json = self.request_v2('/inventory', payload=json_payload,
                               method='POST')
        return json.get('data')

    # Request management
    def get_requests(self, **kwargs):
        json = self.request_v2('/request', params=kwargs)
        return json.get('data')

    # Domain management
    def get_domains(self, **kwargs):
        json = self.request_v2('/domain', params=kwargs)
        return json.get('data')

    def get_domain(self, moref, **kwargs):
        json = self.request_v2('/domain/' + moref, params=kwargs)
        return json.get('data')

    def get_vms_by_domain(self, domain_moref):
        json = self.get_domain(domain_moref, summary=1)
        return json.get('vms')

    def get_vms_by_network(self, network_moref):
        json = self.get_network(network_moref, summary=1)
        return json.get('vms')

    # Image Management
    def get_images(self, **kwargs):
        json = self.request_v2('/image', params=kwargs)
        return json.get('data')

    # ISO Management
    def get_isos(self, **kwargs):
        json = self.request_v2('/iso', params=kwargs)
        return json.get('data')

    # Network Management
    def get_networks(self, **kwargs):
        json = self.request_v2('/network', params=kwargs)
        return json.get('data')

    def get_network(self, moref, **kwargs):
        json = self.request_v2('/network/' + moref, params=kwargs)
        return json.get('data')

    # Folder Management
    def get_folders(self, **kwargs):
        json = self.request_v2('/folder', params=kwargs)
        return json.get('data')

    def get_folder(self, moref):
        json = self.request_v2('/folder/' + moref)
        return json.get('data')

    def create_folder(self, moref, name):
        json_payload = dict(name=name)
        json = self.request_v2('/folder/' + moref,
                               payload=json_payload,
                               method='POST')
        return json.get('data')

    def move_folder(self, moref, new_moref):
        json_payload = dict(attribute='parent', value=new_moref)
        json = self.request_v2('/folder/' + moref,
                               payload=json_payload,
                               method='PUT')
        return json.get('data')

    def rename_folder(self, moref, name, **kwargs):
        json_payload = dict(attribute='name', value=name)
        json_payload.update(kwargs)
        json = self.request_v2('/folder/' + moref,
                               payload=json_payload,
                               method='PUT')
        return json.get('data')

    # Virtual Machine Management
    def get_templates(self, **kwargs):
        json = self.request_v2('/template', params=kwargs)
        return json.get('data')

    def get_vms(self, **kwargs):
        json = self.request_v2('/vm', params=kwargs)
        return json.get('data')

    def get_vm(self, uuid, **kwargs):
        json = self.request_v2('/vm/' + uuid, params=kwargs)
        return json.get('data')

    def get_vm_name(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/name')
        return json.get('data')

    def get_vm_state(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/state')
        return json.get('data')

    def update_vm_state(self, uuid, state, **kwargs):
        json_payload = dict(value=state)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/' + uuid + '/state',
                               method='PUT',
                               payload=json_payload)
        return json.get('data')

    def get_vm_domain(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/domain')
        return json.get('data')

    def update_vm_domain(self, uuid, value, power_on=False, **kwargs):
        json_payload = dict(value=value, poweron=power_on)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/' + uuid + '/domain', method='PUT',
                               payload=json_payload)
        return json.get('data')

    # Virtual Machine Configuration
    def get_vm_boot(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/boot')
        return json.get('data')

    def update_vm_boot_bios(self, uuid, boot_bios, **kwargs):
        json = self.update_vm_boot(uuid, attribute='bootbios',
                                   value=boot_bios, **kwargs)
        return json

    def update_vm_boot_delay(self, uuid, boot_delay_ms, **kwargs):
        json = self.update_vm_boot(uuid, attribute='bootdelay',
                                   value=boot_delay_ms, **kwargs)
        return json

    def update_vm_boot(self, uuid, attribute, value, **kwargs):
        json_payload = dict(attribute=attribute, value=value)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/' + uuid + '/boot', method='PUT',
                               payload=json_payload)
        return json.get('data')

    def get_vm_os(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/os')
        return json.get('data')

    def update_vm_os(self, uuid, os, **kwargs):
        json_payload = dict(value=os)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/' + uuid + '/os', method='PUT',
                               payload=json_payload)
        return json.get('data')

    def get_vm_folder(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/folder')
        return json.get('data')

    def get_vm_version(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/version')
        return json.get('data')

    # Virtual Machine Guest
    def get_vm_guest_os(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/guest/os')
        return json.get('data')

    def run_cmd_guest_vm(self, uuid, user, pwd, cmd, args, **kwargs):
        json_payload = {'user': user,
                        'pass': pwd,
                        'args': args,
                        'cmd': cmd}
        json_payload.update(kwargs)
        json = self.request_v2('/vm/' + uuid + '/guest/cmd',
                               method='POST',
                               payload=json_payload)
        return json.get('data')

    def get_vm_guest_ip(self, uuid):
        json = self.request_v2('/vm/' + uuid)
        data = json['data']
        return data.get('guest').get('ipAddress')

    def get_vm_tools(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/guest/tools',
                               method='GET')
        return json.get('data')

    def upgrade_vm_tools(self, uuid, **kwargs):
        json = self.update_vm_tools(uuid, 'upgrade', **kwargs)
        return json

    def mount_vm_tools(self, uuid, **kwargs):
        json = self.update_vm_tools(uuid, 'mount', **kwargs)
        return json

    def unmount_vm_tools(self, uuid, **kwargs):
        json = self.update_vm_tools(uuid, 'unmount', **kwargs)
        return json

    def update_vm_tools(self, uuid, action, **kwargs):
        json_payload = dict(value=action)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/' + uuid + '/guest/tools',
                               method='PUT', payload=json_payload)
        return json.get('data')

    # Virtual Machine Snapshot Management
    def has_vm_snapshot(self, uuid):
        json = self.get_vm(uuid)
        snapshot = json.get('snapshot')
        return snapshot.get('exist')

    def create_vm_snapshot(self, uuid, desc, date_time, valid):
        import datetime
        date_time_v = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M')
        json_payload = dict(description=desc,
                            from_date=date_time,
                            valid_for=valid)
        json = self.request_v2('/vm/' + uuid + '/snapshot', method='POST',
                               payload=json_payload)
        return json.get('data')

    def get_vm_snapshots(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/snapshot')
        return json.get('data')

    def get_vm_snapshot(self, uuid, snapshot):
        json = self.request_v2('/vm/' + uuid + '/snapshot/' + str(snapshot))
        return json.get('data')

    def delete_vm_snapshot(self, uuid, snapshot):
        json = self.request_v2('/vm/' + uuid + '/snapshot/' + str(snapshot),
                               method='DELETE')
        return json.get('data')

    def revert_vm_snapshot(self, uuid, snapshot):
        json = self.request_v2('/vm/' + uuid + '/snapshot/' + str(snapshot),
                               method='PATCH')
        return json.get('data')

    def get_vm_consolidation(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/snapshot/consolidate')
        return json.get('data')

    def consolidate_vm_disks(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/snapshot/consolidate',
                               method='PUT')
        return json.get('data')

    # Virtual Machine alarms
    def get_vm_alarms(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/alarm')
        return json.get('data')

    def clear_vm_alarm(self, uuid, moref, **kwargs):
        return self.update_vm_alarm(uuid=uuid, moref=moref,
                                    value='clear', **kwargs)

    def ack_vm_alarm(self, uuid, moref, **kwargs):
        return self.update_vm_alarm(uuid=uuid, moref=moref,
                                    value='ack', **kwargs)

    def update_vm_alarm(self, uuid, moref, **kwargs):
        json_payload = {}
        json_payload.update(kwargs)
        json = self.request_v2('/vm/' + uuid + '/alarm/' + moref, method='PUT',
                               payload=json_payload)
        return json.get('data')

    # Virtual Machine events
    def get_vm_events(self, uuid, hours=1):
        event_uri = '/event/{}'.format(hours) if hours > 1 else '/event'
        json = self.request_v2('/vm/' + uuid + event_uri)
        return json.get('data')

    # Virtual Machine performance
    def get_vm_performance_cpu(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/performance/cpu')
        return json.get('data')

    def get_vm_performance_memory(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/performance/memory')
        return json.get('data')

    def get_vm_performance_io(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/performance/io')
        return json.get('data')

    def get_vm_performance_net(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/performance/net')
        return json.get('data')

    # Virtual Machine creation and deployment
    def export_vm(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/export', method='POST')
        return json.get('data')

    def delete_vm(self, uuid):
        json = self.request_v2('/vm/' + uuid, method='DELETE')
        return json.get('data')

    def create_vm(self, os, built, bill_dept, description, folder, **kwargs):
        json_payload = {'os': os,
                        'built_from': built,
                        'bill_dept': bill_dept,
                        'description': description,
                        'folder': folder}
        # additional elements
        json_payload.update(kwargs)
        json = self.request_v2('/vm', payload=json_payload, method='POST')
        return json.get('data')

    def create_vms(self, count, name, os, built, bill_dept,
                   description, folder, **kwargs):
        json_payload = {'os': os,
                        'built_from': built,
                        'bill_dept': bill_dept,
                        'description': description,
                        'folder': folder,
                        'names': ['%s_%s' % (name, i)
                                  for i in range(0, count)]}
        json_payload.update(kwargs)
        json = self.request_v2('/vm', payload=json_payload, method='POST')
        return json.get('data')

    def create_vm_from_image(self, os, image, bill_dept,
                             description, folder, **kwargs):
        json_payload = {'os': os,
                        'built_from': 'image',
                        'bill_dept': bill_dept,
                        'description': description,
                        'folder': folder,
                        'source_image': image}
        json_payload.update(kwargs)
        json = self.request_v2('/vm', payload=json_payload,
                               method='POST')
        return json.get('data')

    def get_vm_console(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/console')
        return json.get('data')

    def is_vm_template(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/template')
        return json.get('data')

    def mark_vm_as_template(self, uuid):
        json_payload = {'value': True}
        json = self.request_v2('/vm/' + uuid + '/template',
                               payload=json_payload, method='PUT')
        return json.get('data')

    def get_vm_memory(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/memory')
        return json.get('data')

    def set_vm_memory(self, uuid, size):
        json = self.request_v2('/vm/' + uuid + '/memory',
                               payload=dict(value=int(size)),
                               method='PUT')
        return json.get('data')

    def get_vm_cpu(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/cpu')
        return json.get('data')

    def set_vm_cpu(self, uuid, number):
        json = self.request_v2('/vm/' + uuid + '/cpu',
                               payload=dict(value=int(number)),
                               method='PUT')
        return json.get('data')

    # Virtual Machine devices
    def get_vm_nics(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/nic')
        nic_numbers = [nic.get('unit') for nic in json.get('data')]
        nics = list()
        for nic in nic_numbers:
            json = self.request_v2('/vm/' + uuid + '/nic/' + nic)
            nics.append({'unit': nic,
                         'data': json['data'][0]})
        return nics

    def get_vm_nic(self, uuid, nic):
        json = self.request_v2('/vm/' + uuid + '/nic/' + nic)
        return json.get('data')

    def get_vm_cds(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/cd')
        cd_units = [cd.get('unit') for cd in json.get('data')]
        cds = list()
        for cd in cd_units:
            data = self.get_vm_cd(uuid, cd)
            cds.append({'unit': cd,
                        'data': data[0]})
        return cds

    def get_vm_cd(self, uuid, cd):
        json = self.request_v2('/vm/' + uuid + '/disk/' + cd)
        return json.get('data')

    def get_vm_disks(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/disk')
        disk_units = [disk.get('unit') for disk in json.get('data')]
        disks = list()
        for disk in disk_units:
            data = self.get_vm_disk(uuid, disk)
            disks.append({'unit': disk,
                          'data': data[0]})
        return disks

    def get_vm_disk(self, uuid, disk):
        json = self.request_v2('/vm/' + uuid + '/disk/' + disk)
        return json.get('data')

    def is_powered_on_vm(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/state')
        power_state = json.get('data').get('powerState')
        if power_state:
            return power_state == 'poweredOn'
        else:
            return False

    def reboot_vm(self, uuid):
        json = self.update_vm_state(uuid=uuid, state='reboot')
        return json.get('data')

    def reset_vm(self, uuid):
        json = self.update_vm_state(uuid=uuid, state='reset')
        return json

    def power_cycle_vm(self, uuid):
        power_off_task = self.power_off_vm(uuid)
        sleep(5)
        power_on_task = self.power_on_vm(uuid)
        return [power_off_task['data'], power_on_task['data']]

    def power_off_vm(self, uuid):
        json = self.update_vm_state(uuid=uuid, state='poweredOff')
        return json

    def power_on_vm(self, uuid):
        json = self.update_vm_state(uuid=uuid, state='poweredOn')
        return json

    def shutdown_vm(self, uuid, **kwargs):
        json = self.update_vm_state(uuid=uuid, state='shutdown', **kwargs)
        return json

    def rename_vm(self, uuid, name, **kwargs):
        json_payload = dict(name=name)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/' + uuid + '/name', method='PUT',
                               payload=json_payload)

        return json.get('data')

    # Virtual Machine Notes
    def get_vm_notes(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/note/client')
        return json.get('data')

    def update_vm_note(self, uuid, notes_dict, **kwargs):
        json_payload = dict(value=notes_dict)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/' + uuid + '/note/client',
                               method='PUT', payload=json_payload)
        return json.get('data')

    # Virtual Machine VSS attributes
    def get_vm_vss_admin(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/vss/admin')
        return json.get('data')

    def update_vm_vss_admin(self, uuid, name, phone, email):
        json_payload = dict(value=':'.join([name, phone, email]))
        json = self.request_v2('/vm/' + uuid + '/vss/admin', method='POST',
                               payload=json_payload)
        return json.get('data')

    def get_vm_vss_usage(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/vss/usage')
        return json.get('data')

    def get_vm_vss_changelog(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/vss/changelog')
        return json.get('data')

    def update_vm_vss_usage(self, uuid, usage, **kwargs):
        json_payload = dict(value=usage)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/' + uuid + '/vss/usage',
                               payload=json_payload,
                               method='PUT')
        return json.get('data')

    def get_vm_vss_inform(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/vss/inform')
        return json.get('data')

    def update_vm_vss_inform(self, uuid, value, append, **kwargs):
        json_payload = dict(value=value, append=append)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/' + uuid + '/vss/inform',
                               method='PUT', payload=json_payload)
        return json.get('data')

    def get_vm_vss_requested(self, uuid):
        json = self.request_v2('/vm/' + uuid + '/vss')
        return json.get('data').get('requested')

    # Virtual Machine summary
    def get_vm_storage(self, uuid):
        json = self.get_vm(uuid)
        return json.get('storage')

    def request_v2(self, url, headers={}, params=None, payload={},
                   method='GET', auth=None):
        headers['Content-Type'] = 'application/json'
        headers['User-Agent'] = 'pyvss/{}'.format(__version__)
        if not url.startswith('http'):
            url = self.api_endpoint + url
        auth = HTTPBasicAuth(self.api_token, '') if not auth else auth
        try:
            if method == 'POST':
                resp = requests.post(url, headers=headers,
                                     timeout=60, auth=auth, json=payload)
                json = self.process_response(resp)
            elif method == 'DELETE':
                resp = requests.delete(url, data=json_module.dumps(params),
                                       headers=headers,
                                       timeout=60, auth=auth, json=payload)
                json = self.process_response(resp)
            elif method == 'PUT':
                resp = requests.put(url, headers=headers, params=params,
                                    timeout=60, auth=auth, json=payload)
                json = self.process_response(resp)
            elif method == 'GET':
                resp = requests.get(url, headers=headers, params=params,
                                    timeout=60, auth=auth, json=payload)
                json = resp.json()
            elif method == 'OPTIONS':
                resp = requests.options(url, headers=headers, params=params,
                                        timeout=60, auth=auth, json=payload)
                json = resp.json()
            else:
                raise VssError('Unsupported method %s' % method)

        except ValueError:  # requests.models.json.JSONDecodeError
            raise ValueError("The API server didn't "
                             "respond with a valid json")
        except requests.RequestException as e:  # errors from requests
            raise RuntimeError(e)

        if resp.status_code != requests.codes.ok:
            if json:
                if 'error' in json and 'message' in json:
                    raise VssError(json['error'] + ': ' + json['message'])
                elif 'parameters' in json and 'message' in json:
                    error = json['message'] + ': ' + \
                            ', '.join(json['parameters'])
                    raise VssError(error)
            resp.raise_for_status()
        return json

    @staticmethod
    def process_response(response):
        if response.status_code == 204:
            return {'status': response.status_code}
        else:
            return response.json()

    def wait_for_request(self, request_url, request_attr,
                         required_status, max_tries=6):
        tries = 0
        while True:
            request = self.request_v2(request_url)
            if 'data' in request:
                if 'status' in request['data']:
                    status = request['data']['status']
                    if required_status == status:
                        return request['data'][request_attr]
                    elif status in ['Pending', 'In Progress']:
                        pass
                    elif status in ['Error Retry', 'Error Processed']:
                        return False
            else:
                return False
            if tries >= max_tries:
                return False
            tries += 1
            sleep(10)

if __name__ == '__main__':
    import sys
    import pprint
    api_token = os.environ.get('VSS_API_TOKEN')
    if not api_token:
        raise VssError('Specify environment variable VSS_API_TOKEN')
    manager = VssManager(api_token)
    fname = sys.argv[1]
    pprint.pprint(getattr(manager, fname)(*sys.argv[2:]), indent=1)
