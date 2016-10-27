#!/usr/bin/python
# -*- coding: utf-8 -*-
from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails,ConnectivityContext
from cloudshell.networking.cisco.iosxr.cisco_iosxr_resource_driver import CiscoIOSXRResourceDriver
import re


def create_context():
    context = ResourceCommandContext()
    context.resource = ResourceContextDetails()
    context.resource.name = 'iosxr45'
    context.reservation = ReservationContextDetails()
    context.reservation.reservation_id = 'test_id'
    context.reservation.owner_user = 'admin'
    context.reservation.owner_email = 'fake@qualisystems.com'
    context.reservation.environment_path ='admin_Environment-6-7-2016_15-25_19-07-2016_13-46-UTC'
    context.reservation.environment_name = 'admin_Environment-6-7-2016_15-25_19-07-2016_13-46-UTC'
    context.reservation.domain = 'Global'
    context.resource.attributes = {}
    context.resource.attributes['CLI Connection Type'] = 'SSH'
    context.resource.attributes['User'] = ''
    context.resource.attributes['AdminUser'] = ''
    context.resource.attributes['Console Password'] = '3M3u7nkDzxWb0aJ/IZYeWw=='
    context.resource.attributes['Password'] = 'PgkOScppedeEbHGHdzpnrw=='
    context.resource.attributes['Enable Password'] = 'PgkOScppedeEbHGHdzpnrw=='
    context.resource.address = '192.168.73.45'
    context.resource.attributes['SNMP Version'] = '2'
    context.resource.attributes['SNMP Read Community'] = 'public'
    context.resource.attributes['Model'] = ''
    context.resource.attributes['AdminPassword'] ='DxTbqlSgAVPmrDLlHvJrsA=='
    context.resource.attributes['Vendor'] = 'Cisco'
    return context


if __name__ == '__main__':
    context = create_context()
    driver = CiscoIOSXRResourceDriver()

    #response = driver.get_inventory(context)
    #res = driver.save(context, 'tftp://82.80.35.226/test', 'startup')
    #
    #res = driver.save(context, 'flash:/config_backup/','startup')
    #C:/Users/Administrator/Desktop/test
    #tftp://12.30.245.98/test/test.txt
    #res = driver.restore(context,'flash:/config_backup/vrpcfg.zip', 'startup', 'override')

    response = driver.get_inventory(context)
    #res = driver.save(context, 'tftp://82.80.35.226/test', 'startup')

    #res = driver.ApplyConnectivityChanges(context, request)
    #res=driver.update_firmware(context,'1.1.1.1','flash:/config_backup/')
    #print driver.send_custom_command(context, "display version")
    # print response
