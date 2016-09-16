# Software License Agreement (BSD License)
#
# Copyright (c) 2009-2014, Eucalyptus Systems, Inc.
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
# Author: tony@eucalyptus.com
import re
import copy
import time
import boto
from boto.ec2.autoscale import ScalingPolicy, Instance
from boto.ec2.autoscale import Tag
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup, AutoScaleConnection
from boto.ec2.regioninfo import RegionInfo
from boto.connection import BotoServerError
from nephoria.baseops.botobaseops import BotoBaseOps
from nephoria.aws.ec2.ec2ops import EC2ops


class ASops(BotoBaseOps):
    EUCARC_URL_NAME = 'auto_scaling_url'
    SERVICE_PREFIX = 'autoscaling'
    CONNECTION_CLASS = AutoScaleConnection

    def setup(self):
        super(ASops, self).setup()
        #Source ip on local test machine used to reach instances
        self.as_source_ip = None

    def setup_resource_trackers(self):
        self.log.warning('No resource trackers have been implemented for: {0}'
                         .format(self.__class__.__name__))

    def create_launch_config(self, name, image_id, key_name=None, security_groups=None, user_data=None,
                             instance_type=None, kernel_id=None, ramdisk_id=None, block_device_mappings=None,
                             instance_monitoring=False, instance_profile_name=None):
        """
        Creates a new launch configuration with specified attributes.

        :param name: Name of the launch configuration to create. (Required)
        :param image_id: Unique ID of the Amazon Machine Image (AMI) assigned during registration. (Required)
        :param key_name: The name of the EC2 key pair.
        :param security_groups: Names of the security groups with which to associate the EC2 instances.
        """
        lc = LaunchConfiguration(name=name,
                                 image_id=image_id,
                                 key_name=key_name,
                                 security_groups=security_groups,
                                 user_data=user_data,
                                 instance_type=instance_type,
                                 kernel_id=kernel_id,
                                 ramdisk_id=ramdisk_id,
                                 block_device_mappings=block_device_mappings,
                                 instance_monitoring=instance_monitoring,
                                 instance_profile_name=instance_profile_name)
        self.log.debug("Creating launch config: " + name)
        self.connection.create_launch_configuration(lc)
        if len(self.describe_launch_config([name])) != 1:
            raise Exception('Launch Config not created')
        self.log.debug('SUCCESS: Created Launch Config: ' +
                   self.describe_launch_config([name])[0].name)

    def describe_launch_config(self, names=None):
        """
        return a list of launch configs

        :param names: list of names to query (optional) otherwise return all launch configs
        :return:
        """
        return self.connection.get_all_launch_configurations(names=names)

    def get_all_launch_config_names(self):
        """
        Returns a list of all launch configuration names.
        :return:
        """
        lc = self.connection.get_all_launch_configurations()

        if len(lc) > 1:
            l = len(lc)
            for i in (0, l - 1):
                lc[i] = str(lc[i].name)
        elif len(lc) == 1:
            lc[0] = str(lc[0].name)
        return lc

    def delete_launch_config(self, launch_config_name):
        self.log.debug("Deleting launch config: " + launch_config_name)
        self.connection.delete_launch_configuration(launch_config_name)
        if len(self.describe_launch_config([launch_config_name])) != 0:
            raise Exception('Launch Config not deleted')
        self.log.debug('SUCCESS: Deleted Launch Config: ' + launch_config_name)

    def create_as_group(self, group_name, launch_config, availability_zones, min_size, max_size, load_balancers=None,
                        desired_capacity=None, termination_policies=None, default_cooldown=None, health_check_type=None,
                        health_check_period=None, tags=None):
        """
        Create auto scaling group.

        :param group_name: Name of autoscaling group (required).
        :param load_balancers: List of load balancers.
        :param availability_zones: List of availability zones (required).
        :param launch_config: Name of launch configuration (required).
        :param min_size:  Minimum size of group (required).
        :param max_size: Maximum size of group (required).
        """
        self.log.debug("Creating Auto Scaling group: " + group_name)
        as_group = AutoScalingGroup(connection=self.connection,
                                    group_name=group_name,
                                    load_balancers=load_balancers,
                                    availability_zones=availability_zones,
                                    launch_config=launch_config,
                                    min_size=min_size,
                                    max_size=max_size,
                                    desired_capacity=desired_capacity,
                                    default_cooldown=default_cooldown,
                                    health_check_type=health_check_type,
                                    health_check_period=health_check_period,
                                    tags=tags,
                                    termination_policies=termination_policies)
        self.connection.create_auto_scaling_group(as_group)

        as_group = self.describe_as_group(group_name)

        self.log.debug("SUCCESS: Created Auto Scaling Group: " + as_group.name)
        return as_group

    def describe_as_group(self, name):
        """
        Returns a full description of each Auto Scaling group in the given
        list. This includes all Amazon EC2 instances that are members of the
        group. If a list of names is not provided, the service returns the full
        details of all Auto Scaling groups.
        :param name:
        :return:
        """
        if not name:
            raise ValueError('No name provided for as group, got:{0}'.format(name))
        groups = self.connection.get_all_groups(names=[name])
        if len(groups) > 1:
            raise Exception("More than one group with name: " + str(name))
        if len(groups) == 0:
            raise Exception("No group found with name: " + str(name))
        return groups[0]

    def get_all_group_names(self):
        """
        Returns a list of all autoscaling group names.
        :return:
        """
        groups = self.connection.get_all_groups()

        if len(groups) > 1:
            l=len(groups)
            for i in (0,l-1):
                groups[i] = str(groups[i].name)
        elif len(groups) == 1:
            groups[0] = str(groups[0].name)

        return groups

    def delete_all_groups_and_launch_configs(self):
        """
         Terminates all autoscaling instances. Deletes all autoscaling groups and all launch configs.
        """

        groups=self.get_all_group_names()
        lcs = self.get_all_launch_config_names()
        g = len(groups)
        if len(groups) > 0:
            if len(lcs) == 0:
                emi = EC2ops.get_emi()
                self.create_launch_config(name='lc-helper', instance_type='m1.small', image_id=emi)
                lcs = self.get_all_launch_config_names()
            for i in range(g):
                try:
                    self.update_as_group(group_name=groups[i], min_size=0, max_size=0, desired_capacity=0, launch_config=lcs[0])
                except BotoServerError:
                    self.log.debug('Could not update autoscaling group')
                    pass

                for j in range(10):
                    try:
                        self.describe_as_group(groups[i])
                        try:
                            self.delete_as_group(groups[i])
                            break
                        except BotoServerError:
                            time.sleep(30)
                            pass
                    except BotoServerError:
                        pass


        lcs = self.get_all_launch_config_names()
        l = len(lcs)
        if l > 1:
            for i in (0, l-1):
                self.connection.delete_launch_configuration(lcs[i])
        elif l == 1:
            self.connection.delete_launch_configuration(lcs[0])


    def delete_as_group(self, name=None, force=None):
        self.log.debug("Deleting Auto Scaling Group: " + name)
        self.log.debug("Forcing: " + str(force))
        # self.autoscale.set_desired_capacity(group_name=names, desired_capacity=0)
        self.connection.delete_auto_scaling_group(name=name, force_delete=force)
        try:
            self.describe_as_group([name])
            raise Exception('Auto Scaling Group not deleted')
        except:
            self.log.debug('SUCCESS: Deleted Auto Scaling Group: ' + name)

    def create_as_policy(self, name, adjustment_type, scaling_adjustment, as_name, cooldown=None):
        """
        Create an auto scaling policy

        :param name:
        :param adjustment_type: (ChangeInCapacity, ExactCapacity, PercentChangeInCapacity)
        :param scaling_adjustment:
        :param as_name:
        :param cooldown: (if something gets scaled, the wait in seconds before trying again.)
        """
        scaling_policy = ScalingPolicy(name=name,
                                       adjustment_type=adjustment_type,
                                       as_name=as_name,
                                       scaling_adjustment=scaling_adjustment,
                                       cooldown=cooldown)
        self.log.debug("Creating Auto Scaling Policy: " + name)
        self.connection.create_scaling_policy(scaling_policy)

    def describe_as_policies(self, as_group=None, policy_names=None):
        """
        If no group name or list of policy names are provided, all
        available policies are returned.

        :param as_group:
        :param policy_names:
        """
        self.connection.get_all_policies(as_group=as_group, policy_names=policy_names)

    def execute_as_policy(self, policy_name=None, as_group=None, honor_cooldown=None):
        self.log.debug("Executing Auto Scaling Policy: " + policy_name)
        self.connection.execute_policy(policy_name=policy_name, as_group=as_group, honor_cooldown=honor_cooldown)

    def delete_as_policy(self, policy_name=None, autoscale_group=None):
        self.log.debug("Deleting Policy: " + policy_name + " from group: " + autoscale_group)
        self.connection.delete_policy(policy_name=policy_name, autoscale_group=autoscale_group)

    def cleanup_autoscaling_groups(self, asg_list = None):
        """
        This will attempt to delete auto scaling groups listed in test_resources['auto-scaling-groups']
        """
        ### clear all ASGs
        if not asg_list:
            auto_scaling_groups=self.test_resources['auto-scaling-groups']
        else:
            auto_scaling_groups = asg_list
        for asg in auto_scaling_groups:
            self.log.debug("Found Auto Scaling Group: " + asg.name)
            self.delete_as_group(name=asg.name, force=True)

    def delete_all_autoscaling_groups(self):
        """
        This will attempt to delete all launch configs and all auto scaling groups
        """
        ### clear all ASGs
        for asg in self.describe_as_group():
            self.log.debug("Found Auto Scaling Group: " + asg.name)
            self.delete_as_group(name=asg.name, force=True)
        if len(self.describe_as_group(asg.name)) != 0:
            self.log.debug("Some AS groups remain")
            for asg in self.describe_as_group():
                self.log.debug("Found Auto Scaling Group: " + asg.name)

    def cleanup_launch_configs(self):
        """
        This will attempt to delete launch configs listed in test_resources['launch-configurations']
        """
        launch_configurations=self.test_resources['launch-configurations']

        if not launch_configurations:
            self.log.debug("Launch configuration list is empty")
        else:
            for lc in launch_configurations:
                self.log.debug("Found Launch Config:" + lc.name)
                self.delete_launch_config(lc.name)

    def delete_all_launch_configs(self):
        ### clear all LCs
        """
        Attempt to remove all launch configs
        """
        for lc in self.describe_launch_config():
            self.log.debug("Found Launch Config:" + lc.name)
            self.delete_launch_config(lc.name)
        if len(self.describe_launch_config()) != 0:
            self.log.debug("Some Launch Configs Remain")
            for lc in self.describe_launch_config():
                self.log.debug("Found Launch Config:" + lc.name)

    def get_last_instance_id(self, tester=None):
        reservations = tester.ec2.connection.get_all_instances()
        instances = [i for r in reservations for i in r.instances]
        newest_time = None
        newest_id = None
        for i in instances:
            if not newest_time or i.launch_time > newest_time:
                newest_time = i.launch_time
                newest_id = i.id
        return newest_id

    def create_group_tag(self, key, value, resource_id, propagate_at_launch=None):
        # self.debug("Number of tags: " + str(len(self.tester.autoscale.get_all_tags())))
        # self.debug("Autoscale group info: " + str(self.tester.autoscale.get_all_groups(names=[auto_scaling_group_name])[0].tags))

        tag = Tag(key=key, value=value, propagate_at_launch=propagate_at_launch, resource_id=resource_id)
        self.connection.create_or_update_tags([tag])
        if len(self.connection.get_all_tags(filters=key)) != 1:
            self.log.debug("Number of tags: " + str(len(self.connection.get_all_tags(filters=key))))
            raise Exception('Tag not created')
        self.log.debug("created or updated tag: " + str(self.connection.get_all_tags(filters=key)[0]))

    def delete_all_group_tags(self):
        all_tags = self.connection.get_all_tags()
        self.connection.delete_tags(all_tags)
        self.log.debug("Number of tags: " + str(len(self.connection.get_all_tags())))

    def delete_all_policies(self):
        policies = self.connection.get_all_policies()
        for policy in policies:
            self.delete_as_policy(policy_name=policy.name, autoscale_group=policy.as_name)
        if len(self.connection.get_all_policies()) != 0:
            raise Exception('Not all auto scaling policies deleted')
        self.log.debug("SUCCESS: Deleted all auto scaling policies")

    def update_as_group(self, group_name, launch_config, min_size, max_size, availability_zones=None,
                        desired_capacity=None, termination_policies=None, default_cooldown=None, health_check_type=None,
                        health_check_period=None):
        """

        :param group_name: REQUIRED
        :param launch_config: REQUIRED
        :param min_size: REQUIRED
        :param max_size: REQUIRED
        :param availability_zones:
        :param desired_capacity:
        :param termination_policies:
        :param default_cooldown:
        :param health_check_type:
        :param health_check_period:
        """
        self.log.debug("Updating ASG: " + group_name)
        return AutoScalingGroup(connection=self.connection,
                                name=group_name,
                                launch_config=launch_config,
                                min_size=min_size,
                                max_size=max_size,
                                availability_zones=availability_zones,
                                desired_capacity=desired_capacity,
                                default_cooldown=default_cooldown,
                                health_check_type=health_check_type,
                                health_check_period=health_check_period,
                                termination_policies=termination_policies).update()

    def wait_for_instances(self, group_name, number=1, tester=None):
        asg = self.describe_as_group(group_name)
        instances = asg.instances
        if not instances:
            self.log.debug("No instances in ASG")
            return False
        if len(asg.instances) != number:
            self.log.debug("Instances not yet allocated")
            return False
        for instance in instances:
            assert isinstance(instance, Instance)
            instance = tester.ec2.get_instances(idstring=instance.instance_id)[0]
            if instance.state != "running":
                self.log.debug("Instance: " + str(instance) + " still in " + instance.state + " state")
                return False
            else:
                self.log.debug("Instance: " + str(instance) + " now running")
        return True
