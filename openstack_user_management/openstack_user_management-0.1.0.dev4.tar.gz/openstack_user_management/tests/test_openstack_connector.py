#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from openstack_user_management.connectors.openstack_connector import OpenstackConnector


class TestOpenstackConnector(unittest.TestCase):
    conn = OpenstackConnector()

    def test_template(self):
        self.assertTrue(True)

    def test_openstackclient(self):
        print self.conn.client_manager
        print self.conn.neutron_manager

    def test_username_availability(self):
        self.assertTrue(self.conn.check_username_availability("demo2"))
        self.assertFalse(self.conn.check_username_availability("demo"))

    def test_project_name_availability(self):
        self.assertTrue(self.conn.check_projectname_availability("demo2"))
        self.assertFalse(self.conn.check_projectname_availability("demo"))

    def test_project_creation(self):
        self.conn.create_project("default",
                                 "mydescription",
                                 "myproject4",
                                 'univ',
                                 'ITU')
        self.conn.create_project("default",
                                 "mydescription",
                                 "a@a.com",
                                 'univ',
                                 'YTU')
        self.assertFalse(self.conn.create_project("default",
                                                  "mydescription",
                                                  "myproject4",
                                                  'univ',
                                                  'YTU'))

    def test_user_creation(self):
        self.conn.create_user("default",
                              "testuser@testuser.com",
                              "testuser",
                              "testuser")
        self.assertFalse(self.conn.create_user("default",
                                               "testuser@testuser.com",
                                               "testuser",
                                               "testuser"))

    def test_pair_user_with_project(self):
        self.assertTrue(self.conn.pair_user_with_project("testuser",
                                                         "myproject4",
                                                         "Member"))

    def test_update_project_status(self):
        self.assertTrue(self.conn.update_project_status("myproject4",
                                                        enabled=True))

    def test_update_user_status(self):
        self.assertTrue(self.conn.update_user_status("testuser",
                                                     enabled=True))

    def test_init_network(self):
        subnet_gateway_ip = '10.0.0.1'
        subnet_cidr = '10.0.0.0/24'
        dns_nameservers = ['10.1.0.1']
        self.assertTrue(self.conn.init_network("a@a.com",
                                               "ext_net",
                                               dns_nameservers,
                                               subnet_cidr,
                                               subnet_gateway_ip))

if __name__ == "__main__":
    unittest.main(verbosity=2)
