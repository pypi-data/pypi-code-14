#!/usr/bin/python
# -*- coding: utf-8 -*-

from mock import MagicMock as Mock
from unittest import TestCase

from cloudshell.networking.brocade.brocade_connectivity_operations import BrocadeConnectivityOperations


class TestBrocadeConnectivityOperations(TestCase):
    def setUp(self):
        self._context = Mock()
        self._api = Mock()
        self._cli_service = Mock()
        self._logger = Mock()
        self._connectivity_operations_instance = BrocadeConnectivityOperations(context=self._context,
                                                                               api=self._api,
                                                                               cli_service=self._cli_service,
                                                                               logger=self._logger)

    def test_validate_vlan_methods_incoming_parameters_empty_port(self):
        self.assertRaises(Exception,
                          self._connectivity_operations_instance.validate_vlan_methods_incoming_parameters,
                          "2, 3, 5-8, 7", "", "access")

    def test_validate_vlan_methods_incoming_parameters_wrong_port_mode(self):
        self.assertRaises(Exception,
                          self._connectivity_operations_instance.validate_vlan_methods_incoming_parameters,
                          "2, 3, 5-8, 7", "ethernet 2/1", "wrong_port_mode")

    def test_validate_vlan_methods_incoming_parameters_access_and_empty_vlan(self):
        self.assertRaises(Exception,
                          self._connectivity_operations_instance.validate_vlan_methods_incoming_parameters,
                          "", "ethernet 2/1", "access")

    def test_validate_vlan_methods_incoming_parameters_access_and_vlan_range_1(self):
        self.assertRaises(Exception,
                          self._connectivity_operations_instance.validate_vlan_methods_incoming_parameters,
                          "2, 3, 5", "ethernet 2/1", "access")

    def test_validate_vlan_methods_incoming_parameters_access_and_vlan_range_2(self):
        self.assertRaises(Exception,
                          self._connectivity_operations_instance.validate_vlan_methods_incoming_parameters,
                          "5-7", "ethernet 2/1", "access")

    def test_get_vlan_list_success(self):
        self.assertEqual(self._connectivity_operations_instance._get_vlan_list("2, 3, 5-8, 7"), [2, 3, 5, 6, 7, 8])

    def test_get_vlan_list_exception_in_list(self):
        self.assertRaises(Exception, self._connectivity_operations_instance._get_vlan_list, "2, 3, 5000")

    def test_get_vlan_list_exception_in_range(self):
        self.assertRaises(Exception, self._connectivity_operations_instance._get_vlan_list, "2, 3999-4001")

    def test_does_interface_support_qnq_False(self):
        self._cli_service.send_config_command = Mock(side_effect=["", "Unrecognized command"])
        self.assertFalse(self._connectivity_operations_instance._does_interface_support_qnq("ethernet 2/1"))

    def test_does_interface_support_qnq_True(self):
        self._cli_service.send_config_command = Mock(side_effect=["", "enable "])
        self.assertTrue(self._connectivity_operations_instance._does_interface_support_qnq("ethernet 2/1"))

    def test_get_port_name_failed(self):
        self._connectivity_operations_instance._get_resource_full_name = Mock(return_value="")
        self.assertRaises(Exception, self._connectivity_operations_instance.get_port_name)

    def test_get_port_name_success(self):
        self._connectivity_operations_instance._get_resource_full_name = Mock(return_value="chassis/module/ethernet2-1")
        self.assertEqual("ethernet 2/1", self._connectivity_operations_instance.get_port_name("some port"))
