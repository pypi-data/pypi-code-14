# -*- coding: utf-8 -*-
"""
    stock.py

"""
from decimal import Decimal
import base64

from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

from fedex.services.rate_service import FedexRateServiceRequest
from fedex.services.ship_service import FedexProcessShipmentRequest
from fedex.base_service import FedexError

__all__ = ['ShipmentOut']
__metaclass__ = PoolMeta


class ShipmentOut:
    "Shipment Out"
    __name__ = 'stock.shipment.out'

    @classmethod
    def __setup__(cls):
        super(ShipmentOut, cls).__setup__()
        cls._error_messages.update({
            'error_label': 'Error in generating label: \n\n%s',
            'fedex_settings_missing':
                'Please select a Box Type and Carrier Service',
            'tracking_number_already_present':
                'Tracking Number is already present for this shipment.',
            'invalid_state': 'Labels can only be generated when the '
                'shipment is in Packed or Done states only',
            'fedex_shipping_cost_error':
                'Error while getting shipping cost from Fedex: \n\n%s'
        })

    def get_shipping_rate(self, carrier, carrier_service=None, silent=False):
        """
        Returns the calculated shipping cost as sent by fedex

        :returns: The shipping cost
        """
        Currency = Pool().get('currency.currency')
        Uom = Pool().get('product.uom')

        if carrier.carrier_cost_method != 'fedex':
            return super(ShipmentOut, self).get_shipping_rate(
                carrier, carrier_service, silent
            )

        fedex_credentials = self.carrier.get_fedex_credentials()

        rate_request = FedexRateServiceRequest(fedex_credentials)

        # TODO: DropOff Type should be configurable
        rate_request.RequestedShipment.DropoffType = "REGULAR_PICKUP"
        if carrier_service:
            rate_request.RequestedShipment.ServiceType = carrier_service.code
        rate_request.RequestedShipment.PackagingType = self.packages[0].box_type.code
        rate_request.RequestedShipment.RateRequestTypes = "PREFERRED"
        rate_request.RequestedShipment.PreferredCurrency = self.cost_currency.code

        # Shipper's address
        shipper_address = self._get_ship_from_address()
        rate_request.RequestedShipment.Shipper.Address.PostalCode = shipper_address.zip
        rate_request.RequestedShipment.Shipper.Address.CountryCode = shipper_address.country.code
        rate_request.RequestedShipment.Shipper.Address.Residential = False

        # Recipient address
        rate_request.RequestedShipment.Recipient.Address.PostalCode = self.delivery_address.zip
        rate_request.RequestedShipment.Recipient.Address.CountryCode = self.delivery_address.country.code

        # Include estimated duties and taxes in rate quote, can be ALL or NONE
        rate_request.RequestedShipment.EdtRequestType = 'NONE'

        # Who pays for the rate_request?
        # RECIPIENT, SENDER or THIRD_PARTY
        rate_request.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'

        for index, package in enumerate(self.packages, 1):
            uom_pound, = Uom.search([('symbol', '=', 'lb')])
            package_weight = rate_request.create_wsdl_object_of_type('Weight')
            package_weight.Value = float("%.2f" % Uom.compute_qty(package.weight_uom, package.weight, uom_pound))
            package_weight.Units = "LB"
            package = rate_request.create_wsdl_object_of_type('RequestedPackageLineItem')
            package.Weight = package_weight

            if self.shippo_insurance_cost:
                # Insured Value
                package_insure = rate_request.create_wsdl_object_of_type('Money')
                package_insure.Currency = self.cost_currency.code
                package_insure.Amount = self.shippo_insurance_cost

                # Add Insured and Total Insured values.
                package.InsuredValue = package_insure
                rate_request.RequestedShipment.TotalInsuredValue = package_insure

            # Can be other values this is probably the most common
            package.PhysicalPackaging = 'BOX'
            package.GroupPackageCount = index

            rate_request.add_package(package)

        try:
            rate_request.send_request()
        except FedexError, error:
            self.raise_user_error("fedex_shipping_cost_error", error_args=(error, ))

        rates = []
        for rate_detail in rate_request.response.RateReplyDetails:
            for service in carrier.services:
                if service.code == str(rate_detail.ServiceType):
                    break
            else:
                continue

            for rate_shipmemt in rate_detail.RatedShipmentDetails:
                if rate_shipmemt.ShipmentRateDetail.TotalNetFedExCharge.Currency != self.cost_currency.code:
                    continue

            rates.append({
                'display_name': self.carrier.rec_name,
                'carrier_service': service,
                'carrier': carrier,
                'cost_currency': Currency(self.cost_currency.id),
                'cost': self.carrier.currency.round(Decimal(rate_shipmemt.ShipmentRateDetail.TotalNetFedExCharge.Amount)),
            })

        return rates

    def generate_shipping_labels(self, **kwargs):
        """
        Make labels for the given shipment

        :return: Tracking number as string
        """
        Attachment = Pool().get('ir.attachment')
        Uom = Pool().get('product.uom')
        Tracking = Pool().get('shipment.tracking')
        Company = Pool().get('company.company')

        if self.carrier_cost_method != 'fedex':
            return super(ShipmentOut, self).generate_shipping_labels(**kwargs)

        if self.tracking_number:
            self.raise_user_error('tracking_number_already_present')

        fedex_credentials = self.carrier.get_fedex_credentials()

        ship_request = FedexProcessShipmentRequest(fedex_credentials)
        # TODO: DropOff Type should be configurable
        ship_request.RequestedShipment.DropoffType = "REGULAR_PICKUP"
        ship_request.RequestedShipment.ServiceType = self.carrier_service.code
        ship_request.RequestedShipment.PackagingType = self.packages[0].box_type.code

        company = Company(Transaction().context.get('company'))
        shipper_address = self._get_ship_from_address()

        # Shipper contact info.
        ship_request.RequestedShipment.Shipper.Contact.PersonName = shipper_address.name
        ship_request.RequestedShipment.Shipper.Contact.CompanyName = company.party.name
        ship_request.RequestedShipment.Shipper.Contact.PhoneNumber = shipper_address.party.phone

        # Shipper address.
        ship_request.RequestedShipment.Shipper.Address.StreetLines = [
            shipper_address.street or '', shipper_address.streetbis or ''
        ]
        ship_request.RequestedShipment.Shipper.Address.City = shipper_address.city
        ship_request.RequestedShipment.Shipper.Address.StateOrProvinceCode = shipper_address.subdivision.code[-2:]
        ship_request.RequestedShipment.Shipper.Address.PostalCode = shipper_address.zip
        ship_request.RequestedShipment.Shipper.Address.CountryCode = shipper_address.country.code
        ship_request.RequestedShipment.Shipper.Address.Residential = False

        # Recipient contact info.
        ship_request.RequestedShipment.Recipient.Contact.PersonName = self.customer.name
        ship_request.RequestedShipment.Recipient.Contact.PhoneNumber = self.delivery_address.phone or self.customer.phone

        # Recipient address
        ship_request.RequestedShipment.Recipient.Address.StreetLines = [
            self.delivery_address.street or '',
            self.delivery_address.streetbis or ''
        ]
        ship_request.RequestedShipment.Recipient.Address.City = self.delivery_address.city
        ship_request.RequestedShipment.Recipient.Address.StateOrProvinceCode = self.delivery_address.subdivision.code[-2:]
        ship_request.RequestedShipment.Recipient.Address.PostalCode = self.delivery_address.zip
        ship_request.RequestedShipment.Recipient.Address.CountryCode = self.delivery_address.country.code

        # Preferred currency
        ship_request.RequestedShipment.RateRequestTypes = "PREFERRED"
        ship_request.RequestedShipment.PreferredCurrency = self.cost_currency.code

        # This is needed to ensure an accurate rate quote with the response.
        ship_request.RequestedShipment.Recipient.Address.Residential = True
        ship_request.RequestedShipment.EdtRequestType = 'NONE'

        ship_request.RequestedShipment.ShippingChargesPayment.Payor.ResponsibleParty.AccountNumber = fedex_credentials.account_number
        ship_request.RequestedShipment.ShippingChargesPayment.Payor.ResponsibleParty.Contact = ship_request.RequestedShipment.Shipper.Contact

        ship_request.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'
        ship_request.RequestedShipment.LabelSpecification.LabelFormatType = 'COMMON2D'
        ship_request.RequestedShipment.LabelSpecification.ImageType = 'PNG'
        ship_request.RequestedShipment.LabelSpecification.LabelStockType = 'PAPER_4X6'
        ship_request.RequestedShipment.LabelSpecification.LabelPrintingOrientation = 'BOTTOM_EDGE_OF_TEXT_FIRST'

        if self.is_international_shipping:
            self._set_fedex_customs_details(ship_request)

        uom_pound, = Uom.search([('symbol', '=', 'lb')])

        master_tracking_number = None
        ship_request.RequestedShipment.PackageCount = len(self.packages)
        ship_request.RequestedShipment.TotalWeight.Units = 'LB'
        ship_request.RequestedShipment.TotalWeight.Value = float("%.2f" % Uom.compute_qty(
            self.weight_uom, self.weight, uom_pound
        ))

        for index, package in enumerate(self.packages, start=1):
            if master_tracking_number is not None:
                tracking_id = ship_request.create_wsdl_object_of_type(
                    'TrackingId'
                )
                tracking_id.TrackingNumber = master_tracking_number
                tracking_id.TrackingIdType = 'EXPRESS'
                ship_request.RequestedShipment.MasterTrackingId = tracking_id

            package_weight = ship_request.create_wsdl_object_of_type('Weight')
            package_weight.Value = float("%.2f" % Uom.compute_qty(
                package.weight_uom, package.weight, uom_pound
            ))
            package_weight.Units = "LB"

            package_item = ship_request.create_wsdl_object_of_type('RequestedPackageLineItem')
            package_item.PhysicalPackaging = 'BOX'
            package_item.Weight = package_weight
            package_item.SequenceNumber = index
            ship_request.RequestedShipment.RequestedPackageLineItems = [package_item]

            if self.shippo_insurance_cost:
                # Insured Value
                package_insure = ship_request.create_wsdl_object_of_type('Money')
                package_insure.Currency = self.cost_currency.code
                package_insure.Amount = self.shippo_insurance_cost

                # Add Insured and Total Insured values.
                package.InsuredValue = package_insure
                ship_request.RequestedShipment.TotalInsuredValue = package_insure

            try:
                ship_request.send_request()
            except FedexError, error:
                self.raise_user_error("error_label", error_args=(error, ))

            tracking_number = (ship_request.response.CompletedShipmentDetail.CompletedPackageDetails[0].TrackingIds[0].TrackingNumber).encode('utf-8')
            if index == 1:
                master_tracking_number = tracking_number

            # Create tracking numbers for package
            tracking, = Tracking.create([{
                'carrier': self.carrier,
                'tracking_number': tracking_number,
                'origin': '%s,%d' % (package.__name__, package.id),
            }])

            for id, image in enumerate(ship_request.response.CompletedShipmentDetail.CompletedPackageDetails[0].Label.Parts):
                Attachment.create([{
                    'name': "%s_%s_Fedex.png" % (tracking_number, id),
                    'type': 'data',
                    'data': buffer(base64.decodestring(image.Image)),
                    'resource': '%s,%s' % (tracking.__name__, tracking.id)
                }])

        for rate_detail in ship_request.response.CompletedShipmentDetail.ShipmentRating.ShipmentRateDetails:
            if rate_detail.TotalNetFedExCharge.Currency != self.cost_currency.code:
                continue
            self.cost = self.carrier.currency.round(Decimal(str(rate_detail.TotalNetFedExCharge.Amount)))
            self.save()

        # Save master tracking number on shipment
        shipment_tracking_number, = Tracking.search([
            ('tracking_number', '=', master_tracking_number),
        ])
        self.tracking_number = shipment_tracking_number
        self.save()

        return master_tracking_number

    def _set_fedex_customs_details(self, ship_request):
        """
        Computes the details of the customs items and passes to fedex request
        """
        ProductUom = Pool().get('product.uom')

        customs_detail = ship_request.create_wsdl_object_of_type(
            'CustomsClearanceDetail'
        )
        customs_detail.DocumentContent = 'NON_DOCUMENTS'
        customs_detail.__delattr__('FreightOnValue')
        customs_detail.__delattr__('ClearanceBrokerage')

        weight_uom, = ProductUom.search([('symbol', '=', 'lb')])

        from_address = self._get_ship_from_address()

        # Encoding Items for customs
        commodities = []
        customs_value = 0
        for move in self.outgoing_moves:
            if move.product.type == 'service':
                continue
            commodity = ship_request.create_wsdl_object_of_type('Commodity')
            commodity.NumberOfPieces = len(self.outgoing_moves)
            commodity.Name = move.product.name
            commodity.Description = move.product.description or \
                move.product.name
            commodity.CountryOfManufacture = from_address.country.code
            commodity.Weight.Units = 'LB'
            commodity.Weight.Value = float("%.2f" % move.get_weight(weight_uom))
            commodity.Quantity = int(move.quantity)
            commodity.QuantityUnits = 'EA'
            commodity.UnitPrice.Amount = move.product.customs_value_used.quantize(Decimal('.01'))
            commodity.UnitPrice.Currency = self.company.currency.code
            commodity.CustomsValue.Currency = self.company.currency.code
            commodity.CustomsValue.Amount = (Decimal(str(move.quantity)) * move.product.customs_value_used).quantize(Decimal('.01'))
            commodities.append(commodity)
            customs_value += Decimal(str(move.quantity)) * move.product.customs_value_used

        customs_detail.CustomsValue.Currency = self.company.currency.code
        customs_detail.CustomsValue.Amount = customs_value.quantize(Decimal('.01'))
        customs_detail.Commodities = commodities

        # Commercial Invoice
        customs_detail.CommercialInvoice.TaxesOrMiscellaneousChargeType = 'OTHER'
        customs_detail.CommercialInvoice.Purpose = "SOLD"
        customs_detail.CommercialInvoice.TermsOfSale = 'DDU'
        customs_detail.DutiesPayment.PaymentType = 'SENDER'
        customs_detail.DutiesPayment.Payor = ship_request.RequestedShipment.ShippingChargesPayment.Payor

        ship_request.RequestedShipment.CustomsClearanceDetail = customs_detail
