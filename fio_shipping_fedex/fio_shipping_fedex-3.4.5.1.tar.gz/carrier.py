# -*- coding: utf-8 -*-
"""
    carrier.py

"""
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Eval
from fedex.config import FedexConfig


REQUIRED_IF_FEDEX = {
    'required': Eval('carrier_cost_method') == 'fedex',
}

__all__ = ['Carrier', 'CarrierService', 'BoxType']
__metaclass__ = PoolMeta


class Carrier:
    "Carrier"
    __name__ = 'carrier'

    fedex_key = fields.Char('Key', states=REQUIRED_IF_FEDEX)
    fedex_password = fields.Char('Password', states=REQUIRED_IF_FEDEX)
    fedex_account_number = fields.Char(
        'Account Number', states=REQUIRED_IF_FEDEX
    )
    fedex_meter_number = fields.Char('Meter Number', states=REQUIRED_IF_FEDEX)
    fedex_is_test = fields.Boolean('Is Test Account?')

    @classmethod
    def __setup__(cls):
        super(Carrier, cls).__setup__()

        selection = ('fedex', 'FedEx (Direct)')
        if selection not in cls.carrier_cost_method.selection:
            cls.carrier_cost_method.selection.append(selection)

        cls._error_messages.update({
            'fedex_settings_missing': 'FedEx settings are incomplete',
        })

    def get_fedex_credentials(self):
        """
        Returns the fedex account credentials in tuple
        :return: FedexConfig object
        """
        if not all([
            self.fedex_key, self.fedex_account_number,
            self.fedex_password, self.fedex_meter_number,
        ]):
            self.raise_user_error('fedex_settings_missing')

        return FedexConfig(
            key=self.fedex_key,
            password=self.fedex_password,
            account_number=self.fedex_account_number,
            meter_number=self.fedex_meter_number,
            use_test_server=self.fedex_is_test
        )


class CarrierService:
    __name__ = 'carrier.service'

    @classmethod
    def __setup__(cls):
        super(CarrierService, cls).__setup__()

        selection = ('fedex', 'FedEx (Direct)')
        if selection not in cls.carrier_cost_method.selection:
            cls.carrier_cost_method.selection.append(selection)


class BoxType:
    __name__ = "carrier.box_type"

    @classmethod
    def __setup__(cls):
        super(BoxType, cls).__setup__()

        selection = ('fedex', 'FedEx (Direct)')
        if selection not in cls.carrier_cost_method.selection:
            cls.carrier_cost_method.selection.append(selection)
