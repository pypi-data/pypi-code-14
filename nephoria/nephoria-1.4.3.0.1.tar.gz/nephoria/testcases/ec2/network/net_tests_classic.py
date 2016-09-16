#!/usr/bin/python
# Software License Agreement (BSD License)
#
# Copyright (c) 2009-2011, Eucalyptus Systems, Inc.
# All rights reserved.
#
# Redistribution and use of this software in source and binary forms, with or
# without modification, are permitted provided that the following conditions
# are met:
#
#   Redistributions of source code must retain the above
#   copyright notice, this list of conditions and the
#   following disclaimer.
#
#   Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the
#   following disclaimer in the documentation and/or other
#   materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author:

__author__ =  'matt.clark@eucalyptus.com'
'''
Test case class to test points of network security groups
See individual test descriptions for test objectives.
test1:
    Definition:
        Create test instances within each zone within security group1. This security group is authorized for
        ssh access from 0.0.0.0/0.
        This test attempts the following:
            -To run an instance in each zone and confirm it reaches 'running' state.
            -Confirm the instance is ping-able from the cc within a given timeout
            -Establish and verify an ssh session directly from the local machine running this test.
            -Place ssh key on instance for later use
            -Add instance to global 'group1_instances'

test2:
    Definition:
        This test attempts to create an instance in each within security group2 which should not
        be authorized for any remote access (outside of the CC).
        The test attempts the following:
            -To run an instance in each zone and confirm it reaches 'running' state.
            -Confirm the instance is ping-able from the cc within a given timeout
            -Establish and verify an ssh session using the cc as a proxy.
            -Place ssh key on instance for later use
            -Add instance to global 'group2_instances'

test3:
    Definition:
        This test attempts to set up security group rules between group1 and group2 to authorize group2 access
        from group1. If use_cidr is True security groups will be setup using cidr notication ip/mask for each instance in
        group1, otherwise the entire source group 1 will authorized.
        the group will be
        Test attempts to:
            -Authorize security groups for inter group private ip access.
            -Iterate through each zone and attempt to ssh from an instance in group1 to an instance in group2 over their
                private ips.

test4:
    Definition:
        Test attempts to verify that the local machine cannot ssh to the instances within group2 which is not authorized
        for ssh access from this source.

test5 (Multi-zone/cluster env):
    Definition:
        This test attempts to check connectivity for instances in the same security group, but in different zones.
        Note: This test requires the CC have tunnelling enabled, or the CCs in each zone be on same
        layer 2 network segment.
        Test attempts to:
            -Iterate through each zone and attempt to ssh from an instance in group1 to an instance in a separate zone
             but same security group1 over their private ips.

test 6 (Multi-zone/cluster env):
    Definition:
        This test attempts to set up security group rules between group1 and group2 to authorize group2 access
        from group1 across different zones.
        If no_cidr is True security groups will be setup using cidr notication ip/mask for each instance in
        group1, otherwise the entire source group 1 will authorized.
        the group will be
        Note: This test requires the CC have tunnelling enabled, or the CCs in each zone be on same
        layer 2 network segment.
        Test attempts to:
            -Authorize security groups for inter group private ip access.
            -Iterate through each zone and attempt to ssh from an instance in group1 to an instance in group2 over their
             private ips.


'''

#todo: Make use of CC optional so test can be run with only creds and non-admin user.
# CC only provides additional point of debug so can be removed from test for non-euca testing
#todo: Allow test to run with an admin and non-admin account, so debug can be provided through admin and test can
# be run under non-admin if desired.

from boto.ec2.instance import Instance
from paramiko import SSHException
from nephoria.testcase_utils.cli_test_runner import CliTestRunner, SkipTestException
from nephoria.testcase_utils import wait_for_result, WaitForResultException
from nephoria.testcontroller import TestController
from nephoria.aws.ec2.euinstance import EuInstance
from cloud_utils.net_utils.sshconnection import SshConnection
from cloud_utils.net_utils.sshconnection import CommandExitCodeException, CommandTimeoutException
from cloud_utils.log_utils import red, get_traceback


from boto.exception import EC2ResponseError
from cloud_utils.net_utils import test_port_status
from cloud_utils.log_utils import get_traceback
import copy
import socket
import time
import os
import re
import sys
try:
    from cloud_admin.backends.network.midget import Midget
except ImportError as IE:
    sys.stderr.write('Failed to import midonet get interface. Err:"{0}"'.format(IE))


class TestZone():
    def __init__(self, zonename):
        self.name = zonename
        self.zone = zonename
        self.test_instance_group1 = None
        self.test_instance_group2 = None


class MidoError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NetTestsClassic(CliTestRunner):

    '''
    self._vpc_backend = None

    '''
    def post_init(self, *args, **kwargs):
        self.cc_last_checked = time.time()

    @property
    def subnet_id(self):
        if hasattr(self.args, 'subnet_id'):
            return self.args.subnet_id
        return None

    @property
    def test_controller(self):
        tc = getattr(self, '_test_controller', None)
        if not tc:
            clc_ip = self.args.clc
            environment_file = self.args.environment_file
            clc_pw = self.args.password
            test_account = self.args.test_account
            test_user = self.args.test_user
            log_level = getattr(self.args, 'log_level', 'DEBUG')
            tc = TestController(hostname=clc_ip, environment_file=environment_file, password=clc_pw,
                                log_level=log_level, clouduser_name=test_user, clouduser_account=test_account)
            setattr(self, '_test_controller', tc)
        return tc

    @test_controller.setter
    def test_controller(self, value):
        if value is None or isinstance(value, TestController):
            setattr(self, '_test_controller', value)
        else:
            raise ValueError('Can only set testcontroller to type TestController or None, '
                             'got:"{0}/{1}"'.format(value, type(value)))

    @property
    def user(self):
        return self.test_controller.user
    
    @property
    def admin(self):
        return self.test_controller.admin
    
    @property
    def sysadmin(self):
        return self.test_controller.sysadmin
    
    @property
    def keypair(self):
        kp = getattr(self, '_keypair', None)
        if not kp:
            try:
                keys = self.user.ec2.get_all_current_local_keys()
                if keys:
                    kp = keys[0]
                else:
                    kp = self.user.ec2.create_keypair_and_localcert(
                        "{0}_key_{1}".format(self.name, time.time()))
                setattr(self, '_keypair', kp)
            except Exception, ke:
                raise Exception("Failed to find/create a keypair, error:" + str(ke))
        return kp 
        
    @property
    def zones(self):
        zones = getattr(self, '_zones', None)
        if not zones:
            ### Create local zone list to run nephoria_unit_tests in
            if self.args.zone:
                zones = str(self.args.zone).replace(',',' ')
                zones = zones.split()
            else:
                zones = self.user.ec2.get_zone_names()
            if not zones:
                raise RuntimeError('No zones found to run this test?')
            self.log.debug('Running test against zones:' + ",".join(zones))
            setattr(self, '_zones', zones)
        return zones

    def setup_test_security_groups(self):
        ### Add and authorize security groups
        group1 = self.group1
        group2 = self.group2
        if self.group1:
            try:
                self.group1 = self.user.ec2.get_security_group(id=self.group1.id)
            except EC2ResponseError as ER:
                if ER.status == 400:
                    self.group1 = None
                else:
                    raise ER
        if self.group2:
            try:
                self.group2 = self.user.ec2.get_security_group(id=self.group2.id)
            except EC2ResponseError as ER:
                if ER.status == 400:
                    self.group2 = None
                else:
                    raise ER
        if not self.group1:
            self.log.debug("Creating group1..")
            self.group1 = self.user.ec2.add_group(str(self.name) + "_group1_" + str(time.time()))
            self.log.debug("Authorize ssh for group1 from '0.0.0.0/0'")
            self.user.ec2.authorize_group(self.group1, port=22, protocol='tcp',
                                        cidr_ip='0.0.0.0/0')
            self.user.ec2.authorize_group(self.group1, protocol='icmp',port='-1',
                                        cidr_ip='0.0.0.0/0')

        if  not self.group2:
            self.log.debug("Creating group2, will authorize later from rules within test methods..")
            self.group2 = self.user.ec2.add_group(str(self.name) + "_group2_" + str(time.time()))
            self.user.ec2.authorize_group(self.group2, protocol='icmp', port='-1',
                                        cidr_ip='0.0.0.0/0')

    @property
    def group1(self):
        g1 = getattr(self, '_group1', None)
        if not g1:
            ### Add and authorize securtiy groups
            self.log.debug("Creating group1...")
            g1 = self.user.ec2.add_group(str(self.name) + "_group1_" + str(time.time()))
            self.log.debug("Authorize ssh for group1 from '0.0.0.0/0'")
            self.user.ec2.authorize_group(g1, port=22, protocol='tcp',
                                          cidr_ip='0.0.0.0/0')
            self.user.ec2.authorize_group(g1, port=-1, protocol='icmp',
                                          cidr_ip='0.0.0.0/0')
            setattr(self, '_group1', g1)
        return g1

    @group1.setter
    def group1(self, value):
        setattr(self, '_group1', value)
    
    @property
    def group2(self):
        g2 = getattr(self, '_group2', None)
        if not g2:
            self.log.debug("Creating group2, will authorize later from rules "
                           "within test methods...")
            g2 = self.user.ec2.add_group(str(self.name) + "_group2_" + str(time.time()))
            self.user.ec2.authorize_group(g2, port=-1, protocol='icmp',
                                          cidr_ip='0.0.0.0/0')
            setattr(self, '_group2', g2)

        return g2

    @group2.setter
    def group2(self, value):
        setattr(self, '_group2', value)
        
    @property
    def group1_instances(self):
        gi = getattr(self, '_group1_instances', None)
        if gi is None:
            gi = []
            self._group1_instances = gi
        return gi

    @group1_instances.setter
    def group1_instances(self, value):
        setattr(self, '_group1_instances', value)

    
    @property
    def group2_instances(self):
        gi = getattr(self, '_group2_instances', None)
        if gi is None:
            gi = []
            self._group2_instances = gi
        return gi

    @group2_instances.setter
    def group2_instances(self, value):
        setattr(self, '_group2_instances', value)
        
    @property
    def image(self):
        image = getattr(self, '_image', None)
        if not image:
            ### Get an image to work with
            if self.args.emi:
                image = self.user.ec2.get_emi(emi=str(self.args.emi))
            else:
                image = self.user.ec2.get_emi(root_device_type="instance-store", basic_image=True)
            if not image:
                raise RuntimeError('couldnt find instance store image')
            setattr(self, '_image', image)
        return image

    @property
    def vpc_backend(self):
        if not self.is_vpc_mode():
            return None
        if not hasattr(self, '_vpc_backend'):
            self._vpc_backend = None
        if not self._vpc_backend:
            vpc_backend_host = self.sysadmin.clc_machine.hostname
            try:
                self._vpc_backend = Midget(vpc_backend_host, systemconnection=self.sysadmin)
            except ImportError as IE:
                self._vpc_backend = None
                self.errormsg('Not Creating VPC backend DEBUG interface, err:"{0}"'.format(str(IE)))
            except Exception as VBE:
                self._vpc_backend = None
                self.errormsg('FYI... Failed to create vpc backend interface, err:\n{0}'
                            '\nUnable to get VPC backend debug. Ignoring Error:"{1}"'
                            .format(get_traceback(), str(VBE)))
                return None
        return self._vpc_backend

    def errormsg(self, msg):
        return self.log.error(red(msg))
        
    def authorize_group_for_instance_list(self, group, instances):
        for instance in instances:
            assert isinstance(instance, EuInstance)
            try:
                self.user.ec2.authorize_group(group, protocol='tcp', port=22,
                                            cidr_ip=instance.private_ip_address + "/32")
                self.user.ec2.authorize_group(group, protocol='icmp', port='-1',
                                            cidr_ip=instance.private_ip_address + "/32")
            except:
                self.user.ec2.show_instance(instance)
                self.user.ec2.show_security_group(group)
                self.errormsg('Failed to authorize group:{0} to allow private ip for '
                              'instance:"{1}/{2}"'.format(group,
                                                          instance.id,
                                                          instance.private_ip_address))
                raise

    def revoke_group_for_instance_list(self, group, instances):
        for instance in instances:
            assert isinstance(instance, EuInstance)
            self.user.ec2.revoke_security_group(group, from_port='22', protocol='tcp',
                                                cidr_ip=instance.private_ip_address + "/32")
            self.user.ec2.revoke_security_group(group, from_port='-1', protocol='icmp',
                                                cidr_ip=instance.private_ip_address + "/32")


    def clean_method(self):
        if self.args.no_clean:
            self.status('No clean flag set, not cleaning test resources')
        else:
            errors = []
            ins = self.group1_instances
            ins.extend(self.group2_instances)
            try:
                self.user.ec2.terminate_instances(ins)
            except EC2ResponseError as ER:
                if ER.status == 400:
                    pass
                else:
                    raise
            except Exception as E:
                errors.append(E)
                self.log.error("{0}\n{1}".format(get_traceback(), E))

            try:
                self.user.ec2.delete_group(self.group1)
            except EC2ResponseError as ER:
                if ER.status == 400:
                    pass
                else:
                    raise
            except Exception as E:
                errors.append(E)
                self.log.error("{0}\n{1}".format(get_traceback(), E))

            try:
                self.user.ec2.delete_group(self.group2)
            except EC2ResponseError as ER:
                if ER.status == 400:
                    pass
                else:
                    raise
            except Exception as E:
                errors.append(E)
                self.log.error("{0}\n{1}".format(get_traceback(), E))
            if errors:
                raise RuntimeError("Error in cleanup:{0}"
                                   .format(", ".join(str(e) for e in errors)))



    def is_vpc_mode(self):
        return 'VPC' in self.user.ec2.get_supported_platforms()

    def get_proxy_machine(self, instance, use_mido_gw=False):
        if self.is_vpc_mode():
            if use_mido_gw:
                gw_hosts = self.user.ec2.get_backend_vpc_gateways()
                if not gw_hosts:
                    raise ValueError('No backend VPC gateways were found?')

                # pick single gw host and ip for lookup purposes
                gw_host_ip = self.user.ec2.clc.ssh.get_ipv4_lookup(gw_hosts[0])
                if not gw_host_ip:
                    raise RuntimeError('Failed to lookup ipv4 address for host:"{0}"'
                                       .format(gw_hosts[0]))
                gw_host_ip = gw_host_ip[0]
                gw_machine = self.sysadmin.get_host_by_hostname(gw_host_ip)
            else:
                gw_machine = self.sysadmin.clc_machine
            return gw_machine

        prop = self.sysadmin.get_property('{0}.cluster.networkmode'.format(instance.placement))
        if prop.value.lower() == "edge":
            proxy_machine = self.get_active_nc_for_instance(instance)
        else:
            proxy_machine = self.get_active_cc_for_instance(instance)
        self.log.debug("Instance is running on: " + proxy_machine.hostname)
        return proxy_machine

    def get_vpc_proxy_ssh_connection(self, instance):
        """
        Provides a means to communicate to instances within a VPC on their private interfaces
        from the VPC namespace (for now this is the CLC). This will act as a sudo proxy interface
        to the instances on their private network(s).
        :param instance: an instance object to connect to
        :param ssh_to_instance: boolean. If true will attempt to ssh from clc to instance for each
                                command.
        """
        gw_machine = self.get_proxy_machine(instance=instance)
        self.log.debug('Using "{0}" as the internal proxy machine for instance:{1}'
                   .format(gw_machine.hostname, instance))
        if gw_machine:
            vpc_proxy_ssh = gw_machine.ssh
        else:
            raise ValueError('Could not find tester machine for ip: "{0}"'
                             .format(gw_machine.hostname))

        if instance.keypath:
            keyname= '{0}_{1}'.format(instance.id, os.path.basename(instance.keypath))
            try:
                vpc_proxy_ssh.sys('ls {0}'.format(keyname), code=0)
            except CommandExitCodeException:
                vpc_proxy_ssh.sftp_put(instance.keypath, keyname)
        if not hasattr(vpc_proxy_ssh, 'orig_cmd_method'):
            vpc_proxy_ssh.orig_cmd_method = vpc_proxy_ssh.cmd
            def newcmd(cmd, **kwargs):
                ssh_cmd = ('ip netns {0} ssh -o StrictHostKeyChecking=no -n -i {1} {2}@{3} "{4}"'
                           .format(instance.vpc_id, keyname, instance.username,
                                   instance.private_ip_address,
                                   cmd))
                return vpc_proxy_ssh.orig_cmd_method(cmd, **kwargs)
            vpc_proxy_ssh.cmd = newcmd
        return vpc_proxy_ssh

    def create_proxy_ssh_connection_to_instance(self, instance, retry=10):
        if self.is_vpc_mode():
            return self.get_vpc_proxy_ssh_connection(instance=instance)
        proxy_machine = self.get_proxy_machine(instance)
        ssh = None
        attempts = 0
        elapsed = 0
        next_retry_time = 10
        start = time.time()
        proxy_keypath=proxy_machine.ssh.keypath or None
        while not ssh and attempts < retry:
            attempts += 1
            elapsed = int(time.time()-start)
            self.log.debug('Attempting to ssh to instances private ip:' + str(instance.private_ip_address) +
                       'through the cc ip:' + str(proxy_machine.hostname) + ', attempts:' +str(attempts) + "/" + str(retry) +
                       ", elapsed:" + str(elapsed))
            try:
                ssh = SshConnection(host=instance.private_ip_address,
                                keypath=instance.keypath,
                                proxy=proxy_machine.hostname,
                                proxy_username=proxy_machine.ssh.username,
                                proxy_password=proxy_machine.ssh.password,
                                proxy_keypath=proxy_keypath)
            except Exception, ce:
                tb = get_traceback()
                if attempts >= retry:
                    self.log.debug("\n{0}".format(tb))
                self.log.debug('Failed to connect error:' + str(ce))
            if attempts < retry:
                    time.sleep(next_retry_time)

        if not ssh:
            raise Exception('Could not ssh to instances private ip:' + str(instance.private_ip_address) +
                            ' through the cc ip:' + str(proxy_machine.hostname) + ', attempts:' +str(attempts) + "/" + str(retry) +
                            ", elapsed:" + str(elapsed))
        return ssh

    def get_active_cc_for_instance(self,instance,refresh_active_cc=30):
        elapsed = time.time()-self.cc_last_checked
        self.cc_last_checked = time.time()
        if elapsed > refresh_active_cc:
            use_cached_list = False
        else:
            use_cached_list = True
        cc = self.sysadmin.get_hosts_for_cluster_controllers(partition=instance.placement)[0]
        return cc

    def get_active_nc_for_instance(self,instance):
        nc = self.sysadmin.get_hosts_for_node_controllers(instanceid=instance.id)[0]
        return nc

    def ping_instance_private_ip_from_euca_internal(self, instance, ping_timeout=120):
        assert isinstance(instance, EuInstance)
        proxy_machine = self.get_proxy_machine(instance)
        net_namespace = None
        if self.is_vpc_mode():
            net_namespace = instance.vpc_id
        vpc_backend_retries = 0
        max_retries = 1
        while vpc_backend_retries <= max_retries:
            if not self.vpc_backend:
                vpc_backend_retries = max_retries + 1
            try:
                wait_for_result(self._ping_instance_private_ip_from_euca_internal,
                                            result=True,
                                            timeout=ping_timeout,
                                            instance=instance,
                                            proxy_machine=proxy_machine,
                                            net_namespace=net_namespace)
            except WaitForResultException:
                self.errormsg('Failed to ping instance: {0},  private ip:{1} from internal host: {2}'
                              .format(instance.id,
                                      instance.private_ip_address,
                                      proxy_machine.hostname))
                self.errormsg('Ping failure. Fetching network debug info from internal host...')
                proxy_machine.dump_netfail_info(ip=instance.private_ip_address,
                                                        net_namespace=net_namespace)
                self.errormsg('Done dumping network debug info from the "internal euca proxy host" @ '
                              '{0} '
                              'used in attempting to ping instance {1}, private ip: {2}'
                              .format(proxy_machine.hostname,
                                      instance.id,
                                      instance.private_ip_address))
                if self.vpc_backend:
                    self.dump_vpc_backend_info_for_instance(instance)
                    raise
                else:
                    raise
            vpc_backend_retries += 1
        self.log.debug('Successfully pinged instance: {0},  private ip:{1} from internal host: {2}'
                   .format(instance.id,
                           instance.private_ip_address,
                           proxy_machine.hostname))

    def dump_vpc_backend_info_for_instance(self, instance):
        if self.vpc_backend:
            try:
                self.vpc_backend.show_instance_network_summary(instance)
            except Exception, ME:
                self.log.debug('{0}\nCould not dump vpc backend debug, err:{1}'
                           .format(ME, get_traceback()))

    def _ping_instance_private_ip_from_euca_internal(self,
                                                     instance,
                                                     proxy_machine,
                                                     net_namespace=None):
        assert isinstance(instance, EuInstance)
        try:
            proxy_machine.ping_check(instance.private_ip_address,
                                             net_namespace=net_namespace)
            return True
        except Exception, PE:
            self.log.debug('Ping Exception:{0}'.format(PE))
            self.log.debug('Failed to ping instance: {0},  private ip:{1} from internal host: {2}'
                          .format(instance.id,
                                  instance.private_ip_address,
                                  proxy_machine.hostname))
        return False


    def is_port_in_use_on_instance(self, instance, port, tcp=True, ipv4=True):
        args = '-ln'
        if tcp:
            args += 't'
        else:
            args += 'u'
        if ipv4:
            args += 'A inet'
        else:
            args += 'A inet6'
        use = instance.sys("netstat " + str(args) + " | awk '$6 ==" +
                           ' "LISTEN" && $4 ~ ".' + str(port) +
                           '"' + "' | grep LISTEN")
        if use:
            self.log.debug('Port {0} IS in use on instance:'
                       .format(port, instance.id))
            return True
        else:
            self.log.debug('Port {0} IS NOT in use on instance:'
                       .format(port, instance.id))
            False

    def is_port_range_in_use_on_instance(self, instance, start, end,
                                         tcp=True, ipv4=True):
        for x in xrange(start, end):
            if self.is_port_in_use_on_instance(instance=instance,
                                               port=x,
                                               tcp=tcp,
                                               ipv4=ipv4):
                return True
        return False

    def show_instance_security_groups(self, instance):
        assert isinstance(instance, Instance)
        self.status('Showing security groups for instance: {0}'.format(instance.id))
        for group in instance.groups:
            self.user.ec2.show_security_group(group)




    ################################################################
    #   Test Methods
    ################################################################


    def test1_create_instance_in_zones_for_security_group1(self, ping_timeout=180, zones=None):
        '''
        Definition:
        Create test instances within each zone within security group1. This security group is authorized for
        ssh access from 0.0.0.0/0.
        This test attempts the following:
            -To run an instance in each zone and confirm it reaches 'running' state.
            -Confirm the instance is ping-able from the cc within a given timeout
            -Establish and verify an ssh session directly from the local machine running this test.
            -Place ssh key on instance for later use
            -Add instance to global 'group1_instances'
        '''
        if zones and not isinstance(zones, list):
            zones = [zones]
        zones = zones or self.zones
        for zone in zones:
            #Create an instance, monitor it's state but disable the auto network/connect checks till afterward
            instance = self.user.ec2.run_image(image=self.image,
                                             keypair=self.keypair,
                                             group=self.group1,
                                             zone=zone,
                                             auto_connect=False,
                                             subnet_id=self.subnet_id,
                                             systemconnection=self.sysadmin,
                                             monitor_to_running=False)[0]
            self.group1_instances.append(instance)
        self.user.ec2.monitor_euinstances_to_running(self.group1_instances)
        #Now run the network portion.
        for instance in self.group1_instances:
            self.status('Checking connectivity to:'
                        + str(instance.id) + ":" + str(instance.private_ip_address)
                        + ", zone:" + str(instance.placement) )
            assert isinstance(instance, EuInstance)
            self.log.debug('Attempting to ping instances private ip from cc...')
            self.ping_instance_private_ip_from_euca_internal(instance=instance, ping_timeout=ping_timeout)
            self.log.debug('Attempting to ssh to instance from local test machine...')
            self.log.debug('Check some debug information re this data connection in this security group first...')
            self.show_instance_security_groups(instance)
            self.user.ec2.does_instance_sec_group_allow(instance=instance,
                                                      src_addr=None,
                                                      protocol='tcp',
                                                      port=22)
            try:
                start = time.time()
                instance.connect_to_instance(timeout=120)
            except Exception, ConnectErr:
                if self.vpc_backend:
                    self.errormsg('{0}\n{1}\nFailed to connect to instance:"{2}", dumping info '
                                  .format(ConnectErr, get_traceback(), instance.id))
                    self.dump_vpc_backend_info_for_instance(instance)
                    raise ConnectErr

            if instance.ssh:
                self.status('SSH connection to instance:' + str(instance.id) +
                            ' successful to public ip:' + str(instance.ip_address) +
                            ', zone:' + str(instance.placement))
            else:
                raise RuntimeError('intance:{0} ssh is none, failed to connect after {1} seconds?'
                                   .format(instance.id, int(time.time()-start)))
            instance.sys('uname -a', code=0)
            instance.ssh.sftp_put(instance.keypath, os.path.basename(instance.keypath))
            instance.sys('chmod 0600 ' + os.path.basename(instance.keypath), code=0 )


    def test2_create_instance_in_zones_for_security_group2(self, ping_timeout=180,
                                                           auto_connect=False, zones=None):
        '''
        Definition:
        This test attempts to create an instance in each zone within security group2 which should not
        be authorized for any remote access (outside of the CC).
        The test attempts the following:
            -To run an instance in each zone and confirm it reaches 'running' state.
            -Confirm the instance is ping-able from the cc within a given timeout
            -Establish and verify an ssh session using the cc as a proxy.
            -Place ssh key on instance for later use
            -Add instance to global 'group2_instances'
        :params ping_timeout: Int Time to wait for ping for successful ping to instance(s)
        :params auto_connect: Boolean. If True will auto ssh to instance(s), if False will
                              use cc/nc as ssh proxy
        :params zones: List of names of Availability zone(s) to create instances in
        '''
        if zones and not isinstance(zones, list):
            zones = [zones]
        zones = zones or self.zones
        for zone in self.zones:
            instance = self.user.ec2.run_image(image=self.image,
                                             keypair=self.keypair,
                                             group=self.group2,
                                             zone=zone,
                                             subnet_id = self.subnet_id,
                                             auto_connect=auto_connect,
                                             systemconnection=self.sysadmin,
                                             monitor_to_running=False)[0]
            self.group2_instances.append(instance)
        self.user.ec2.monitor_euinstances_to_running(self.group2_instances)
        for instance in self.group2_instances:
            self.status('Checking connectivity to:' + str(instance.id) + ":" + str(instance.private_ip_address)+
                        ", zone:" + str(instance.placement) )
            assert isinstance(instance, EuInstance)
            self.show_instance_security_groups(instance)
            self.ping_instance_private_ip_from_euca_internal(instance=instance,
                                                             ping_timeout=ping_timeout)
            if not auto_connect:
                self.status('Make sure ssh is working through an internal euca path before '
                            'trying between instances...')
                instance.proxy_ssh = self.create_proxy_ssh_connection_to_instance(instance)
                self.status('SSH connection to instance:' + str(instance.id) +
                            ' successful to private ip:' + str(instance.private_ip_address) +
                            ', zone:' + str(instance.placement))
            else:
                instance.proxy_ssh = instance.ssh
            instance.proxy_ssh.sys('uname -a', code=0)
            self.status('Uploading keypair to instance in group2...')
            instance.proxy_ssh.sftp_put(instance.keypath, os.path.basename(instance.keypath))
            instance.proxy_ssh.sys('chmod 0600 ' + os.path.basename(instance.keypath), code=0 )
            self.status('Done with create instance security group2:' + str(instance.id))


    def test3_test_ssh_between_instances_in_diff_sec_groups_same_zone(self):
        '''
        Definition:
        This test attempts to set up security group rules between group1 and group2 to authorize group2 access
        from group1. If no_cidr is True security groups will be setup using cidr notation ip/mask for each instance in
        group1, otherwise the entire source group 1 will be authorized.

        Test attempts to:
            -Authorize security groups for inter group private ip access.
            -Iterate through each zone and attempt to ssh from an instance in group1 to an instance in group2 over their
                private ips.
            - Run same 2 tests from above by authorizing a SecurityGroup
        '''
        def check_instance_connectivity():
            max_retries = 1
            vpc_backend_retries = 0
            while vpc_backend_retries <= max_retries:
                if not self.vpc_backend:
                    vpc_backend_retries = max_retries + 1
                try:
                    for zone in self.zones:
                        instance1 = None
                        instance2 = None
                        for instance in self.group1_instances:
                            if instance.placement == zone:
                                assert isinstance(instance, EuInstance)
                                instance1 = instance
                                break
                        if not instance1:
                            raise Exception('Could not find instance in group1 for zone:' +
                                            str(zone))

                        for instance in self.group2_instances:
                            if instance.placement == zone:
                                assert isinstance(instance, EuInstance)
                                instance2 = instance
                                break
                        if not instance2:
                            raise Exception('Could not find instance in group2 for zone:'
                                            + str(zone))
                    self.status(
                        'Attempting to run ssh command "uname -a" between instances across '
                        'security groups:\n'
                        + str(instance1.id) + '/sec grps(' + str(instance1.security_groups) +
                        ") --> "
                        + str(instance2.id) + '/sec grps(' + str(instance2.security_groups) + ")\n"
                        + "Current test run in zone: " + str(zone))
                    self.log.debug('Check some debug information re this data connection in this '
                               'security group first...')
                    self.show_instance_security_groups(instance2)
                    self.user.ec2.does_instance_sec_group_allow(instance=instance2,
                                                              src_addr=instance1.private_ip_address,
                                                              protocol='tcp',
                                                              port=22)

                    self.log.debug('Reset ssh connection to instance:{0} first...'
                               .format(instance1.id))
                    instance1.connect_to_instance()
                    self.status('Now Running the ssh command which checks connectivity from '
                               'instance1 to instance2...')
                    instance1.sys("ssh -o StrictHostKeyChecking=no -i "
                                  + str(os.path.basename(instance1.keypath))
                                  + " root@" + str(instance2.private_ip_address)
                                  + " 'uname -a'", code=0)
                    self.status('"{0}" to "{1}" connectivity test succeeded'.format(instance1.id,
                                                                                    instance2.id))
                except Exception, ConnectivityErr:
                    if vpc_backend_retries:
                        if self.vpc_backend:
                            self.errormsg('Retry still failed connectivity test after restarting '
                                          'vpc backend')
                        raise ConnectivityErr

                    elif self.vpc_backend:
                        self.dump_vpc_backend_info_for_instance(instance1)
                        self.dump_vpc_backend_info_for_instance(instance2)
                        self.errormsg('Could not connect to instance:"{0}"'
                                      .format(instance.id))
                        raise ConnectivityErr
                    else:
                        raise ConnectivityErr
                else:
                    if self.vpc_backend and vpc_backend_retries:
                        self.log.debug('MidoRetries:{0}'.format(vpc_backend_retries))
                        raise MidoError('Connectivity test passed, but only after '
                                        'restarting Midolman.')
                    else:
                        self.status('Ssh between instances passed')
                        break

        self.status('Authorizing access from group1 individual instance IPs to group2, '
                    'then checking connectivity...')
        self.authorize_group_for_instance_list(self.group2, self.group1_instances)
        self.status('group2 should now allow access from each individual instance IP from '
                    'group1...')
        self.user.ec2.show_security_group(self.group2)
        check_instance_connectivity()
        self.status('Revoking auth for group1 instances from group2, then re-add using '
                    'the using the group id instead of invididual instance IPs...')
        self.revoke_group_for_instance_list(self.group2, self.group1_instances)
        self.status('group2 should no longer have authorization from the individual instance IPs'
                    'from group1...')
        self.user.ec2.show_security_group(self.group2)
        self.status('Auth group1 access to group2...')
        self.user.ec2.authorize_group(self.group2, cidr_ip=None, port=22,
                                      protocol='tcp', src_security_group=self.group1)
        self.user.ec2.authorize_group(self.group2, cidr_ip=None, port=-1,
                                      protocol='icmp', src_security_group=self.group1)
        self.status('Group2 should now allow access from source group1 on tcp/22 and icmp...')
        self.user.ec2.show_security_group(self.group2)
        check_instance_connectivity()

    def test4_attempt_unauthorized_ssh_from_test_machine_to_group2(self):
        '''
        Description:
        Test attempts to verify that the local machine cannot ssh to the instances within group2 which is not authorized
        for ssh access from this source.
        '''
        for instance in self.group2_instances:
            assert isinstance(instance, EuInstance)
            #Provide some debug information re this data connection in this security group
            self.status('Attempting to ssh from local test machine to instance: {0}, '
                        'this should not be allowed...'.format(instance.id))
            self.show_instance_security_groups(instance)
            self.user.ec2.does_instance_sec_group_allow(instance=instance, src_addr=None, protocol='tcp',port=22)
            try:
                instance.reset_ssh_connection(timeout=5)
                if self.vpc_backend:
                    try:
                        self.vpc_backend.show_instance_network_summary(instance)
                    except Exception, ME:
                        self.log.debug('{0}\nCould not dump Mido debug, err:{1}'
                                   .format(ME, get_traceback()))
                raise Exception('Was able to connect to instance: ' + str(instance.id) + ' in security group:'
                                + str(self.group2.name))
            except:
                self.log.debug('Success: Was not able to ssh from the local machine to instance in unauthorized sec group')

    def test5_test_ssh_between_instances_in_same_sec_groups_different_zone(self):
        '''
        Definition:
        This test attempts to check connectivity for instances in the same security group, but in different zones.
        Note: This test requires the CC have tunnelling enabled, or the CCs in each zone be on same
        layer 2 network segment.

        Test attempts to:
            -Iterate through each zone and attempt to ssh from an instance in group1 to an instance in a separate zone
             but same security group1 over their private ips.
        '''
        zones = []
        if len(self.zones) < 2:
            raise SkipTestException('Skipping test5, only a single zone found or provided')

        for zone in self.zones:
            zones.append(TestZone(zone))
            #Grab a single instance from each zone within security group1
        for zone in zones:
            instance = None
            for instance in self.group1_instances:
                if instance.placement == zone.zone:
                    assert isinstance(instance, EuInstance)
                    zone.test_instance_group1 = instance
                    break
                instance = None
            if not zone.test_instance_group1:
                raise Exception('Could not find an instance in group1 for zone:' + str(zone.zone))

        self.log.debug('Iterating through zones, attempting ssh between zones within '
                       'same security group...')
        for zone in zones:
            instance1 = zone.test_instance_group1
            for zone2 in zones:
                if zone.zone != zone2.zone:
                    instance2 = zone2.test_instance_group1
                    if not instance1 or not instance2:
                        raise Exception('Security group: {0}, missing instances in a '
                                        'Zone:{1} = instance:{2}, Zone:{3} = instance:{4}'
                                        .format(self.group1.name, zone.zone, instance1,
                                                zone2.zone, instance2))
                    self.log.debug('Attempting to run ssh command "uname -a" between '
                                   'instances across zones and security groups:\n'
                                   '{0}/sec grps({1}) --> {2}/sec grps({3})\n'
                                   'Current test run in zones: {4} ---> {5}'
                                   .format(instance1.id, instance1.security_groups,
                                           instance2.id, instance2.security_groups,
                                           instance1.placement, instance2.placement))
                    self.log.debug('Check some debug information re this data connection in '
                                   'this security group first...')
                    self.user.ec2.does_instance_sec_group_allow(
                        instance=instance2, src_addr=instance1.private_ip_address, protocol='tcp',
                        port=22)
                    self.log.debug('Now Running the ssh command...')
                    try:
                        instance1.sys("ssh -o StrictHostKeyChecking=no -i "
                                      + str(os.path.basename(instance1.keypath))
                                      + " root@" + str(instance2.private_ip_address)
                                      + " ' uname -a'", code=0)
                        self.log.debug('Ssh between instances passed')
                    except Exception, ME:
                        if self.vpc_backend:
                            try:
                                self.vpc_backend.show_instance_network_summary(instance)
                            except Exception, ME:
                                self.log.warning('{0}\nCould not dump Mido debug, err:{1}'
                                                 .format(ME, get_traceback()))
                        raise

    def test6_test_ssh_between_instances_in_diff_sec_groups_different_zone(self):
        '''
        Definition:
        This test attempts to set up security group rules between group1 and group2 to authorize group2 access
        from group1 across different zones.
        If no_cidr is True security groups will be setup using cidr notication ip/mask for each instance in
        group1, otherwise the entire source group 1 will authorized.
        the group will be
        Note: This test requires the CC have tunnelling enabled, or the CCs in each zone be on same
        layer 2 network segment.

        Test attempts to:
            -Authorize security groups for inter group private ip access.
            -Iterate through each zone and attempt to ssh from an instance in group1 to an instance in group2 over their
                private ips.
        '''
        zones = []
        if len(self.zones) < 2:
            raise SkipTestException('Skipping test5, only a single zone found or provided')
        self.status('Authorizing group2:' + str(self.group2.name) + ' for access from group1:' + str(self.group1.name))
        self.user.ec2.authorize_group(self.group2, cidr_ip=None, port=None,
                                      src_security_group=self.group1)


        for zone in self.zones:
            zones.append(TestZone(zone))


        self.log.debug('Grabbing  a single instance from each zone and from each test security group to use in this test...')
        for zone in zones:
            instance = None
            for instance in self.group1_instances:
                if instance.placement == zone.zone:
                    assert isinstance(instance, EuInstance)
                    zone.test_instance_group1 = instance
                    break
                instance = None
            if not zone.test_instance_group1:
                raise Exception('Could not find an instance in group1 for zone:' + str(zone.zone))
            instance = None
            for instance in self.group2_instances:
                if instance.placement == zone.zone:
                    assert isinstance(instance, EuInstance)
                    zone.test_instance_group2 = instance
                    break
            if not zone.test_instance_group2:
                raise Exception('Could not find instance in group2 for zone:' + str(zone.zone))
            instance = None

        self.status('Checking connectivity for instances in each zone, in separate but authorized security groups...')
        for zone in zones:
            instance1 = zone.test_instance_group1
            if not instance1:
                raise Exception('Missing instance in Security group: ' + str(self.group1.name) + ', Zone:' +
                                str(zone) + " = instance:" + str(instance1) )
            for zone2 in zones:
                if zone.zone != zone2.zone:
                    instance2 = zone2.test_instance_group2
                    if not instance2:
                        raise Exception('Missing instance in Security group: ' + str(self.group2.name) + ', Zone:' +
                                        str(zone2.zone) + " = instance:" + str(instance2) )
                    self.log.debug('Attempting to run ssh command "uname -a" between instances across zones and security groups:\n'
                               + str(instance1.id) + '/sec grps(' + str(instance1.security_groups)+") --> "
                               + str(instance2.id) + '/sec grps(' + str(instance2.security_groups)+")\n"
                               + "Current test run in zones: " + str(instance1.placement) + "-->" + str(instance2.placement),
                               linebyline=False )
                    self.log.debug('Check some debug information re this data connection in this security group first...')
                    self.user.ec2.does_instance_sec_group_allow(instance=instance2,
                                                              src_addr=instance1.private_ip_address,
                                                              protocol='tcp',
                                                              port=22)
                    self.log.debug('Now Running the ssh command...')
                    instance1.sys("ssh -o StrictHostKeyChecking=no -i "
                                  + str(os.path.basename(instance1.keypath))
                                  + " root@" + str(instance2.private_ip_address)
                                  + " ' uname -a'", code=0)
                    self.log.debug('Ssh between instances passed')

    def test7_add_and_revoke_tcp_port_range(self,
                                            start=None,
                                            src_cidr_ip='0.0.0.0/0',
                                            count=10,
                                            instances=None,
                                            retry_interval=15):
        '''
        Definition:
        Attempts to add a range of ports to a security group and test
        the ports from the local machine to make sure they are available.
        Next the test revokes the ports and verifies they are no longer
        available.
        :param start: starting port of range to scan
        :param src_cidr_ip: cidr ip for src authorization. If None the test
                            will attempt to discovery the cidr ip of the
                            machine running this test to use for src auth ip.
        :param count: number of consecutive ports from 'start' to test
        :param tcp: boolean tcp if true, udp if false
        '''

        if instances:
            if not isinstance(instances, list):
                instances = [instances]
            for instance in instances:
                assert isinstance(instance, EuInstance)
        else:
            instances = self.group1_instances
        if not instances:
            raise ValueError('Could not find instance in group1')


        # Iterate through all instances and test...
        for instance1 in instances:
            # Make sure we can ssh to this instance (note this may need to be
            # adjusted for windows access
            # 'does_instance_sec_group_allow' will set user.ec2.local_machine_source_ip to the
            # ip the local machine uses to communicate with the instance.
            instance1.netcat_name = 'netcat'
            if src_cidr_ip is None:
                if not self.user.ec2.does_instance_sec_group_allow(instance=instance1,
                                                                   protocol='tcp',
                                                                   port=22):
                    src_cidr_ip = str(self.user.ec2.local_machine_source_ip) + '/32'
                    self.user.ec2.authorize_group(self.group1,
                                                  protocol='tcp',
                                                  cidr_ip=src_cidr_ip,
                                                  port=22)
            else:
                self.user.ec2.authorize_group(self.group1,
                                              protocol='tcp',
                                              cidr_ip=src_cidr_ip,
                                              port=22)
            try:
                instance1.sys('which {0}'.format(instance1.netcat_name), code=0)
            except CommandExitCodeException:
                got_it = False
                for pkg in ['nc', 'netcat']:
                    try:
                        instance1.sys('apt-get install {0} -y'.format(pkg), code=0)
                        got_it = True
                        break
                    except CommandExitCodeException:
                        try:
                            instance1.sys('yum install {0} -y'.format(pkg), code=0)
                            got_it = True
                            break
                        except CommandExitCodeException:
                            self.log.debug('could install "{0}" on this instance'.format(pkg))
                if not got_it:
                        raise RuntimeError('Could not install netcat on: {0}'.format(instance1))
                instance1.netcat_name = pkg

            #make sure we have an open port range to play with...
            if start is None:
                for x in xrange(2000,65000):
                    if self.is_port_range_in_use_on_instance(instance=instance1,
                                                             start=x,
                                                             end=x+count,
                                                             tcp=True):
                        x=x+count
                    else:
                        start=x
                        break
                if not start:
                    raise RuntimeError('Free consecutive port range of count:{0} '
                                       'not found on instance:{1}'
                                       .format(count, instance1.id))
            # authorize entire port range...
            self.user.ec2.authorize_group(self.group1,
                                          protocol='tcp',
                                          cidr_ip=src_cidr_ip,
                                          port=start,
                                          end_port=start+count)
            auth_starttime = time.time()
            # test entire port range is accessible from this machine
            test_file = 'nephoria_port_test.txt'
            #Allow some delay for the rule to be applied in the network...
            time.sleep(10)
            for x in xrange(start, start+count):
                # Set up socket listener with netcat, to make sure we're not
                # connecting to the CC or other device write port to file and
                # verify file contents as well.
                test_string = '{0} last port tested[{1}]'.format(time.time(), x)
                self.log.debug("Gathering debug information as to whether the "
                           "tester's src ip is authorized for this port test...")
                if not self.user.ec2.does_instance_sec_group_allow(
                        instance=instance1,
                        src_addr=src_cidr_ip.split('/')[0],
                        protocol='tcp',
                        port=x):
                    raise ValueError('Group:{0} did not have {1}:{2} authorized'
                                     .format(self.group1.name,
                                             src_cidr_ip.split('/')[0],
                                             x))
                # start up netcat, sleep to allow nohup to work before quiting
                # the shell...
                instance1.sys('killall -9 {0} 2> /dev/null'.format(instance1.netcat_name),
                              timeout=5)
                instance1.sys('{' + ' ( nohup {0} -k -l {1} > {2} ) &  sleep 1; '
                              .format(instance1.netcat_name, x, test_file) + '}',
                              code=0, timeout=5)
                # attempt to connect socket at instance/port and send the
                # test_string...
                time.sleep(2) #Allow listener to setup...
                done = False
                attempt =0
                while not done:
                    try:
                        attempt += 1
                        test_port_status(ip=instance1.ip_address,
                                                port=x,
                                                tcp=True,
                                                send_buf=test_string,
                                                verbose=True)
                        done = True
                    except socket.error as SE:
                        self.log.debug('Failed to poll port status on attempt {0}, elapsed since auth '
                                   'request:"{1}"'
                                   .format(attempt, int(time.time()-auth_starttime)))
                        try:
                            self.log.debug('Failed to connect to "{0}":IP:"{1}":'
                                       'PORT:"{2}"'.format(instance1.id,
                                                           instance1.ip_address,
                                                           x))
                            self.user.show_security_group(self.group1)
                            try:
                                self.log.debug('Getting netcat info from instance...')
                                instance1.sys('ps aux | grep {0}'.format(instance1.netcat_name),
                                              timeout=10)
                            except CommandExitCodeException:
                                pass
                            self.log.debug('Iptables info from Euca network component '
                                       'responsible for this instance/security '
                                       'group...')
                            proxy_machine = self.get_proxy_machine(instance1)
                            proxy_machine.sys('iptables-save', timeout=10)

                        except:
                            self.log.debug('Error when fetching debug output for '
                                       'failure, ignoring:' +
                                       str(get_traceback()))
                        if attempt >= 2:
                            raise SE
                        self.log.debug('Sleeping {0} seconds before next attempt:({1}/{2})'
                                   .format(retry_interval, attempt, '2'))
                        time.sleep(retry_interval)
                # Since no socket errors were encountered assume we connected,
                # check file on instance to make sure we didn't connect somewhere
                # else like the CC...
                instance1.sys('grep "{0}" {1}; echo "" > {1}'
                              .format(test_string, test_file),
                              code=0)
                self.status('Port "{0}" successfully tested on instance:{1}/{2}'
                           .format(x, instance1.id, instance1.ip_address))
            self.status('Authorizing port range {0}-{1} passed'
                        .format(start, start+count))

            self.status('Now testing revoking by removing the same port'
                        'range...')
            time.sleep(3)
            self.user.ec2.revoke_security_group(group=self.group1, from_port=start,
                                                to_port=start + count, protocol='tcp',
                                                cidr_ip=src_cidr_ip)
            #Allow some delay for the rule to be applied in the network...
            time.sleep(10)
            for x in xrange(start, start+count):
                # Set up socket listener with netcat, to make sure we're not
                # connecting to the CC or other device write port to file and
                # verify file contents as well.
                # This portion of the test expects that the connection will fail.
                test_string = '{0} last port tested[{1}]'.format(time.time(), x)
                self.log.debug("Gathering debug information as to whether the "
                           "tester's src ip is authorized for this port test...")
                if self.user.ec2.does_instance_sec_group_allow(
                        instance=instance1,
                        src_addr=src_cidr_ip.split('/')[0],
                        protocol='tcp',
                        port=x):
                    raise ValueError('Group:{0} has {1}:{2} authorized after revoke'
                                     .format(self.group1.name,
                                             src_cidr_ip,
                                             x))
                try:
                    instance1.sys('killall -9 {0} 2> /dev/null'.format(instance1.netcat_name),
                                  timeout=5)
                    instance1.sys('{' + ' ( nohup {0} -k -l {1} > {2} ) &  sleep 1; '
                              .format(instance1.netcat_name, x, test_file) + '}',
                                  code=0, timeout=5)
                    test_port_status(ip=instance1.ip_address,
                                            port=x,
                                            tcp=True,
                                            send_buf=test_string,
                                            verbose=True)
                    #We may still need to test the file content for the UDP case...
                    # Since no socket errors were encountered assume we connected,
                    # check file on instance to make sure we didn't connect somewhere
                    # else like the CC. Dont' error here cuz it's already a bug...
                    instance1.sys('grep "{0}" {1}; echo "" > {1}'
                              .format(test_string, test_file))
                except (socket.error, CommandExitCodeException) as OK:
                    self.status('Port "{0}" successfully revoked on '
                                'instance:{1}/{2}'
                                .format(x, instance1.id, instance1.ip_address))
        self.status('Add and revoke ports test passed')



    def test8_verify_deleting_of_auth_source_group2(self):
        """
        Definition:
        Attempts to delete a security group which has been authorized by another security group.
        -Authorizes group1 access from group2
        -Validates connectivity for instances in group1 can be accessed from group2
        -Deletes group2, validates group1 still allows traffic from other authorized sources
        """
        zones = []
        for zone in self.zones:
            zones.append(TestZone(zone))
        # Make sure the groups are created.
        self.status('Checking and/or create test security groups, and at least one instance'
                    'running in them per zone...')
        self.setup_test_security_groups()
        self.user.ec2.authorize_group(self.group1, port=22, protocol='tcp', cidr_ip='0.0.0.0/0')
        self.user.ec2.authorize_group(self.group2, port=22, protocol='tcp', cidr_ip='0.0.0.0/0')
        for zone in self.zones:
            instances_group1 = []
            instances_group2 = []
            for instance in self.group1_instances:
                if instance.placement == zone:
                    assert isinstance(instance, EuInstance)
                    instances_group1.append(instance)
            if len(instances_group1) < 1:
                self.test1_create_instance_in_zones_for_security_group1(zones=[zone])
            for instance in self.group2_instances:
                if instance.placement == zone:
                    assert isinstance(instance, EuInstance)
                    instances_group2.append(instance)
            if len(instances_group2) < 1:
                self.test2_create_instance_in_zones_for_security_group2(zones=[zone])

        self.status('Clean out any existing rules in group1 to start with a clean group...')
        self.user.ec2.revoke_all_rules(self.group1)
        self.user.ec2.show_security_group(self.group1)
        instance1 = self.group1_instances[0]
        #Add back ssh
        assert not self.user.ec2.does_instance_sec_group_allow(instance=instance1,
                                                         protocol='tcp',
                                                         port=22), \
            'Instance: {0}, security group still allows access after ' \
            'revoking all rules'
        self.status('Authorize group1 access from group testing machine ssh (tcp/22)...')
        self.user.ec2.authorize_group(self.group1,
                               # cidr_ip=str(user.ec2.local_machine_source_ip) + '/32',
                               cidr_ip='0.0.0.0/0', # open to 0/0 to avoid nat issues
                               protocol='tcp',
                               port=22)
        self.user.ec2.authorize_group(self.group1, port=-1, protocol='icmp', cidr_ip='0.0.0.0/0')
        self.user.ec2.show_security_group(self.group1)
        self.status('Test ssh access from this testing machine to each instance in group1...')
        for instance in self.group1_instances:
            try:
                instance.printself()
                self.user.ec2.does_instance_sec_group_allow(instance=instance, protocol='tcp', port=22)
            except:
                pass
            instance.connect_to_instance()
            instance.sys('echo "reset ssh worked"', code=0)
        self.status('Authorizing group2 access to group1...')
        self.user.ec2.authorize_group(self.group1,
                               cidr_ip=None,
                               port=-1,
                               protocol='icmp',
                               src_security_group=self.group2)
        # For debug purposes allow ssh from anywhere here...
        self.user.ec2.authorize_group(self.group1,
                               cidr_ip=None,
                               port=22,
                               protocol='tcp')
        self.status('Sleeping for 10 seconds to allow rule/network'
                            ' to set...')
        time.sleep(10)
        self.user.ec2.show_security_group(self.group1)
        self.status('Checking auth from group2 to group1 instances...')
        self.log.debug('Check some debug information re this data connection in this security '
                   'group first...')
        for zone in zones:
            for instance in self.group1_instances:
                if instance.placement == zone.name:
                    zone.test_instance_group1 = instance
                    if not zone.test_instance_group1.ssh:
                        self.status('Instance in group1 did not have an ssh connection, '
                                    'trying to setup ssh now...')
                        self.user.ec2.show_security_groups_for_instance(zone.test_instance_group1)
                        self.log.debug('ssh connect using instance:"{0}", keypath:"{1}"'
                                   .format(zone.test_instance_group1,
                                           zone.test_instance_group1.keypath))
                        zone.test_instance_group1.connect_to_instance()
                    break
            for instance in self.group2_instances:
                if instance.placement == zone.name:
                    zone.test_instance_group2 = instance
                    if not zone.test_instance_group2.ssh:
                        self.status('Instance in group1 did not have an ssh connection, '
                                    'trying to setup ssh now...')
                        self.user.ec2.show_security_groups_for_instance(zone.test_instance_group2)
                        self.log.debug('ssh connect using instance:"{0}", keypath:"{1}"'
                                   .format(zone.test_instance_group2,
                                           zone.test_instance_group2.keypath))
                        zone.test_instance_group2.connect_to_instance()
                    break
            if not zone.test_instance_group1:
                raise ValueError('Could not find instances in sec group1'
                                 'group for zone:' + str(zone.name))
            if not zone.test_instance_group2:
                raise ValueError('Could not find instances in sec group2'
                                 'group for zone:' + str(zone.name))

            assert isinstance(zone.test_instance_group1, EuInstance)
            assert isinstance(zone.test_instance_group2, EuInstance)
        for zone in zones:
            #Make sure the instance in group1 has allowed icmp access from group2
            allowed = False

            if self.user.ec2.does_instance_sec_group_allow(
                    instance=zone.test_instance_group1,
                    src_group=self.group2,
                    protocol='icmp',
                    port='-1'):
                allowed = True
            if not allowed:
                raise ValueError('Group2 instance not allowed in group1'
                                 ' after authorizing group2')

            self.status('Attempting to ping group1 instance from group2 '
                        'instance using their private IPs')
            try:
                zone.test_instance_group2.ssh.verbose = True
                zone.test_instance_group2.sys(
                    'ping -c 1 {0}'
                    .format(zone.test_instance_group1.private_ip_address),
                    code=0,verbose=True)
            except:
                self.errormsg('Failed to ping from group2 to group1 instance '
                              'after authorizing the source group2')
                raise
        self.status('Terminating all instances in group2 in order to delete '
                    'security group2')
        self.user.ec2.terminate_instances(self.group2_instances)
        self.group2_instances = []
        self.user.ec2.delete_group(self.group2)
        self.status('Now confirm that ssh still works for all instances in group1')
        for instance in self.group1_instances:
            self.user.ec2.show_security_groups_for_instance(instance)
            self.log.debug('Attempting to connect to instance from source IP: "{0}"'
                       .format(self.user.ec2.local_machine_source_ip))
            instance.connect_to_instance(timeout=300)
            instance.sys('echo "Getting hostname from {0}"; hostname'
                         .format(instance.id), code=0)
        self.status('Passed. Group1 ssh working after deleting src group which '
                    'was authorized to group1')

    def test9_ssh_between_instances_same_group_same_zone_public(self):
        """
        Definition:
        For each zone this test will attempt to test ssh between two instances in the same
        security group using the public ips of the instances.
        -Authorize group for ssh access
        -Re-use or create 2 instances within the same security group, same zone
        -For each zone, attempt to ssh to a vm in the same security group same zone
        """
        self.user.ec2.authorize_group(self.group1, port=22, protocol='tcp', cidr_ip='0.0.0.0/0')
        self.user.ec2.authorize_group(self.group1, port=-1, protocol='icmp', cidr_ip='0.0.0.0/0')
        for zone in self.zones:
            instances =[]
            for instance in self.group1_instances:
                if instance.placement == zone:
                    assert isinstance(instance, EuInstance)
                    instances.append(instance)
            if len(instances) < 2:
                for x in xrange(len(instances), 2):
                    self.test1_create_instance_in_zones_for_security_group1(zones=[zone])
        for zone in self.zones:
            zone_instances = []
            for instance in self.group1_instances:
                if instance.placement == zone:
                    zone_instances.append(instance)
            instance1 = zone_instances[0]
            instance2 = zone_instances[1]
            instance1.ssh.sftp_put(instance1.keypath, 'testkey.pem')
            instance1.sys('chmod 0600 testkey.pem')
            testphrase = "pubsamezone_test_from_instance1_{0}".format(instance1.id)
            testfile = 'testfile.txt'
            retry = 2
            for x in xrange(0, retry):
                try:
                    instance1.sys("ssh -o StrictHostKeyChecking=no -i testkey.pem root@{0} "
                                  "\'echo {1} > {2}; hostname; ifconfig; pwd; ls\'"
                                  .format(instance2.ip_address, testphrase, testfile),
                                  code=0, timeout=20)
                    break
                except (CommandTimeoutException, CommandExitCodeException) as CE:
                    self.status('Attempt #{0} to connect between instances failed:"{1}'
                                .format(x, str(CE)))
                    if x:
                        raise
            instance2.sys('hostname; ifconfig; pwd; ls; cat {0} | grep {1}'
                          .format(testfile, testphrase), code=0)

    def test10_ssh_between_instances_same_group_public_different_zone(self):
        """
        Definition:
        If multiple zones are detected, this test will attempt to test ssh between
        two instances in the same security group and accross each zone using the public ips
        of the instances
        -Authorize group for ssh access
        -Re-use or create 2 instances within the same security group, different zone(s)
        -For each zone, attempt to ssh to a vm in the same security group different zone(s)
        """
        if len(self.zones) < 2:
            raise SkipTestException('Skipping multi-zone test, '
                                    'only a single zone found or provided')
        self.user.ec2.authorize_group(self.group1, port=22, protocol='tcp', cidr_ip='0.0.0.0/0')
        self.user.ec2.authorize_group(self.group1, port=-1, protocol='icmp', cidr_ip='0.0.0.0/0')
        zone_instances = {}
        for zone in self.zones:
            instances =[]
            for instance in self.group1_instances:
                if instance.placement == zone:
                    assert isinstance(instance, EuInstance)
                    instances.append(instance)
            if len(instances) < 1:
                for x in xrange(len(instances), 1):
                    self.test1_create_instance_in_zones_for_security_group1(zones=[zone])
            zone_instances[zone] = instances
        for zone1 in self.zones:
            instance1 = zone_instances[zone1][0]
            instance1.ssh.sftp_put(instance1.keypath, 'testkey.pem')
            instance1.sys('chmod 0600 testkey.pem')
            for zone2 in self.zones:
                if zone1 != zone2:
                    instance2 = zone_instances[zone2][0]
                    testphrase = "diffpubzone_test_from_instance1_{0}".format(instance1.id)
                    testfile = 'testfile.txt'
                    instance1.sys("ssh -o StrictHostKeyChecking=no -i testkey.pem root@{0} "
                                  "\'echo {1} > {2}; hostname; ifconfig; pwd; ls\'"
                                  .format(instance2.ip_address, testphrase, testfile),
                                  code=0,
                                  timeout=10)
                    instance2.sys('cat {0} | grep {1}'.format(testfile, testphrase), code=0)

    def test11_ssh_between_instances_same_group_same_zone_private(self):
        """
        Definition:
        For each zone this test will attempt to test ssh between two instances in the same
        security group using the private ips of the instances.
        -Authorize group for ssh access
        -Re-use or create 2 instances within the same security group, same zone
        -For each zone, attempt to ssh to a vm in the same security group same zone
        """
        # Remove all rules from the group and add back the minimum amount of rules to run
        # this test...
        self.user.ec2.revoke_all_rules(self.group1)
        time.sleep(1)
        self.user.ec2.authorize_group(self.group1, port=22, protocol='tcp', cidr_ip='0.0.0.0/0')
        self.user.ec2.authorize_group(self.group1, port=-1, protocol='icmp', cidr_ip='0.0.0.0/0')
        self.status('Using 2 instances from each zone within the following security group to'
                    'test private ip connectivity:"{0}"'.format(self.group1))
        self.user.ec2.show_security_group(self.group1)

        for zone in self.zones:
            instances =[]
            for instance in self.group1_instances:
                if instance.placement == zone:
                    assert isinstance(instance, EuInstance)
                    instances.append(instance)
            if len(instances) < 2:
                for x in xrange(len(instances), 2):
                    self.test1_create_instance_in_zones_for_security_group1(zones=[zone])

        for zone in self.zones:
            zone_instances = []
            zone_name = getattr(zone, 'name', None) or zone
            for instance in self.group1_instances:
                if instance.placement == zone_name:
                    zone_instances.append(instance)
            instance1 = zone_instances[0]
            instance2 = zone_instances[1]
            instance1.ssh.sftp_put(instance1.keypath, 'testkey.pem')
            instance1.sys('chmod 0600 testkey.pem')
            testphrase = "hello_from_instance1_{0}".format(instance1.id)
            testfile = 'testfile.txt'
            self.status("Attempting to ssh from instance:{0} to instance:{1}'s private ip:{2}"
                        .format(instance1.id, instance2.id, instance2.private_ip_address))
            try:
                instance1.sys("ssh -o StrictHostKeyChecking=no -i testkey.pem root@{0} "
                              "\'echo {1} > {2}; hostname; ifconfig; pwd; ls\'"
                              .format(instance2.private_ip_address, testphrase, testfile),
                              code=0,
                              timeout=10)
            except Exception, se:
                self.status('First attempt to ssh between instances failed, err: ' + str(se) +
                            '\nIncreasing command timeout to 20 seconds, and trying again. ')
                instance1.sys("ssh -o StrictHostKeyChecking=no -i testkey.pem root@{0} "
                              "\'echo {1} > {2}; hostname; ifconfig; pwd; ls\'"
                              .format(instance2.private_ip_address, testphrase, testfile),
                              code=0,
                              timeout=20)
            self.status('Cat the test file create from the ssh cmd {0} ran on on {1}...'
                        .format(instance1, instance2))
            instance2.sys('cat {0} | grep {1}'.format(testfile, testphrase), code=0)

    def test12_ssh_between_instances_same_group_private_different_zone(self):
        """
        Definition:
        If multiple zones are detected, this test will attempt to test ssh between
        two instances in the same security group and across each zone using the instances'
        private ip addresses.
        -Authorize group for ssh access
        -Re-use or create 2 instances within the same security group, different zone(s)
        -For each zone, attempt to ssh to a vm in the same security group different zone(s)
        """
        if len(self.zones) < 2:
            raise SkipTestException('Skipping multi-zone test, '
                                    'only a single zone found or provided')
        self.user.ec2.authorize_group(self.group1, port=22, protocol='tcp', cidr_ip='0.0.0.0/0')
        self.user.ec2.authorize_group(self.group1, port=-1, protocol='icmp', cidr_ip='0.0.0.0/0')
        for zone in self.zones:
            instances =[]
            for instance in self.group1_instances:
                if instance.placement == zone:
                    assert isinstance(instance, EuInstance)
                    instances.append(instance)
            if len(instances) < 1:
                for x in xrange(len(instances), 1):
                    self.test1_create_instance_in_zones_for_security_group1(zones=[zone])
        for zone1 in self.zones:
            zone_instances = []
            for instance in self.group1_instances:
                if instance.placement == zone1:
                    zone_instances.append(instance)
            instance1 = zone_instances[0]
            instance1.ssh.sftp_put(instance1.keypath, 'testkey.pem')
            instance1.sys('chmod 0600 testkey.pem')
            for zone2 in self.zones:
                if zone1 != zone2:
                    zone2_instances = []
                    for instance in self.group1_instances:
                        if instance.placement == zone2:
                            zone2_instances.append(instance)
                    instance2 = zone_instances[0]
                    testphrase = "diffprivzone_test_from_instance1_{0}".format(instance1.id)
                    testfile = 'testfile.txt'
                    instance1.sys("ssh -o StrictHostKeyChecking=no -i testkey.pem root@{0} "
                                  "\'echo {1} > {2}; hostname; ifconfig; pwd; ls\'"
                                  .format(instance2.private_ip_address, testphrase, testfile),
                                  code=0,
                                  timeout=10)
                    instance2.sys('cat {0} | grep {1}'.format(testfile, testphrase), code=0)

    def test13_ssh_between_instances_diff_group_private_different_zone(self):
        """
        Definition:
        If multiple zones are detected, this test will attempt to test ssh between
        two instances in the same security group and across each zone using the instances'
        private ip addresses.
        -Authorize group for ssh access
        -Re-use or create 2 instances within the same security group, different zone(s)
        -For each zone, attempt to ssh to a vm in the same security group different zone(s)
        """
        if len(self.zones) < 2:
            raise SkipTestException('Skipping multi-zone test, '
                                    'only a single zone found or provided')
        self.user.ec2.authorize_group(self.group1, port=22, protocol='tcp', cidr_ip='0.0.0.0/0')
        self.user.ec2.authorize_group(self.group1, port=-1, protocol='icmp', cidr_ip='0.0.0.0/0')
        # In case a previous test has deleted group2...
        self.group2 = self.user.ec2.add_group(self.group2.name)
        self.user.ec2.authorize_group(self.group2, port=22, protocol='tcp', cidr_ip='0.0.0.0/0')
        self.user.ec2.authorize_group(self.group2, port=-1, protocol='icmp', cidr_ip='0.0.0.0/0')
        for zone in self.zones:
            instance1 = None
            instances =[]
            for instance in self.group1_instances:
                if instance.placement == zone:
                    instance1 = instance
            if not instance1:
                self.test1_create_instance_in_zones_for_security_group1(zones=[zone])
                for instance in self.group1_instances:
                    if instance.placement == zone:
                        instance1 = instance
            instance1.ssh.sftp_put(instance1.keypath, 'testkey.pem')
            instance1.sys('chmod 0600 testkey.pem')
            for zone2 in self.zones:
                instance2 = None
                if zone2 != zone:
                    for instance in self.group2_instances:
                        if instance.placement == zone2:
                            instance2 = instance
                    if not instance2:
                        self.test2_create_instance_in_zones_for_security_group2(zones=[zone2],
                                                                                auto_connect=True)
                        for instance in self.group2_instances:
                            if instance.placement == zone2:
                                instance2 = instance
                    testphrase = "diffprivzone_test_from_instance1_{0}".format(instance1.id)
                    testfile = 'testfile.txt'
                    self.status('Testing instance:{0} zone:{1} --ssh--> instance:{2} zone:{3} '
                                '-- private ip'.format(instance1.id, zone,instance2.id, zone2))
                    instance1.sys("ssh -o StrictHostKeyChecking=no -i testkey.pem root@{0} "
                                  "\'echo {1} > {2}; hostname; ifconfig; pwd; ls\'"
                                  .format(instance2.private_ip_address, testphrase, testfile),
                                  code=0,
                                  timeout=10)
                    instance2.sys('cat {0} | grep {1}'.format(testfile, testphrase), code=0)

    def test14_ssh_between_instances_diff_group_public_different_zone(self):
        """
        Definition:
        If multiple zones are detected, this test will attempt to test ssh between
        two instances in the same security group and across each zone using the instances'
        private ip addresses.
        -Authorize group for ssh access
        -Re-use or create 2 instances within the same security group, different zone(s)
        -For each zone, attempt to ssh to a vm in the same security group different zone(s)
        """
        if len(self.zones) < 2:
            raise SkipTestException('Skipping multi-zone test, '
                                    'only a single zone found or provided')
        self.user.ec2.authorize_group(self.group1, port=22, protocol='tcp', cidr_ip='0.0.0.0/0')
        self.user.ec2.authorize_group(self.group1, port=-1, protocol='icmp', cidr_ip='0.0.0.0/0')
        # In case a previous test has deleted group2...
        self.group2 = self.user.ec2.add_group(self.group2.name)
        self.user.ec2.authorize_group(self.group2, port=22, protocol='tcp', cidr_ip='0.0.0.0/0')
        self.user.ec2.authorize_group(self.group2, port=-1, protocol='icmp', cidr_ip='0.0.0.0/0')
        for zone in self.zones:
            instance1 = None
            instances =[]
            for instance in self.group1_instances:
                if instance.placement == zone:
                    instance1 = instance
            if not instance1:
                self.test1_create_instance_in_zones_for_security_group1(zones=[zone])
                for instance in self.group1_instances:
                    if instance.placement == zone:
                        instance1 = instance
            instance1.ssh.sftp_put(instance1.keypath, 'testkey.pem')
            instance1.sys('chmod 0600 testkey.pem')
            for zone2 in self.zones:
                instance2 = None
                if zone2 != zone:
                    for instance in self.group2_instances:
                        if instance.placement == zone2:
                            instance2 = instance
                    if not instance2:
                        self.test2_create_instance_in_zones_for_security_group2(zones=[zone2],
                                                                                auto_connect=True)
                        for instance in self.group2_instances:
                            if instance.placement == zone2:
                                instance2 = instance
                    testphrase = "diffprivzone_test_from_instance1_{0}".format(instance1.id)
                    testfile = 'testfile.txt'
                    self.status('Testing instance:{0} zone:{1} --ssh--> instance:{2} zone:{3} '
                                '-- private ip'.format(instance1.id, zone,instance2.id, zone2))
                    instance1.sys("ssh -o StrictHostKeyChecking=no -i testkey.pem root@{0} "
                                  "\'echo {1} > {2}; hostname; ifconfig; pwd; ls\'"
                                  .format(instance2.ip_address, testphrase, testfile),
                                  code=0,
                                  timeout=10)
                    instance2.sys('cat {0} | grep {1}'.format(testfile, testphrase), code=0)


    # add revoke may be covered above...?
    def test_revoke_rules(self):

        revoke_group = self.user.ec2.add_group("revoke-group-" + str(int(time.time())))
        self.user.ec2.authorize_group(revoke_group, protocol='tcp', port=22)
        for zone in self.zones:
            instance = self.user.ec2.run_image(image=self.image,
                                                 keypair=self.keypair,
                                                 subnet_id = self.subnet_id,
                                                 group=revoke_group,
                                                 systemconnection=self.sysadmin,
                                                 zone=zone)[0]
            self.user.ec2.revoke_security_group(revoke_group, from_port=22, protocol='tcp')
            self.log.debug('Sleeping for 60 seconds before retrying group')
            time.sleep(60)
            try:
                instance.reset_ssh_connection(timeout=30)
                self.user.ec2.delete_group(revoke_group)
                raise Exception("Was able to SSH without authorized rule")
            except SSHException, e:
                self.log.debug("SSH was properly blocked to the instance")
            self.user.ec2.authorize_group(revoke_group, protocol='tcp', port=22)
            instance.reset_ssh_connection()
            self.user.ec2.terminate_instances(instance)
        self.user.ec2.delete_group(revoke_group)


    def _run_suite(self, testlist=None, basic_only=False, exclude=None):
        # The first tests will have the End On Failure flag set to true. If these tests fail
        # the remaining tests will not be attempted.
        unit_list = []
        testlist = testlist or []
        exclude = exclude or []
        if exclude:
            exclude = re.sub('[",]', " ", str(exclude)).split()
        if testlist:
            if not isinstance(testlist, list):
                testlist.replace(',',' ')
                testlist = testlist.split()
            for test in testlist:
                unit_list.append(nettests.create_testunit_by_name(test))
        else:
            unit_list =[
                self.create_testunit_by_name('test1_create_instance_in_zones_for_security_group1',
                                                 eof=True),
                self.create_testunit_by_name('test2_create_instance_in_zones_for_security_group2',
                                                 eof=True),
                self.create_testunit_by_name(
                    'test3_test_ssh_between_instances_in_diff_sec_groups_same_zone', eof=True)]
            if basic_only:
                testlist = []
            else:
                # Then add the rest of the tests...
                testlist = [ 'test4_attempt_unauthorized_ssh_from_test_machine_to_group2',
                             'test5_test_ssh_between_instances_in_same_sec_groups_different_zone',
                             'test7_add_and_revoke_tcp_port_range',
                             'test8_verify_deleting_of_auth_source_group2',
                             'test9_ssh_between_instances_same_group_same_zone_public',
                             'test10_ssh_between_instances_same_group_public_different_zone',
                             'test11_ssh_between_instances_same_group_same_zone_private',
                             'test12_ssh_between_instances_same_group_private_different_zone',
                             'test13_ssh_between_instances_diff_group_private_different_zone',
                             'test14_ssh_between_instances_diff_group_public_different_zone']
            for test in exclude:
                if test in testlist:
                    testlist.remove(test)
            for test in testlist:
                unit_list.append(self.create_testunit_by_name(test))
        self.status('Got running the following list of tests:' + str(testlist))

        ### Run the nephoriaUnitTest objects
        result = self.run(unit_list,eof=False,clean_on_exit=True)
        self.status('Test finished with status:"{0}"'.format(result))
        return result

if __name__ == "__main__":
    nettests = NetTestsClassic()
    exit(nettests._run_suite(testlist=nettests.args.test_list))

