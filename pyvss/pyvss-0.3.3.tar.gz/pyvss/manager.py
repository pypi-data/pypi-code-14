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

API_ENDPOINT_BASE = 'https://vss-api.eis.utoronto.ca:8001'
API_ENDPOINT = '{}/v2'.format(API_ENDPOINT_BASE)
TOKEN_ENDPOINT = '{}/auth/request-token'.format(API_ENDPOINT_BASE)


class VssError(RuntimeError):
    pass


class VssManager(object):
    """
    Class containing methods to interact with the VSS REST API

    Example::

        vss = VssManager(tk='access-token')
        vss.whoami()

    """
    def __init__(self, tk):
        """
        VSS Manager to interact with the REST API
        :param tk: REST API access token
        :param tk: str
        """
        self.api_endpoint = API_ENDPOINT
        self.api_token = tk

    def get_token(self):
        """
        Generates token based on two environment variables:

        - ``VSS_API_USER``: username
        - ``VSS_API_PASS``: password

        :return: generated token or VssError
        """
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
        """
        Gets both request and access roles of current user

        :return: object
        """
        json = self.request_v2('/user/role', method='GET')
        return json.get('data')

    def get_user_token(self, token_id):
        """
        Obtains given token id data such as:

        - value
        - status

        :param token_id: Access token id to manage
        :type token_id: int
        :return:
        """
        json = self.request_v2('/user/token/{tk}'.format(tk=token_id),
                               method='GET')
        return json.get('data')

    def disable_user_token(self, token_id):
        """
        Disables given access token id

        :param token_id: token id to disable
        :type token_id: int
        :return: status dict
        """
        json = self.request_v2('/user/token/{tk}'.format(tk=token_id),
                               method='PUT')
        return json

    def get_user_tokens(self, **kwargs):
        """
        Get all user tokens

        :param kwargs: arguments to pass such as:

        - filter=<field_name>,<operator>,<value>
        - sort=<field_name>,<asc|desc>
        - per_page=<value>
        - expand=<value>

        :return: object with results and meta containing pages
        """
        json = self.request_v2('/user/token', params=kwargs,
                               method='GET')
        meta = json.get('meta')
        return dict(meta=meta.get('pages'), data=json.get('data'))

    def delete_user_token(self, token_id):
        """
        Deletes given token id

        :param token_id: Token id to delete
        :type token_id: int
        :return: dict with request status
        """
        json = self.request_v2('/user/token/{tk}'.format(tk=token_id),
                               method='DELETE')
        return json

    def get_user_email_settings(self):
        """
        Returns current user email settings

        Email settings currently are:

        - all: receive email notifications
        - completion: receive email notification upon completion
        - error: receive email notifications only when error
        - none: no email notifications
        - submission: receive email notification when submitted

        :return: object
        """
        json = self.request_v2('/user/setting/email', method='GET')
        return json.get('data')

    def disable_user_email(self):
        """
        Disables all email notification

        :return: updated email settings object
        """
        json = self.update_user_email_settings(attribute='none',
                                               value=True)
        return json

    def enable_user_email(self):
        """
        Enables all email notification

        :return: updated email settings object
        """
        json = self.update_user_email_settings(attribute='all',
                                               value=True)
        return json

    def enable_user_email_error(self):
        """
        Updates email notification settings to get just errors

        :return: updated email settings object
        """
        json = self.update_user_email_settings(attribute='error',
                                               value=True)
        return json

    def update_user_email_settings(self, attribute, value):
        """
        Updates user email notification settings for a given
        attribute and value

        :param attribute: attribute to update. could be
         ``<error|none|completion|submission>``
        :type attribute: str
        :param value: True or false
        :type value: bool
        :return: updated email settings object

        """
        json_payload = dict(attribute=attribute, value=value)
        json = self.request_v2('/user/setting/email', method='PUT',
                               payload=json_payload)
        json.update(self.get_user_email_settings())
        return json

    def whoami(self):
        """
        Retrieves current user summary

        :return: object
        """
        json = self.request_v2('/user')
        return json.get('data')

    # Operating systems
    def get_os(self, **kwargs):
        """
        Gets Virtual Machine supported Guest Operating systems

        :param kwargs: arguments to pass such as:

        - name: Guest operating system full name. i.e. CentOS 4/5
        - id: Guest operating system id. i.e. centosGuest

        :return: object
        """
        json = self.request_v2('/os', params=kwargs, method='GET')
        return json.get('data')

    # inventory management
    def create_inventory_file(self, props=None, fmt='json'):
        """ Submits a request to generate a full inventory
        report of your Virtual Machines.

        .. _VSKEY-STOR: https://vskey-stor.eis.utoronto.ca

        The report will be transferred to your space at VSKEY-STOR_

        :param props: properties to include in report
        :type props: str or None. defaults uuid and name
        :param fmt: report format <json|csv>. default json
        :type fmt: str
        :return: inventory request object

        .. note:: See `Inventory Docs <https://wiki.eis.utoronto.ca/x/_gCC>`_
          for more information

        """
        props = ['Uuid', 'Name'] if not props else props.split(',')
        json_payload = dict(properties=props, format=fmt)
        json = self.request_v2('/inventory', payload=json_payload,
                               method='POST')
        return json.get('data')

    # Request management
    def get_requests(self, **kwargs):
        json = self.request_v2('/request', params=kwargs)
        return json.get('data')

    def get_new_requests(self, **kwargs):
        json = self.request_v2('/request/new', params=kwargs)
        return json.get('data')

    def get_new_request(self, request_id, **kwargs):
        json = self.request_v2('/request/new/{id}'.format(id=request_id),
                               params=kwargs)
        return json.get('data')

    # Domain management
    def get_domains(self, **kwargs):
        """
        Get available Fault Domains

        :param kwargs: filters

        - moref: managed object reference
        - name: domain name

        :return: list of objects

        """
        json = self.request_v2('/domain', params=kwargs)
        return json.get('data')

    def get_domain(self, moref, **kwargs):
        """
        Get fault domain data

        :param moref: managed object reference
        :type moref: str
        :param kwargs: filter key-word args

        - summary: list vms running on fault domain

        :return: object
        """
        json = self.request_v2('/domain/{moId}'.format(moId=moref),
                               params=kwargs)
        return json.get('data')

    def get_vms_by_domain(self, domain_moref):
        """
        Get Virtual Machines on given Fault Domain

        :param domain_moref: Domain managed object reference
        :type domain_moref: str
        :return: list of vm objects

        """
        json = self.get_domain(domain_moref, summary=1)
        return json.get('vms')

    # Image Management
    def get_images(self, **kwargs):
        """
        Get available virtual machine OVF/OVA files.

        :param kwargs: filters

        - name: filter by name
        - path: filter by path

        :return: lust of images

        .. _VSKEY-STOR: https://vskey-stor.eis.utoronto.ca

        .. note:: Files are stored in VSKEY-STOR_

        """
        json = self.request_v2('/image', params=kwargs)
        return json.get('data')

    # ISO Management
    def get_isos(self, **kwargs):
        """
        Get list ISO images you are allowed to access.

        .. _VSKEY-STOR: https://vskey-stor.eis.utoronto.ca

        Also includes files in your VSKEY-STOR_ space.

        :param kwargs: filters

        - name: filter by name
        - path: filter by path

        :return: list of iso images

        """
        json = self.request_v2('/iso', params=kwargs)
        return json.get('data')

    # Network Management
    def get_networks(self, **kwargs):
        """
        Get list networks you are allowed to access

        :param kwargs: filters

        - name: filter by name
        - moref: filter by network managed object reference
        - summary: show network summary

        :return: list of objects

        """
        json = self.request_v2('/network', params=kwargs)
        return json.get('data')

    def get_network(self, moref, **kwargs):
        """
        Get details of given network

        :param moref: network managed object reference
        :param kwargs: additional parameters

        - summary: show vms on this network

        :return: list of virtual machine objects

        """
        json = self.request_v2('/network/{moId}'.format(moId=moref),
                               params=kwargs)
        return json.get('data')

    def get_vms_by_network(self, moref):
        """
        Get Virtual Machines on given network

        :param moref: network managed object reference
        :return: list of objects
        """
        json = self.get_network(moref, summary=1)
        return json.get('vms')

    # Folder Management
    def get_folders(self, **kwargs):
        """
        Get list of logical folders

        :param kwargs: arguments to pass such as:

        - moref: filter by managed object reference
        - name: filter by name
        - parent: filter by parent name
        - summary: show folder summary

        :return: list of objects
        """
        json = self.request_v2('/folder', params=kwargs)
        return json.get('data')

    def get_folder(self, moref, **kwargs):
        """
        Get logical folder data

        :param moref: managed object reference
        :type moref: str
        :param kwargs: arguments to pass such as:

        - summary: enables children vm listing

        :return: object
        """
        json = self.request_v2('/folder/{moId}'.format(moId=moref),
                               params=kwargs)
        return json.get('data')

    def create_folder(self, moref, name):
        """
        Creates logical folder under given managed object
        reference

        :param moref: Parent folder managed object reference
        :param name: New folder name
        :return: folder request object
        """
        json_payload = dict(name=name)
        json = self.request_v2('/folder/{moId}'.format(moId=moref),
                               payload=json_payload,
                               method='POST')
        return json.get('data')

    def move_folder(self, moref, new_moref):
        """
        Moves given folder to new parent

        :param moref: folder to move managed object
         reference
        :param new_moref: target parent managed object
         reference to move folder to
        :return: folder request object

        """
        json_payload = dict(attribute='parent', value=new_moref)
        json = self.request_v2('/folder/{moId}'.format(moId=moref),
                               payload=json_payload,
                               method='PUT')
        return json.get('data')

    def rename_folder(self, moref, name, **kwargs):
        """
        Renames given logical folder

        :param moref: folder managed object reference
        :param name: folder new name
        :return: folder request object
        """
        json_payload = dict(attribute='name', value=name)
        json_payload.update(kwargs)
        json = self.request_v2('/folder/' + moref,
                               payload=json_payload,
                               method='PUT')
        return json.get('data')

    # Virtual Machine Management
    def get_templates(self, **kwargs):
        """
        Get list of your templates

        :param kwargs: filters and flags

        - name: filters by name
        - summary: displays summary of template

        :return: list of virutal machine objects
        """
        json = self.request_v2('/template', params=kwargs)
        return json.get('data')

    def get_vms(self, **kwargs):
        """
        Get list of virtual machines

        :param kwargs: filters and flags

        - dns: filter by main dns name
        - ip: filter by main ip address
        - name: filter by name
        - path: filter by VM path
        - summary: show VMs summary or not.

        :return: list of virtual machine objects
        """
        json = self.request_v2('/vm', params=kwargs)
        return json.get('data')

    def get_vm(self, uuid, **kwargs):
        """
        Get basic information of given virtual machine

        :param uuid: virtual machine uuid
        :type uuid: str

        :return: object

        Virtual Machine attributes include:

        - storage
        - state
        - snapshot
        - note
        - devices
        - memory
        - cpu
        - guest
        - folder

        .. note:: more information about required attributes
          available in `Virtual Machine <https://wiki.eis.utoronto.ca/x/pgCC>`_

        """
        json = self.request_v2('/vm/{uuid}'.format(uuid=uuid),
                               params=kwargs)
        return json.get('data')

    def get_vm_name(self, uuid):
        """
        Gets given Virtual Machine full name

        :param uuid: Virtual Machine uuid
        :type uuid: str
        :return: object
        """
        json = self.request_v2('/vm/{uuid}/name'.format(uuid=uuid))
        return json.get('data')

    def get_vm_state(self, uuid):
        """
        Gets given Virtual Machine state info

        :param uuid: Virtual Machine uuid
        :type uuid: str
        :return: object

        Virtual Machine attributes include:

        - bootTime
        - domain
        - connectionState
        - powerState

        """
        json = self.request_v2('/vm/{uuid}/state'.format(uuid=uuid))
        return json.get('data')

    def update_vm_state(self, uuid, state, **kwargs):
        """
        Updates given Virtual Machine power state

        :param uuid: Virtual Machine uuid
        :type uuid: str
        :param state: Desired state
        :type state: str
        :return: change request object

        .. note:: key words arguments include schedule to process request
          on a given date and time

        """
        if state not in ['poweredOff', 'poweredOn', 'reset', 'reboot',
                         'shutdown']:
            raise VssError('Unsupported {state} state'.format(state=state))
        json_payload = dict(value=state)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/{uuid}/state'.format(uuid=uuid),
                               method='PUT',
                               payload=json_payload)
        return json.get('data')

    def get_vm_domain(self, uuid):
        """
        Get domain where Virtual Machine is running

        :param uuid: Virtual Machine uuid
        :type uuid: str
        :return: object
        """
        json = self.request_v2('/vm/{uuid}/domain'.format(uuid=uuid))
        return json.get('data')

    def update_vm_domain(self, uuid, moref, power_on=False,
                         force=False, **kwargs):
        """
        Updates fault domain of given VM

        :param uuid: Virtual Machine uuid
        :type uuid: str
        :param moref: Target domain managed object reference
        :type moref: str
        :param power_on: Whether VM will be powered of after migration
        :type power_on: bool
        :param force: If set to True, VM will be powered off prior migration
        :type force: bool
        :return: change request object

        .. note:: key words arguments include schedule to process request
                  on a given date and time

        .. seealso:: :func:``get_domains`` for os parameter
        """
        valid_domain = self.get_domains(moref=moref)
        json_payload = dict(value=moref, poweron=power_on, force=force)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/{uuid}/domain'.format(uuid=uuid),
                               method='PUT',
                               payload=json_payload)
        return json.get('data')

    # Virtual Machine Configuration
    def get_vm_boot(self, uuid):
        """
        Queries given Virtual Machine boot configuration

        :param uuid: Virtual Machine UUid
        :type uuid: int
        :return: object

        Configuration includes:

        - enterBIOSSetup
        - bootRetryDelayMs
        - bootDelayMs

        .. note:: more information about required attributes available in
          `Virtual Machine Attributes <https://wiki.eis.utoronto.ca/x/5ACC>`_

        """
        json = self.request_v2('/vm/{uuid}/boot'.format(uuid=uuid))
        return json.get('data')

    def update_vm_boot_bios(self, uuid, boot_bios, **kwargs):
        """
        Updates boot to bios configuration

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param boot_bios: Enable or disable
        :type boot_bios: bool
        :return: change request object

        .. note:: key words arguments include schedule to process request
                  on a given date and time

        """
        json = self.update_vm_boot(uuid, attribute='bootbios',
                                   value=boot_bios, **kwargs)
        return json

    def update_vm_boot_delay(self, uuid, boot_delay_ms, **kwargs):
        """
        Updates boot bios delay configuration

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param boot_delay_ms: boot delay in milliseconds
        :type boot_delay_ms: int
        :return: change request object

        .. note:: key words arguments include schedule to process request
                  on a given date and time
        """
        json = self.update_vm_boot(uuid, attribute='bootdelay',
                                   value=boot_delay_ms, **kwargs)
        return json

    def update_vm_boot(self, uuid, attribute, value, **kwargs):
        """
        Helper function to update boot configuration

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param attribute: Either boot bios or boot delay
        :param value: int or bool
        :return: change request object

        .. note:: key words arguments include schedule to process request
                  on a given date and time
        """
        if attribute not in ['bootbios', 'bootdelay']:
            raise VssError('Boot attribute {} not supported'.format(attribute))
        json_payload = dict(attribute=attribute, value=value)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/{uuid}/boot'.format(uuid=uuid),
                               method='PUT',
                               payload=json_payload)
        return json.get('data')

    def get_vm_os(self, uuid):
        """
        Gets Virtual Machine configured Operating System

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: object
        """
        json = self.request_v2('/vm/{uuid}/os'.format(uuid=uuid))
        return json.get('data')

    def update_vm_os(self, uuid, os, **kwargs):
        """
        Updates Virtual Machine Operating System configuration
        :param uuid: Virtual Machine uuid
        :type uuid: str
        :param os: Operating system id.
        :type os: str
        :return: change request object

        .. note:: key words arguments include schedule to process request
                  on a given date and time
        .. seealso:: :func:``get_os`` for os parameter

        """
        json_payload = dict(value=os)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/{uuid}/os'.format(uuid=uuid),
                               method='PUT',
                               payload=json_payload)
        return json.get('data')

    def get_vm_folder(self, uuid):
        """
        Gets given Virtual Machine parent folder information

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: object

        attributes include:

        - full_path
        - name
        - parent
        - reference to folder resource

        .. seealso:: :func:``get_folder``
        """
        json = self.request_v2('/vm/{uuid}/folder'.format(uuid=uuid))
        return json.get('data')

    def get_vm_version(self, uuid):
        """
        Given Virtual Machine VMX version

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: object
        """
        json = self.request_v2('/vm/{uuid}/version'.format(uuid=uuid))
        return json.get('data')

    # Virtual Machine Guest
    def get_vm_guest_os(self, uuid):
        """
        Gets Virtual Machine Guest Operating System

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: object
        """
        json = self.request_v2('/vm/{uuid}/guest/os'.format(uuid=uuid))
        return json.get('data')

    def run_cmd_guest_vm(self, uuid, user, pwd, cmd, arg, **kwargs):
        """
        Executes command in Guest Operating System

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param user: Guest Operating Username
        :type user: str
        :param pwd: Guest Operating Username password
        :type pwd: str
        :param cmd: Command to execute
        :type cmd: str
        :param arg: Command arguments
        :type arg: str
        :return: change request object

        .. note:: key words arguments include schedule to process request
          on a given date and time

        .. note:: more information about required attributes
          available in
          `Virtual Machine Attributes <https://wiki.eis.utoronto.ca/x/5ACC>`_

        """
        json_payload = {'user': user, 'pass': pwd,
                        'args': arg, 'cmd': cmd}
        json_payload.update(kwargs)
        json = self.request_v2('/vm/{uuid}/guest/cmd'.format(uuid=uuid),
                               method='POST',
                               payload=json_payload)
        return json.get('data')

    def get_vm_guest_ip(self, uuid):
        """
        Get Virtual Machine IP and Mac addresses via
        VMware tools

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: list of objects
        """
        json = self.request_v2('/vm/{uuid}/guest/net/ip'.format(uuid=uuid))
        return json.get('data')

    # VMWare Tools
    def get_vm_tools(self, uuid):
        """
        Get VMware Tools status on given Virtual Machine

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: object

        attributes include:

        - runningStatus
        - version
        - versionStatus
        """
        json = self.request_v2('/vm/{uuid}/guest/tools'.format(uuid=uuid),
                               method='GET')
        return json.get('data')

    def upgrade_vm_tools(self, uuid, **kwargs):
        """
        Upgrade VMware Tools if Virtual Machine is using the
        official VMware Tools version.

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: change request object

        .. note:: This method fails if Guest OS is running
          an unmanaged distribution of VMware Tools.

        .. note:: key words arguments include schedule to process request
          on a given date and time

        """
        json = self.update_vm_tools(uuid, 'upgrade', **kwargs)
        return json

    def mount_vm_tools(self, uuid, **kwargs):
        """
        Mounts VMware official distribution of VMware Tools
        in Guest Operating system

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: change request object

        .. note:: This method fails if Guest OS is running
          an unmanaged distribution of VMware Tools.

        .. note:: key words arguments include schedule to process request
          on a given date and time

        """
        json = self.update_vm_tools(uuid, 'mount', **kwargs)
        return json

    def unmount_vm_tools(self, uuid, **kwargs):
        """
        Unmounts VMware official distribution of VMware Tools
        in Guest Operating system

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: change request object

        .. note:: This method fails if VMware Tools ISO is not
          mounted in guest OS

        .. note:: key words arguments include schedule to process request
          on a given date and time

        """
        json = self.update_vm_tools(uuid, 'unmount', **kwargs)
        return json

    def update_vm_tools(self, uuid, action, **kwargs):
        """
        Helper method to manage VMware tools on Virtual Machiene.

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param action: Either mount, unmount or upgrade actions
        :type action: str
        :return: change request object

        .. note:: key words arguments include schedule to process request
                  on a given date and time
        """
        if action not in ['mount', 'unmount', 'upgrade']:
            raise VssError('Unsupported {} action'.format(action))
        json_payload = dict(value=action)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/{uuid}/guest/tools'.format(uuid=uuid),
                               method='PUT', payload=json_payload)
        return json.get('data')

    # Virtual Machine Snapshot Management
    def has_vm_snapshot(self, uuid):
        """
        Validates if Virtual Machine has snapshots

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: bool
        """
        json = self.get_vm(uuid)
        snapshot = json.get('snapshot')
        return snapshot.get('exist')

    def create_vm_snapshot(self, uuid, desc, date_time, valid):
        """
        Creates a Virtual Machine snapshot on a given date and time

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param desc: A brief description of the snapshot.
        :type desc: str
        :param date_time: Timestamp with the following format %Y-%m-%d %H:%M.
         If date is in the past, the snapshot will be taken right away,
         otherwise it will wait.
         :type desc: str
        :param valid: Number of hours (max 72) the snapshot will live
        :type valid: int
        :return: snapshot request object

        """
        import datetime
        date_time_v = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M')
        json_payload = dict(description=desc,
                            from_date=date_time,
                            valid_for=valid)
        json = self.request_v2('/vm/{uuid}/snapshot'.format(uuid=uuid),
                               method='POST',
                               payload=json_payload)
        return json.get('data')

    def get_vm_snapshots(self, uuid):
        """
        Listing existent Virtual Machine snapshots

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: list of objects
        """
        json = self.request_v2('/vm/{uuid}/snapshot'.format(uuid=uuid))
        return json.get('data')

    def get_vm_snapshot(self, uuid, snapshot):
        """
        Get given Virtual Machine Snapshot information

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param snapshot: Snapshot Id
        :type snapshot: int
        :return: object
        """
        json = self.request_v2('/vm/{uuid}/snapshot/{id)'.format(
            uuid=uuid, id=snapshot))
        return json.get('data')

    def delete_vm_snapshot(self, uuid, snapshot):
        """
        Deletes given Virtual Machine snapshot

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param snapshot: Snapshot Id
        :type snapshot: int
        :return: snapshot request object
        """
        json = self.request_v2('/vm/{uuid}/snapshot/{id)'.format(
            uuid=uuid, id=snapshot), method='DELETE')
        return json.get('data')

    def revert_vm_snapshot(self, uuid, snapshot):
        """
        Reverts to given Virtual Machine snapshot

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param snapshot: Snapshot Id
        :type snapshot: int
        :return: snapshot request object
        """
        json = self.request_v2('/vm/{uuid}/snapshot/{id)'.format(
            uuid=uuid, id=snapshot), method='PATCH')
        return json.get('data')

    def get_vm_consolidation(self, uuid):
        """
        Gets current Virtual Machine disks consolidation state

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: object
        """
        json = self.request_v2(
            '/vm/{uuid}/snapshot/consolidate'.format(uuid=uuid))
        return json.get('data')

    def consolidate_vm_disks(self, uuid, **kwargs):
        """
        Submits a Virtual Machine disk consolidation

        :param uuid:
        :return: change request object

        .. note:: key words arguments include schedule to process request
                  on a given date and time
        """
        payload = dict()
        payload.update(kwargs)
        json = self.request_v2(
            '/vm/{uuid}/snapshot/consolidate'.format(uuid=uuid),
            method='PUT', payload=payload)
        return json.get('data')

    # Virtual Machine alarms
    def get_vm_alarms(self, uuid):
        """
        Gets Virtual Machine Alarms

        :param uuid: Virtual Machine uuid
        :type uuid: str
        :return: list of objects
        """
        json = self.request_v2('/vm/{uuid}/alarm'.format(uuid=uuid))
        return json.get('data')

    def clear_vm_alarm(self, uuid, moref, **kwargs):
        """
        Clears given Virtual Machine alarm

        :param uuid: Virtual Machine uuid
        :type uuid: str
        :param moref: Virtual Machine Alarm managed object
                      reference
        :return: change request object

        .. note:: key words arguments include schedule to process request
          on a given date and time
        """
        return self.update_vm_alarm(uuid=uuid, moref=moref,
                                    value='clear', **kwargs)

    def ack_vm_alarm(self, uuid, moref, **kwargs):
        """
        Acknowledges given Virtual Machine alarm

        :param uuid: Virtual Machine uuid
        :type uuid: str
        :param moref: Virtual Machine Alarm managed object
                      reference
        :return: change request object

        .. note:: key words arguments include schedule to process request
          on a given date and time

        """
        return self.update_vm_alarm(uuid=uuid, moref=moref,
                                    value='ack', **kwargs)

    def update_vm_alarm(self, uuid, moref, **kwargs):
        """
        Updates given Virtual Machine Alarm

        :param uuid: Virtual Machine uuid
        :type uuid: str
        :param moref: Virtual Machine Alarm managed object
         reference
        :return: change request object

        .. note:: key words arguments include schedule to process request
          on a given date and time

        """
        json_payload = dict()
        json_payload.update(kwargs)
        json = self.request_v2(
            '/vm/{uuid]/alarm/{moref}'.format(uuid=uuid,
                                              moref=moref),
            method='PUT',
            payload=json_payload)
        return json.get('data')

    # Virtual Machine events
    def get_vm_events(self, uuid, hours=1):
        """
        Queries Virtual Machine events in vCenter

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param hours: Time window to get events from
        :type hours: int
        :return: list of events

        """
        event_uri = '/event/{}'.format(hours) if hours > 1 else '/event'
        json = self.request_v2('/vm/{uuid}{events}'.format(uuid=uuid,
                                                           events=event_uri))
        return json.get('data')

    # Virtual Machine performance
    def get_vm_performance_cpu(self, uuid):
        """
        Queries given Virtual Machine CPU
        performance counters. VM has to be powered On.

        :param uuid: Virtual Machine uuid
        :type uuid: str
        :return: object

        Performance counters include:

        - readyAvgPct
        - readyMaxPct
        - usagePct

        """
        json = self.request_v2(
            '/vm/{uuid}/performance/cpu'.format(uuid=uuid))
        return json.get('data')

    def get_vm_performance_memory(self, uuid):
        """
        Queries given Virtual Machine Memory
        performance counters. VM has to be powered On.

        :param uuid: Virtual Machine uuid
        :type uuid: str
        :return: object

        Performance counters include:

        - activeMb
        - activePct
        - balloonMb
        - balloonPct
        - dateTime
        - name
        - sharedMb
        - sharedPct
        - swappedMb
        - swappedPct
        - usagePct

        """
        json = self.request_v2(
            '/vm/{uuid}/performance/memory'.format(uuid=uuid))
        return json.get('data')

    def get_vm_performance_io(self, uuid):
        """
        Queries given Virtual Machine IO (datastore)
        performance counters. VM has to be powered On.

        :param uuid: Virtual Machine uuid
        :type uuid: str
        :return: object

        Performance counters include:

        - ioReadIops
        - ioWriteIops
        - latReadMs
        - latWriteMs

        """
        json = self.request_v2(
            '/vm/{uuid}/performance/io'.format(uuid=uuid))
        return json.get('data')

    def get_vm_performance_net(self, uuid):
        """
        Queries given Virtual Machine Network
        performance counters. VM has to be powered On.

        :param uuid: Virtual Machine uuid
        :type uuid: str
        :return: object

        Performance counters include:

        - rxErrors
        - rxMbps
        - txErrors
        - txMbps

        """
        json = self.request_v2(
            '/vm/{uuid}/performance/net'.format(uuid=uuid))
        return json.get('data')

    # Virtual Machine creation and deployment
    def export_vm(self, uuid):
        """
        Export given Virtual Machine to OVF.

        :param uuid: Virtual Machine uuid
        :type uuid: str
        :return: export request object

        .. _VSKEY-STOR: https://vskey-stor.eis.utoronto.ca

        .. note:: Once the export completes, will be transferred to
          VSKEY-STOR_

        """
        json = self.request_v2('/vm/{uuid}/export'.format(uuid=uuid),
                               method='POST')
        return json.get('data')

    def delete_vm(self, uuid):
        """
        Deletes given Virtual Machine

        :param uuid: Virtual Machine uuid
        :type uuid: str
        :return: change request object

        """
        json = self.request_v2('/vm/{uuid}'.format(uuid=uuid),
                               method='DELETE')
        return json.get('data')

    def create_vm(self, name, os, built, bill_dept,
                  description, folder, networks, disks,
                  usage='Test', cpu=1, memoryGB=1, **kwargs):
        """
        Creates single Virtual Machine. Names are generated
        by appending name_number

        :param name: name of the new virtual machine
        :type name: str
        :param os: Operating system id.
        :type os: str
        :param built: built process
        :param bill_dept: Billing department
        :type bill_dept: str
        :param description: VM description
        :type description: str
        :param folder: Target VM folder moref
        :type folder: str
        :param networks: list of networks morefs
        :type networks: list
        :param disks: list of disk sizes in GB
        :type disks: list
        :param usage: virtual machine usage
        :type usage: str
        :param cpu: vCPU count
        :type cpu: int
        :param memoryGB: Memory size in GB
        :type memoryGB: int
        :return: new request objects

        .. seealso:: :func:``get_os`` for os parameter,
          :func:``get_images`` for image, :func:``get_folder`` for folder,
          :func:``get_networks`` for networks

        .. note:: more information about required attributes
          available in `Virtual Machine <https://wiki.eis.utoronto.ca/x/pgCC>`_

        """
        # validate basic items
        if usage not in ['Prod', 'Test', 'Dev', 'QA']:
            raise VssError('Usage {} not supported'.format(usage))
        if built not in ['clone', 'template', 'image', 'os_install']:
            raise VssError('Built process {} not supported'.format(usage))
        disks = disks if disks else [40]
        folder_valid = self.get_folder(folder)
        networks_valid = [self.get_network(net) for net in networks]
        # generating payload
        json_payload = dict(os=os, built_from=built, bill_dept=bill_dept,
                            cpu=cpu, memory=memoryGB,
                            description=description, folder=folder)
        if name:
            json_payload['name'] = name
        json_payload.update(kwargs)
        json = self.request_v2('/vm', payload=json_payload, method='POST')
        return json.get('data')

    def create_vms(self, count, name, os, built, bill_dept,
                   description, folder, networks, disks,
                   usage='Test', cpu=1, memoryGB=1, **kwargs):
        """
        Creates multiple Virtual Machines. Names are generated
        by appending name_number

        :param count: number of virtual machines to deploy
        :type count: int
        :param name: name of the new virtual machines
        :type name: str
        :param os: Operating system id.
        :type os: str
        :param built: built process
        :param bill_dept: Billing department
        :type bill_dept: str
        :param description: VM description
        :type description: str
        :param folder: Target VM folder moref
        :type folder: str
        :param networks: list of networks morefs
        :type networks: list
        :param disks: list of disk sizes in GB
        :type disks: list
        :param usage: virtual machine usage
        :type usage: str
        :param cpu: vCPU count
        :type cpu: int
        :param memoryGB: Memory size in GB
        :type memoryGB: int
        :return: new request objects

        .. seealso:: :func:``get_os`` for os parameter,
          :func:``get_images`` for image, :func:``get_folder`` for folder,
          :func:``get_networks`` for networks

        .. note:: more information about required attributes
          available in `Virtual Machine <https://wiki.eis.utoronto.ca/x/pgCC>`_

        """
        # validate basic items
        if usage not in ['Prod', 'Test', 'Dev', 'QA']:
            raise VssError('Usage {} not supported'.format(usage))
        if built not in ['clone', 'template', 'image', 'os_install']:
            raise VssError('Built process {} not supported'.format(usage))
        disks = disks if disks else [40]
        folder_valid = self.get_folder(folder)
        networks_valid = [self.get_network(net) for net in networks]
        names = ['%s_%s' % (name, i) for i in range(0, count)]
        # generating payload
        json_payload = dict(os=os, built_from=built, bill_dept=bill_dept,
                            cpu=cpu, memory=memoryGB,
                            description=description, folder=folder,
                            names=names)
        json_payload.update(kwargs)
        json = self.request_v2('/vm', payload=json_payload, method='POST')
        return json.get('data')

    def create_vm_from_image(self, os, image, bill_dept,
                             description, folder, networks, disks,
                             usage='Test', cpu=1, memoryGB=1, **kwargs):
        """
        Creates a new Virtual Machine from OVA or OVF

        :param os: Operating system id.
        :type os: str
        :param image: OVA/OVF filename
        :type image: str
        :param bill_dept: Billing department
        :type bill_dept: str
        :param description: VM description
        :type description: str
        :param folder: Target VM folder moref
        :type folder: str
        :param networks: list of networks morefs
        :type networks: list
        :param disks: list of disk sizes in GB
        :type disks: list
        :param usage: virtual machine usage
        :type usage: str
        :param cpu: vCPU count
        :type cpu: int
        :param memoryGB: Memory size in GB
        :type memoryGB: int
        :return: new request object

        .. seealso:: :func:``get_os`` for os parameter,
          :func:``get_images`` for image, :func:``get_folder`` for folder,
          :func:``get_networks`` for networks.

        .. note:: more information about required attributes
          available in `Virtual Machine <https://wiki.eis.utoronto.ca/x/pgCC>`_
        """
        if usage not in ['Prod', 'Test', 'Dev', 'QA']:
            raise VssError('Usage {} not supported'.format(usage))
        disks = disks if disks else [40]
        # validate basic items
        folder_valid = self.get_folder(folder)
        networks_valid = [self.get_network(net) for net in networks]
        # generate payload
        json_payload = dict(os=os, cpu=cpu, memory=memoryGB,
                            built_from='image', bill_dept=bill_dept,
                            description=description, folder=folder,
                            networks=networks, disks=disks,
                            source_image=image)
        json_payload.update(kwargs)
        json = self.request_v2('/vm', payload=json_payload,
                               method='POST')
        return json.get('data')

    def get_vm_console(self, uuid):
        """
        Produces a one-time URL to Virtual Machine
        console. Virtual machine needs to be powered on
        and user must have a valid vCenter session
        (limitation in the vSphere SOAP API).

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: object
        """
        json = self.request_v2('/vm/' + uuid + '/console')
        return json.get('data')

    def is_vm_template(self, uuid):
        """
        Checks if Virtual Machine is marked as template

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: bool
        """
        json = self.request_v2('/vm/' + uuid + '/template')
        return json.get('data')

    def mark_vm_as_template(self, uuid, **kwargs):
        """
        Marks Virtual Machine as template to freeze changes.
        Templates cannot be modified nor powered on unless marked
        as Virtual Machine.

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: change request object

        .. note:: key words arguments include schedule to process request
                  on a given date and time
        """
        json_payload = dict(value=True)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/' + uuid + '/template',
                               payload=json_payload, method='PUT')
        return json.get('data')

    def get_vm_memory(self, uuid):
        """
        Gets Virtual Machine memory information such as:

        - memoryGB
        - hotAdd
        - quickStats:

          - ballooned
          - compressed
          - consumedOverhead,
          - private
          - shared
          - swapped

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: object

        """
        json = self.request_v2('/vm/' + uuid + '/memory')
        return json.get('data')

    def set_vm_memory(self, uuid, sizeGB, **kwargs):
        """
        Updates Virtual Machine Memory size

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param sizeGB: New memory size in GB
        :type sizeGB: int
        :return: change request object

        .. note:: key words arguments include schedule to process request
         on a given date and time

        """
        payload = dict(value=int(sizeGB))
        payload.update(kwargs)
        json = self.request_v2('/vm/' + uuid + '/memory',
                               payload=payload,
                               method='PUT')
        return json.get('data')

    def get_vm_cpu(self, uuid):
        """
        Get VM cpu information such as:

        - coresPerSocket
        - cpu
        - hotAdd
        - hotRemove
        - quickStats

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: change request object
        """
        json = self.request_v2('/vm/' + uuid + '/cpu')
        return json.get('data')

    def set_vm_cpu(self, uuid, number, **kwargs):
        """
        Updates Virtual Machine CPU count

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param number: New vCPU count
        :type number: int
        :return: change request object

        .. note:: key words arguments include schedule to process request
          on a given date and time

        """
        payload = dict(value=number)
        payload.update(kwargs)
        json = self.request_v2('/vm/' + uuid + '/cpu',
                               payload=payload,
                               method='PUT')
        return json.get('data')

    # Virtual Machine devices
    def get_vm_nics(self, uuid):
        """
        Gets Virtual Machine NICs information.

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: list of objects
        """
        json = self.request_v2('/vm/' + uuid + '/nic')
        nic_numbers = [nic.get('unit') for nic in json.get('data')]
        nics = list()
        for nic in nic_numbers:
            json = self.request_v2('/vm/' + uuid + '/nic/' + nic)
            nics.append({'unit': nic,
                         'data': json['data'][0]})
        return nics

    def get_vm_nic(self, uuid, nic):
        """
        Gets Virtual Machine NIC information such as:

        - connected
        - label
        - macAddress
        - network
        - startConnected
        - type

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param nic: nic number
        :type nic: int
        :return:
        """
        json = self.request_v2('/vm/' + uuid + '/nic/' + str(nic))
        return json.get('data')

    def create_vm_nic(self, uuid, nic, network, **kwargs):
        """
        Creates Virtual Machine NIC

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param nic: Network interface card number
        :type nic: int
        :param network: Network moref to attach
        :type network: str
        :return: change request object

        """
        json_payload = dict(value=network)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/{uuid}/nic/{number}'.format(uuid=uuid,
                                                                number=nic),
                               method='POST', payload=json_payload)
        return json.get('data')

    def delete_vm_nic(self, uuid, nic, **kwargs):
        """
        Deletes Virtual Machine NIC unit

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param nic: Network interface card number
        :type nic: int
        :return: change request object

        .. note:: key words arguments include schedule to process request
          on a given date and time

        """
        json_payload = dict(attribute='state',
                            value='delete')
        json_payload.update(kwargs)
        json = self.request_v2('/vm/{uuid}/nic/{number}'.format(uuid=uuid,
                                                                number=nic),
                               method='DELETE', payload=json_payload)
        return json.get('data')

    def update_vm_nic_network(self, uuid, nic, network, **kwargs):
        """
        Updates Virtual Machine network on a given nic

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param nic: Network interface card number
        :type nic: int
        :param network: new network moref
        :type network: str
        :return: change request object

        .. note:: key words arguments include schedule to process request
          on a given date and time

        """
        json_payload = dict(attribute='network',
                            value=network)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/{uuid}/nic/{number}'.format(uuid=uuid,
                                                                number=nic),
                               method='PUT', payload=json_payload)
        return json.get('data')

    def update_vm_nic_type(self, uuid, nic, type, **kwargs):
        """
        Updates Virtual Machine NIC type

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param nic: Network interface card number
        :type nic: int
        :param type: new nic type (E1000e, E1000, VMXNET3, VMXNET2)
        :type type: str
        :return: change request object

        .. note:: key words arguments include schedule to process request
          on a given date and time

        """
        if type not in ['VMXNET2', 'VMXNET3', 'E1000', 'E1000e']:
            raise VssError('Unsupported NIC type')

        json_payload = dict(attribute='type',
                            value=type)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/{uuid}/nic/{number}'.format(uuid=uuid,
                                                                number=nic),
                               method='PUT', payload=json_payload)
        return json.get('data')

    def update_vm_nic_state(self, uuid, nic, state, **kwargs):
        """
        Updates Virtual Machine NIC state

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param nic: Network interface card number
        :type nic: int
        :param state: new nic state (connect, disconnect)
        :type state: str
        :return: change request object

        .. note:: key words arguments include schedule to process request
          on a given date and time

        """
        if state not in ['connect', 'disconnect']:
            raise VssError('Unsupported NIC state')

        json_payload = dict(attribute='state',
                            value=state)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/{uuid}/nic/{number}'.format(uuid=uuid,
                                                                number=nic),
                               method='PUT', payload=json_payload)
        return json.get('data')

    def get_vm_cds(self, uuid):
        """
        Returns Virtual Machine CD/DVD devices
        available.

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: list of objects
        """
        json = self.request_v2('/vm/' + uuid + '/cd')
        cd_units = [cd.get('unit') for cd in json.get('data')]
        cds = list()
        for cd in cd_units:
            data = self.get_vm_cd(uuid, cd)
            cds.append({'unit': cd,
                        'data': data[0]})
        return cds

    def get_vm_cd(self, uuid, cd):
        """
        Returns Virtual Machine CD/DVD given unit
        information such as:

        - backing
        - connected
        - controller
        - description
        - label

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param cd: CD/DVD unit number
        :type cd: int
        :return: object

        """
        json = self.request_v2('/vm/' + uuid + '/cd/' + str(cd))
        return json.get('data')

    def get_vm_disks(self, uuid):
        """
        Returns Virtual Machine available disks

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: list of objects

        """
        json = self.request_v2('/vm/' + uuid + '/disk')
        disk_units = [disk.get('unit') for disk in json.get('data')]
        disks = list()
        for disk in disk_units:
            data = self.get_vm_disk(uuid, disk)
            disks.append({'unit': disk,
                          'data': data[0]})
        return disks

    def get_vm_disk(self, uuid, disk):
        """
        Gets Virtual Machine disk data such as:

        - capacity
        - controller
        - description
        - label
        - shares
        - filenName

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param disk: Virtual Machine disk number
        :type disk: int
        :return: object

        """
        json = self.request_v2('/vm/' + uuid + '/disk/' + str(disk))
        return json.get('data')

    def is_powered_on_vm(self, uuid):
        """
        Checks if given Virtual Machine is powered
        On.

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: bool
        """
        json = self.request_v2('/vm/' + uuid + '/state')
        power_state = json.get('data').get('powerState')
        if power_state:
            return power_state == 'poweredOn'
        else:
            return False

    def reboot_vm(self, uuid, **kwargs):
        """
        Graceful reboot VM. This method sends a reboot signal
        via VMware Tools to the Guest Operating system,
        thus VMware Tools is required up-to-date
        and running on VM.

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: change request object

        .. note:: key words arguments include schedule to process request
          on a given date and time

        """
        json = self.update_vm_state(uuid=uuid, state='reboot', **kwargs)
        return json.get('data')

    def reset_vm(self, uuid, **kwargs):
        """
         Hard reset VM. This method resets a given Virtual Machine.
         This method is equivalent to power_off_vm and power_on_vm

         :param uuid: Virtual Machine Uuid
         :type uuid: str
         :return: change request object

         .. note:: key words arguments include schedule to process request
           on a given date and time

         """
        json = self.update_vm_state(uuid=uuid, state='reset', **kwargs)
        return json

    def power_off_vm(self, uuid, **kwargs):
        """
        Power Off VM. This method powers Off given virtual
        machine.

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: change request object

        .. note:: key words arguments include schedule to process request
          on a given date and time

        """
        json = self.update_vm_state(uuid=uuid, state='poweredOff', **kwargs)
        return json

    def power_on_vm(self, uuid, **kwargs):
        """
        Power On VM. This method powers on given virtual
        machine.

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: change request object

        .. note:: key words arguments include schedule to process request
          on a given date and time

        """
        json = self.update_vm_state(uuid=uuid, state='poweredOn', **kwargs)
        return json

    def shutdown_vm(self, uuid, **kwargs):
        """
        Graceful shutdown VM. This method sends a shutdown signal
        via VMware Tools to the Guest Operating system,
        thus VMware Tools is required up-to-date
        and running on VM.

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: change request object

        .. note:: key words arguments include schedule to process request
          on a given date and time

        """
        json = self.update_vm_state(uuid=uuid, state='shutdown', **kwargs)
        return json

    def rename_vm(self, uuid, name, **kwargs):
        """
        Update Virtual Machine name. This do not change
        the VSS prefix ``YYMM{P|Q|D|T}-VMName``.

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param name: New virtual machine name. Do not
         include VSS prefix.
        :return: change request object

        .. note:: key words arguments include schedule to process request
          on a given date and time

        """
        json_payload = dict(name=name)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/' + uuid + '/name', method='PUT',
                               payload=json_payload)

        return json.get('data')

    # Virtual Machine Notes
    def get_vm_notes(self, uuid):
        """
        Get Virtual Machine client notes.
        Metadata available for users to manage.

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: list of key value notes
        """
        json = self.request_v2('/vm/' + uuid + '/note/client')
        return json.get('data')

    def update_vm_note(self, uuid, notes_dict, **kwargs):
        """
        Update Virtual Machine client notes. Notes are
        stored as key-value metadata items.

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param notes_dict:
        :type notes_dict: dict
        :return: change request object

        .. note:: key words arguments include schedule to process request
          on a given date and time

        """
        json_payload = dict(value=notes_dict)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/' + uuid + '/note/client',
                               method='PUT', payload=json_payload)
        return json.get('data')

    # Virtual Machine VSS attributes
    def get_vm_vss_admin(self, uuid):
        """
        Get Virtual Machine administrator
        This is part of the VSS metadata added to the
        VM annotation.

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: dict with phone, name and email of
         vm admin

        """
        json = self.request_v2('/vm/' + uuid + '/vss/admin')
        return json.get('data')

    def update_vm_vss_admin(self, uuid, name, phone, email, **kwargs):
        """
        Update Virtual Machine administrator contact
        info.

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :param name: Full name of VM admin
        :type name: str
        :param phone: Valid phone number of VM admin
        :type phone: str
        :param email: Valid email address of VM admin
        :type email: str
        :return: change request object

        .. note:: key words arguments include schedule to process request
          on a given date and time
        """
        json_payload = dict(value=':'.join([name, phone, email]))
        json_payload.update(kwargs)
        json = self.request_v2('/vm/' + uuid + '/vss/admin', method='POST',
                               payload=json_payload)
        return json.get('data')

    def get_vm_vss_usage(self, uuid):
        """
        Get Virtual Machine Usage.
        This is part of the VSS metadata added to the
        VM annotation.

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: dict

        """
        json = self.request_v2('/vm/' + uuid + '/vss/usage')
        return json.get('data')

    def get_vm_vss_changelog(self, uuid):
        """
        Get Virtual Machine change log. Maximum change
        log entries are 9.
        This is part of the VSS metadata added to the
        VM annotation.

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: list of changelog entries as dict

        """
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
        """
        Get Virtual Machine informational contacts.
        This is part of the VSS metadata added to the
        VM annotation

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: list of email addresses if any

        """
        json = self.request_v2('/vm/' + uuid + '/vss/inform')
        return json.get('data')

    def update_vm_vss_inform(self, uuid, value, append, **kwargs):
        json_payload = dict(value=value, append=append)
        json_payload.update(kwargs)
        json = self.request_v2('/vm/' + uuid + '/vss/inform',
                               method='PUT', payload=json_payload)
        return json.get('data')

    def get_vm_vss_requested(self, uuid):
        """
        Get Virtual Machine requested timestamp
        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: timestamp in str or none if unknown

        """
        json = self.request_v2('/vm/' + uuid + '/vss')
        return json.get('data').get('requested')

    # Virtual Machine summary
    def get_vm_storage(self, uuid):
        """
        Get Virtual Machine storage summary

        :param uuid: Virtual Machine Uuid
        :type uuid: str
        :return: dict with:

        - uncommittedGB
        - provisionedGB
        - committedGB
        - unsharedGB

        """
        json = self.get_vm(uuid)
        return json.get('storage')

    def request_v2(self, url, headers=None, params=None, payload=None,
                   method='GET', auth=None, timeout=60):
        if not headers:
            headers = {'Content-Type': 'application/json',
                       'User-Agent': 'pyvss/{}'.format(__version__)}
        if not url.startswith('http'):
            url = self.api_endpoint + url
        auth = HTTPBasicAuth(self.api_token, '') if not auth else auth
        try:
            if method == 'POST':
                resp = requests.post(url, headers=headers,
                                     timeout=timeout, auth=auth, json=payload)
                json = self.process_response(resp)
            elif method == 'DELETE':
                resp = requests.delete(url, data=json_module.dumps(params),
                                       headers=headers,
                                       timeout=timeout, auth=auth,
                                       json=payload)
                json = self.process_response(resp)
            elif method == 'PUT':
                resp = requests.put(url, headers=headers, params=params,
                                    timeout=timeout, auth=auth,
                                    json=payload)
                json = self.process_response(resp)
            elif method == 'GET':
                resp = requests.get(url, headers=headers, params=params,
                                    timeout=timeout, auth=auth,
                                    json=payload)
                json = resp.json()
            elif method == 'OPTIONS':
                resp = requests.options(url, headers=headers, params=params,
                                        timeout=timeout, auth=auth,
                                        json=payload)
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
        """
        Processes response in case of status code

        equals 204
        :param response: request.response object
        :return: dict
        """
        if response.status_code == 204:
            return {'status': response.status_code}
        else:
            return response.json()

    def wait_for_request(self, request_url, request_attr,
                         required_status, max_tries=6):
        """
        Waits for request to be in any given status

        :param request_url: Request URL to check periodically
        :type request_url: str
        :param request_attr: Attribute to return upon completion
        :type request_attr: str
        :param required_status: Required request status.
        :type required_status: str
        :param max_tries: Maximum tries to check. Defaults to 6 and
         every try waits for 10 secs
        :type max_tries: int
        :return: False if failed or the type of attribute requested

        """
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


def run_main():
    """
    Simple wrapper to execute manager functions

    Checks for VSS_API_TOKEN environment variable

    Example::

        python pyvss/manager.py get_vms 'summary=1&name=pm'

    """
    import sys
    import pprint
    api_token = os.environ.get('VSS_API_TOKEN')
    if not api_token:
        raise VssError('Specify environment variable VSS_API_TOKEN')
    manager = VssManager(api_token)
    fname = sys.argv[1]
    pprint.pprint(getattr(manager, fname)(*sys.argv[2:]), indent=1)

if __name__ == '__main__':
    run_main()
