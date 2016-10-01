# -*- coding: utf-8 -*-
"""
    sale.py

"""
from decimal import Decimal

from trytond.model import fields
from trytond.pool import PoolMeta, Pool

from fedex.services.rate_service import FedexRateServiceRequest
from fedex.base_service import FedexError

__all__ = ['Sale']
__metaclass__ = PoolMeta


class Configuration:
    'Sale Configuration'
    __name__ = 'sale.configuration'

    fedex_box_type = fields.Many2One(
        'carrier.box_type', 'Box Type',
        domain=[('carrier_cost_method', '=', 'fedex')],
    )
    fedex_carrier_service = fields.Many2One(
        'carrier.service', 'Carrier Service',
        domain=[('carrier_cost_method', '=', 'fedex')],
    )


class Sale:
    "Sale"
    __name__ = 'sale.sale'

    is_fedex_shipping = fields.Function(
        fields.Boolean('Is Fedex Shipping'),
        'get_is_fedex_shipping',
    )

    def get_is_fedex_shipping(self, name):
        return self.carrier and \
            self.carrier.carrier_cost_method == 'fedex' or False

    @classmethod
    def __setup__(self):
        super(Sale, self).__setup__()
        self._error_messages.update({
            'fedex_settings_missing': 'FedEx settings are missing on Sale Configuration',
            'fedex_rates_error':
                "Error while getting rates from Fedex: \n\n%s"
        })

    def on_change_carrier(self):
        """
        Show/Hide UPS Tab in view on change of carrier
        """
        super(Sale, self).on_change_carrier()

        if self.carrier and self.carrier.carrier_cost_method == 'fedex':
            self.is_fedex_shipping = True

    def get_shipping_rate(self, carrier, carrier_service=None, silent=False):
        """
        Returns the calculated shipping cost as sent by fedex

        :returns: The shipping cost
        """
        Config = Pool().get('sale.configuration')
        Currency = Pool().get('currency.currency')
        Uom = Pool().get('product.uom')

        if carrier.carrier_cost_method != 'fedex':
            return super(Sale, self).get_shipping_rate(
                carrier, carrier_service, silent
            )

        fedex_credentials = self.carrier.get_fedex_credentials()
        config = Config(1)

        carrier_service = carrier_service or config.fedex_carrier_service
        if not (config.fedex_box_type and carrier_service):
            self.raise_user_error('fedex_settings_missing')

        rate_request = FedexRateServiceRequest(fedex_credentials)
        # TODO: DropOff Type should be configurable
        rate_request.RequestedShipment.DropoffType = "REGULAR_PICKUP"
        rate_request.RequestedShipment.ServiceType = carrier_service.code
        rate_request.RequestedShipment.PackagingType = config.fedex_box_type.code
        rate_request.RequestedShipment.RateRequestTypes = "PREFERRED"
        rate_request.RequestedShipment.PreferredCurrency = self.currency.code

        # Shipper's address
        shipper_address = self._get_ship_from_address()
        rate_request.RequestedShipment.Shipper.Address.PostalCode = shipper_address.zip
        rate_request.RequestedShipment.Shipper.Address.CountryCode = shipper_address.country.code
        rate_request.RequestedShipment.Shipper.Address.Residential = False

        # Recipient address
        rate_request.RequestedShipment.Recipient.Address.PostalCode = self.shipment_address.zip
        rate_request.RequestedShipment.Recipient.Address.CountryCode = self.shipment_address.country.code

        # Include estimated duties and taxes in rate quote, can be ALL or NONE
        rate_request.RequestedShipment.EdtRequestType = 'NONE'

        # Who pays for the rate_request?
        # RECIPIENT, SENDER or THIRD_PARTY
        rate_request.RequestedShipment.ShippingChargesPayment.PaymentType = \
            'SENDER'

        uom_pound, = Uom.search([('symbol', '=', 'lb')])
        package_weight = rate_request.create_wsdl_object_of_type('Weight')
        package_weight.Value = float("%.2f" % Uom.compute_qty(self.weight_uom, self.weight, uom_pound))
        package_weight.Units = "LB"
        package = rate_request.create_wsdl_object_of_type('RequestedPackageLineItem')
        package.Weight = package_weight
        # Can be other values this is probably the most common
        package.PhysicalPackaging = 'BOX'
        package.GroupPackageCount = 1

        rate_request.add_package(package)

        try:
            rate_request.send_request()
        except FedexError, error:
            self.raise_user_error("fedex_rates_error", error_args=(error, ))

        rates = []
        for rate_detail in rate_request.response.RateReplyDetails[0].RatedShipmentDetails:
            if rate_detail.ShipmentRateDetail.TotalNetFedExCharge.Currency != self.currency.code:
                continue
            rates.append({
                'display_name': self.carrier.rec_name,
                'carrier_service': carrier_service,
                'carrier': carrier,
                'cost_currency': Currency(self.currency.id),
                'cost': self.currency.round(Decimal(rate_detail.ShipmentRateDetail.TotalNetFedExCharge.Amount)),
            })

        return rates
