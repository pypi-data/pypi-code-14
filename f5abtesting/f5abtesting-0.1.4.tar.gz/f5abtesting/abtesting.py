#!/usr/bin/python
# -*- coding:utf-8 -*-
# import getpass
import re
import os
from f5.bigip import ManagementRoot


class f5abtesting(object):
    def __init__(self, bigip, bigip_username, bigip_password):
        self.bigip = bigip
        self.bigip_username = bigip_username
        self.bigip_password = bigip_password
        self.mgmt = ManagementRoot(self.bigip, self.bigip_username, self.bigip_password)

    # function to undeploy the f5abtesting
    def undeploy(self, vs_name, cleanup):
        pool_b_name = vs_name + '_pool_b'
        dg_region2b = vs_name + '_dg_region2b'
        dg_ip2region = vs_name + '_dg_ip2region'
        irules_ab = vs_name + '_irules_ab'
        irules_ab_fullpath = '/Common/' + irules_ab
        vs_tmp = self.mgmt.tm.ltm.virtuals.virtual.load(name=vs_name, partition='Common')
        vs_tmp_raw = vs_tmp.raw
        if 'rules' in vs_tmp_raw:
            print vs_tmp_raw['rules']
            if irules_ab_fullpath in vs_tmp_raw['rules']:
                print irules_ab + ' bound on ' + vs_name + ', unbind it'
                vs_tmp_irules = vs_tmp.rules
                vs_tmp_irules.remove(irules_ab_fullpath)
                print vs_tmp_irules
                vs_tmp.update()
                print irules_ab + ' unbound from ' + vs_name
            else:
                print irules_ab + ' is not bound on ' + vs_name
        else:
            print 'No iRules bound on ' + vs_name
        if cleanup == 'cleanup':
            print 'clean up f5abtesting configure for ' + vs_name
            if self.mgmt.tm.ltm.rules.rule.exists(name=irules_ab):
                print 'deleting ' + irules_ab
                irules_tmp = self.mgmt.tm.ltm.rules.rule.load(name=irules_ab)
                irules_tmp.delete()
                print 'done'
            if self.mgmt.tm.ltm.pools.pool.exists(name=pool_b_name, partition='Common'):
                print 'deleting ' + pool_b_name
                pool_tmp = self.mgmt.tm.ltm.pools.pool.load(name=pool_b_name, partition='Common')
                for member in pool_tmp.members_s.get_collection():
                    print member.name
                    self.pool_b_mbr_del(vs_name, member.name)
                print 'done'
            if self.mgmt.tm.ltm.data_group.internals.internal.exists(name=dg_region2b):
                print 'deleting ' + dg_region2b
                datagroup_tmp = self.mgmt.tm.ltm.data_group.internals.internal.load(name=dg_region2b,
                                                                                    partition='Common')
                datagroup_tmp.delete()
                print 'done'
            if self.mgmt.tm.ltm.data_group.internals.internal.exists(name=dg_ip2region):
                print 'deleting ' + dg_ip2region
                datagroup_tmp = self.mgmt.tm.ltm.data_group.internals.internal.load(name=dg_ip2region,
                                                                                    partition='Common')
                datagroup_tmp.delete()
                print 'done'
            print 'clean up finished'

    # function to deploy the f5abtesting
    def deploy(self, vs_name):
        pool_b_name = vs_name + '_pool_b'
        dg_region2b = vs_name + '_dg_region2b'
        dg_ip2region = vs_name + '_dg_ip2region'
        irules_ab = vs_name + '_irules_ab'
        irules_ab_fullpath = '/Common/' + irules_ab
        if not self.mgmt.tm.ltm.pools.pool.exists(name=pool_b_name, partition='Common'):
            print pool_b_name + ' does not exist, use pool_b_mbr_add to create and add member into it.'
        elif not self.mgmt.tm.ltm.data_group.internals.internal.exists(name=dg_region2b):
            print dg_region2b + ' does not exist, use region2b_assign to create and add record into it.'
        elif not self.mgmt.tm.ltm.data_group.internals.internal.exists(name=dg_ip2region):
            print dg_ip2region + ' does not exist, use init_ip2region to create it.'
        elif not self.mgmt.tm.ltm.rules.rule.exists(name=irules_ab):
            print irules_ab + ' does not exist, use init_irules to create it.'
        else:
            vs_tmp = self.mgmt.tm.ltm.virtuals.virtual.load(name=vs_name, partition='Common')
            vs_tmp_raw = vs_tmp.raw
            if 'rules' in vs_tmp_raw:
                print vs_tmp_raw['rules']
                if irules_ab_fullpath in vs_tmp_raw['rules']:
                    print irules_ab + ' already bound on ' + vs_name
                else:
                    vs_tmp_irules = vs_tmp.rules
                    irules_record_file = vs_name + '_irules_records.bak'
                    f = open(irules_record_file, 'w')
                    for s in vs_tmp_irules:
                        f.write(s + '\n')
                    f.close()
                    vs_tmp_irules.insert(0, irules_ab_fullpath)
                    vs_tmp.update()
                    print irules_ab + ' prepended on vs ' + vs_name
            else:
                print 'No iRules bound on ' + vs_name + ', binding ' + irules_ab
                vs_tmp.rules = [irules_ab_fullpath]
                vs_tmp.update()
                print irules_ab + ' bound on ' + vs_name

    @staticmethod
    def validip(address):
        parts = address.split(".")
        if len(parts) != 4:
            return False
        for item in parts:
            if not 0 <= int(item) <= 255:
                return False
        return True

    def valid_pool_member(self, pool_member):
        pool_member_parts = pool_member.split(':')
        if len(pool_member_parts) != 2:
            return False
        if self.validip(pool_member_parts[0]) and (0 <= int(pool_member_parts[1]) <= 65535):
            return True
        else:
            return False

    # function pool_b_mbr_del to delete a pool member from pool B
    def pool_b_mbr_del(self, vs_name, pool_b_member):
        pool_b_name = vs_name + '_pool_b'
        if self.mgmt.tm.ltm.pools.pool.exists(name=pool_b_name, partition='Common'):
            pool_b = self.mgmt.tm.ltm.pools.pool.load(name=pool_b_name, partition='Common')
            if pool_b.members_s.members.exists(name=pool_b_member, partition='Common'):
                pool_b_members = pool_b.members_s.get_collection()
                if len(pool_b_members) > 1:
                    pool_b_member_tmp = pool_b.members_s.members.load(name=pool_b_member, partition='Common')
                    pool_b_member_tmp.delete()
                    print pool_b_member + ' removed from ' + pool_b_name
                else:
                    pool_b.delete()
                    print pool_b_member + ' is the last member, delete ' + pool_b_name
                # check pool_b_member is in pool_a
                vs_tmp = self.mgmt.tm.ltm.virtuals.virtual.load(name=vs_name, partition='Common')
                vs_tmp_raw = vs_tmp.raw
                pool_a_s = vs_tmp_raw['pool'].split('/')
                pool_a = self.mgmt.tm.ltm.pools.pool.load(name=pool_a_s[2], partition=pool_a_s[1])
                for pool_a_member in pool_a.members_s.get_collection():
                    # print pool_a_member.raw
                    # Retrieve full path of the pool member, as the name could be different from IP:port
                    pool_a_member_path = pool_a_member.fullPath
                    # check if the IP:port already in pool_a's member list, enable it if exists
                    if pool_a_member_path.split('/')[2] == pool_b_member:
                        print pool_b_member + ' is also in ' + pool_a.name + ', enable it ...'
                        pool_a_member_tmp = pool_a.members_s.members.load(name=pool_a_member.name,
                                                                          partition=pool_a_s[1])
                        pool_a_member_tmp.session = 'user-enabled'
                        pool_a_member_tmp.update()
                        print pool_b_member + ' enabled in ' + pool_a.name
            else:
                print pool_b_member + ' does not in ' + pool_b_name

    # function pool_b_mbr_add to add pool member into pool B
    def pool_b_mbr_add(self, vs_name, pool_b_member):
        vs_tmp = self.mgmt.tm.ltm.virtuals.virtual.load(name=vs_name, partition='Common')
        vs_tmp_raw = vs_tmp.raw
        pool_a_s = vs_tmp_raw['pool'].split('/')
        pool_a = self.mgmt.tm.ltm.pools.pool.load(name=pool_a_s[2], partition=pool_a_s[1])
        # print pool_a.raw
        pool_a_monitor = pool_a.monitor
        for pool_a_member in pool_a.members_s.get_collection():
            # print pool_a_member.raw
            # Retrieve full path of the pool member, as the name could be different from IP:port
            pool_a_member_path = pool_a_member.fullPath
            # check if the IP:port already in pool_a's member list
            if pool_a_member_path.split('/')[2] == pool_b_member:
                print pool_b_member + ' already in ' + pool_a.name + ', disable it ...'
                pool_a_member_tmp = pool_a.members_s.members.load(name=pool_a_member.name, partition=pool_a_s[1])
                # print pool_a_member_tmp.raw
                # print 'session:' + pool_a_member_tmp.session
                # print 'state:' + pool_a_member_tmp.state
                pool_a_member_tmp.session = 'user-disabled'
                pool_a_member_tmp.update()
                print pool_b_member + ' disabled in ' + pool_a.name
        pool_list = self.mgmt.tm.ltm.pools.get_collection()
        pool_name_list = []
        for pool in pool_list:
            pool_name_list.append(pool.name)
        # print pool_name_list
        pool_b_name = vs_name + '_pool_b'
        if pool_b_name in pool_name_list:
            print pool_b_name + ' already exist, add pool member ' + pool_b_member
            pool_b = self.mgmt.tm.ltm.pools.pool.load(name=pool_b_name, partition='Common')
            if not (pool_b.members_s.members.exists(name=pool_b_member, partition='Common')):
                pool_b_member_tmp = pool_b.members_s.members.create(name=pool_b_member, partition='Common')
                print pool_b_member + ' added in ' + pool_b_name
            else:
                print pool_b_member + ' already exists in ' + pool_b_name
        else:
            print pool_b_name + ' does not exist, create ' + pool_b_name + ' and add pool member ' + pool_b_member
            pool_b = self.mgmt.tm.ltm.pools.pool.create(name=pool_b_name, partition='Common')
            # print pool_b.raw
            pool_b.monitor = pool_a_monitor
            pool_b.update()
            print pool_b_name + ' created '
            pool_b_member_tmp = pool_b.members_s.members.create(name=pool_b_member, partition='Common')
            print 'added pool member ' + pool_b_member

    # function pool_b_list to list member list of pool b
    def pool_b_list(self, vs_name):
        pool_b_name = vs_name + '_pool_b'
        if self.mgmt.tm.ltm.pools.pool.exists(name=pool_b_name, partition='Common'):
            pool_b = self.mgmt.tm.ltm.pools.pool.load(name=pool_b_name, partition='Common')
            print 'Here is the member list of ' + pool_b_name + ':'
            for member in pool_b.members_s.get_collection():
                print 'member:' + member.name + ' status:' + member.session
        else:
            print pool_b_name + ' does not exist...'

    # function region2b_remove to remove  region from B testing pool
    def region2b_remove(self, vs_name, region_name):
        dg_list = self.mgmt.tm.ltm.data_group.internals.get_collection()
        dg_name_list = []
        for dg in dg_list:
            dg_name_list.append(dg.name)
        print dg_name_list
        dg_region2b = vs_name + '_dg_region2b'
        dg_region2b_record = {'name': region_name}
        if dg_region2b in dg_name_list:
            print dg_region2b + ' exists,  removing ' + region_name + ' ...'
            dg_tmp = self.mgmt.tm.ltm.data_group.internals.internal.load(name=dg_region2b)
            print dg_tmp.records
            dg_records = dg_tmp.records
            if dg_region2b_record in dg_records:
                if len(dg_records) > 1:
                    dg_records.remove(dg_region2b_record)
                    dg_tmp.update()
                    print dg_region2b + ' updated ...'
                else:
                    print 'The last region, remove the datagroup ' + dg_region2b
                    dg_tmp.delete()
            else:
                print region_name + ' does not exist ...'
        else:
            print dg_region2b + ' does not exist ...'

    # function region2b_assign to assign region for B testing
    def region2b_assign(self, vs_name, region_name):
        dg_list = self.mgmt.tm.ltm.data_group.internals.get_collection()
        dg_name_list = []
        for dg in dg_list:
            dg_name_list.append(dg.name)
        print dg_name_list
        dg_region2b = vs_name + '_dg_region2b'
        dg_region2b_record = {'name': region_name}
        if dg_region2b in dg_name_list:
            print dg_region2b + ' already exists,  updating ...'
            dg_tmp = self.mgmt.tm.ltm.data_group.internals.internal.load(name=dg_region2b)
            print dg_tmp.records
            dg_records = dg_tmp.records
            dg_records.append(dg_region2b_record)
            dg_tmp.update()
            print dg_region2b + ' updated ...'
        else:
            print dg_region2b + ' does not exist,  creating ...'
            dg_tmp = self.mgmt.tm.ltm.data_group.internals.internal.create(name=dg_region2b, type='string',
                                                                           records=[dg_region2b_record])
            print dg_tmp.records
            print dg_region2b + ' created ...'

    # function region2b_list to list region2b datagroup
    def region2b_list(self, vs_name):
        dg_region2b = vs_name + '_dg_region2b'
        if self.mgmt.tm.ltm.data_group.internals.internal.exists(name=dg_region2b):
            dg_tmp = self.mgmt.tm.ltm.data_group.internals.internal.load(name=dg_region2b)
            print 'Here is the record of ' + dg_region2b + ':'
            dg_records = dg_tmp.records
            for record in dg_records:
                for (k, v) in record.items():
                    print v
        else:
            print dg_region2b + ' does not exist ...'

    # function init_irules to create irules for ab traffic distribution
    def init_irules(self, vs_name, irules_tmp_file):
        if not (os.path.isfile(irules_tmp_file)):
            print 'File ' + irules_tmp_file + ' does not exist !'
        else:
            irules_file = open(irules_tmp_file)
            try:
                irules_text = irules_file.read()
                strinfo = re.compile('ab_demo')
                irules_text = strinfo.sub(vs_name, irules_text)
            finally:
                irules_file.close()
            irules_ab = vs_name + '_irules_ab'
            if self.mgmt.tm.ltm.rules.rule.exists(name=irules_ab):
                print irules_ab + ' already exists, updating ... '
                rule1 = self.mgmt.tm.ltm.rules.rule.load(name=irules_ab)
                rule1.apiAnonymous = irules_text
                rule1.update()
            else:
                print irules_ab + ' does not exist, creating ... '
                rule1 = self.mgmt.tm.ltm.rules.rule.create(name=irules_ab, partition='Common', apiAnonymous=irules_text)
                print rule1.name + ' created '
            rule1 = self.mgmt.tm.ltm.rules.rule.load(name=irules_ab)
            print rule1.name + ' created '
            print rule1.apiAnonymous

    # function init_ip2region to create ip address to region mapping
    def init_ip2region(self, vs_name, ip2region_file):
        dg_records = []
        if not (os.path.isfile(ip2region_file)):
            print 'File ' + ip2region_file + ' does not exist !'
        else:
            for line in open(ip2region_file):
                dg_str = line.split()
                dg_record = {'data': dg_str[0], 'name': dg_str[1]}
                dg_records.append(dg_record)
            print dg_records
            dg_list = self.mgmt.tm.ltm.data_group.internals.get_collection()
            dg_name_list = []
            for dg in dg_list:
                dg_name_list.append(dg.name)
            print dg_name_list
            dg_ip2region = vs_name + '_dg_ip2region'
            if dg_ip2region in dg_name_list:
                print dg_ip2region + ' already exists, deleting ...'
                dg_tmp = self.mgmt.tm.ltm.data_group.internals.internal.load(name=dg_ip2region)
                dg_tmp.delete()
                print dg_ip2region + ' deleted'
                print ' creating a new version ...'
                dg_new = self.mgmt.tm.ltm.data_group.internals.internal.create(name=dg_ip2region, type='ip',
                                                                               records=dg_records)
                print 'Datagroup ' + dg_new.name + ' created'
            else:
                print dg_ip2region + ' does not exist, creating ...'
                dg_new = self.mgmt.tm.ltm.data_group.internals.internal.create(name=dg_ip2region, type='ip',
                                                                               records=dg_records)
                print 'Datagroup ' + dg_new.name + ' created'

            dg_new = self.mgmt.tm.ltm.data_group.internals.internal.load(name=dg_ip2region)
            print dg_new.records
