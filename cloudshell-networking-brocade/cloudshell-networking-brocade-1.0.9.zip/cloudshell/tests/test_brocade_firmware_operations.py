#!/usr/bin/python
# -*- coding: utf-8 -*-

from mock import MagicMock as Mock
from unittest import TestCase

from cloudshell.networking.brocade.brocade_firmware_operations import BrocadeFirmwareOperations


class TestFirmwareOperationsInterface(TestCase):
    def setUp(self):
        self._context = Mock()
        self._api = Mock()
        self._cli_service = Mock()
        self._logger = Mock()
        self._config = Mock()
        self._firmware_operations_instance = BrocadeFirmwareOperations(context=self._context,
                                                                       api=self._api,
                                                                       cli_service=self._cli_service,
                                                                       logger=self._logger
                                                                       )

    def test_load_firmware_copy_image_failed(self):
        self._cli_service.send_command = Mock(return_value="")
        self.assertRaises(Exception,
                          self._firmware_operations_instance.load_firmware,
                          "some wrong path to image")
