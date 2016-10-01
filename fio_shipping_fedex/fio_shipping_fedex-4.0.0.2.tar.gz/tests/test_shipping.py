# -*- coding: utf-8 -*-
"""
    tests/test_shipping.py

"""
from decimal import Decimal
from pprint import pprint

from trytond.transaction import Transaction
from trytond.pool import Pool


class TestShipping:

    def test_get_shipping_rate_sale(
        self, manual_channel, usd, john_doe, fedex_carrier,
        company, payment_term_advance, product_1, uom_unit
    ):
        """
        Get shipping rates for sale with one carrier
        """
        Sale = Pool().get('sale.sale')

        sale, = Sale.create([{
            'party': john_doe.id,
            'invoice_address': john_doe.addresses[0].id,
            'shipment_address': john_doe.addresses[0].id,
            'company': company.id,
            'currency': usd.id,
            'carrier': fedex_carrier.id,
            'channel': manual_channel.id,
            'payment_term': payment_term_advance.id,
            'lines': [('create', [{
                'type': 'line',
                'quantity': 1,
                'product': product_1.id,
                'unit_price': Decimal('119.00'),
                'description': 'KindleFire',
                'unit': uom_unit.id,
                'delivery_mode': 'ship',
            }])]
        }])

        rates = Sale.get_shipping_rate(sale, fedex_carrier)
        pprint(rates)

        assert len(rates) > 0

    def test_fedex_labels_single_package(
        self, john_doe, company, usd, fedex_carrier,
        payment_term_advance, product_1, uom_unit, manual_channel
    ):
        """
        Generate fedex label if there is single package.
        """
        ModelData = Pool().get('ir.model.data')
        Sale = Pool().get('sale.sale')
        Attachment = Pool().get('ir.attachment')
        GenerateLabel = Pool().get('shipping.label', type="wizard")

        sale, = Sale.create([{
            'party': john_doe.id,
            'invoice_address': john_doe.addresses[0].id,
            'shipment_address': john_doe.addresses[0].id,
            'company': company.id,
            'currency': usd.id,
            'carrier': fedex_carrier.id,
            'channel': manual_channel.id,
            'payment_term': payment_term_advance.id,
            'lines': [('create', [{
                'type': 'line',
                'quantity': 1,
                'product': product_1.id,
                'unit_price': Decimal('119.00'),
                'description': 'KindleFire',
                'unit': uom_unit.id,
                'delivery_mode': 'ship',
            }])]
        }])

        # Quote, confirm and process
        Sale.quote([sale])
        Sale.confirm([sale])
        Sale.process([sale])

        shipment, = sale.shipments

        # Assign, pack and generate labels.
        shipment.assign([shipment])
        shipment.pack([shipment])

        assert shipment.cost == Decimal('0')

        # There are no label generated yet
        assert Attachment.search([], count=True) == 0

        with Transaction().set_context(
            active_model="stock.shipment.out", active_id=shipment.id
        ):
            # Call method to generate labels.
            session_id, start_state, _ = GenerateLabel.create()

            generate_label = GenerateLabel(session_id)

            generate_label.start.shipment = shipment.id
            generate_label.start.override_weight = Decimal('0')
            generate_label.start.carrier = fedex_carrier.id
            generate_label.start.carrier_service = \
                ModelData.get_id('shipping_fedex', 'service_fedex_2_day')
            generate_label.start.box_type = \
                ModelData.get_id('shipping_fedex', 'packaging_fedex_box')

            generate_label.transition_next()
            # Add rates
            generate_label.select_rate.rate = \
                generate_label.select_rate.__class__.rate.selection[0][0]

            # Generate label
            generate_label.transition_generate_labels()

        package, = shipment.packages

        assert package.tracking_number == shipment.tracking_number
        assert Attachment.search([], count=True) == 1
        assert shipment.cost > Decimal('0')

    def test_fedex_labels_multiple_package(
        self, company, product_1, product_2, uom_unit, usd,
        payment_term_advance, fedex_carrier, manual_channel,
        john_doe
    ):
        """
        Generate fedex label if there are multiple packages.
        """
        Sale = Pool().get('sale.sale')
        Attachment = Pool().get('ir.attachment')
        Package = Pool().get('stock.package')
        ModelData = Pool().get('ir.model.data')
        GenerateLabel = Pool().get('shipping.label', type="wizard")

        sale, = Sale.create([{
            'party': john_doe.id,
            'invoice_address': john_doe.addresses[0].id,
            'shipment_address': john_doe.addresses[0].id,
            'company': company.id,
            'currency': usd.id,
            'carrier': fedex_carrier.id,
            'channel': manual_channel.id,
            'payment_term': payment_term_advance.id,
            'lines': [('create', [{
                'type': 'line',
                'quantity': 1,
                'product': product_1.id,
                'unit_price': Decimal('119.00'),
                'description': 'KindleFire',
                'unit': uom_unit.id,
                'delivery_mode': 'ship',
            }, {
                'type': 'line',
                'quantity': 2,
                'product': product_2.id,
                'unit_price': Decimal('219.00'),
                'description': 'KindleFire HD',
                'unit': uom_unit.id,
                'delivery_mode': 'ship',
            }])]
        }])

        # Quote, confirm and process
        Sale.quote([sale])
        Sale.confirm([sale])
        Sale.process([sale])

        shipment, = sale.shipments

        type_id = ModelData.get_id(
            "shipping", "shipment_package_type"
        )
        package1, package2 = Package.create([{
            'shipment': '%s,%d' % (shipment.__name__, shipment.id),
            'type': type_id,
            'moves': [('add', [shipment.outgoing_moves[0]])],
        }, {
            'shipment': '%s,%d' % (shipment.__name__, shipment.id),
            'type': type_id,
            'moves': [('add', [shipment.outgoing_moves[1]])],
        }])

        # Assign, pack and generate labels.
        shipment.assign([shipment])
        shipment.pack([shipment])

        assert shipment.cost == Decimal('0')

        # There are no label generated yet
        assert Attachment.search([], count=True) == 0

        with Transaction().set_context(
            active_model="stock.shipment.out", active_id=shipment.id
        ):
            # Call method to generate labels.
            session_id, start_state, _ = GenerateLabel.create()

            generate_label = GenerateLabel(session_id)
            generate_label.start.shipment = shipment.id
            generate_label.start.override_weight = Decimal('0')
            generate_label.start.carrier = fedex_carrier.id
            generate_label.start.carrier_service = \
                ModelData.get_id('shipping_fedex', 'service_fedex_2_day')
            generate_label.start.box_type = \
                ModelData.get_id('shipping_fedex', 'packaging_fedex_box')

            generate_label.transition_next()
            # Add rates
            generate_label.select_rate.rate = \
                generate_label.select_rate.__class__.rate.selection[0][0]

            # Generate label
            generate_label.transition_generate_labels()

        assert package1.tracking_number is not None
        assert package2.tracking_number is not None
        assert shipment.tracking_number is not None
        assert Attachment.search([], count=True) == 2
        assert shipment.cost > Decimal('0')

    def test_fedex_labels_single_package_international(
        self, company, usd, uom_unit, payment_term_advance,
        product_1, india, in_kl, fedex_carrier, john_doe,
        manual_channel
    ):
        """
        Generate fedex label if there is single package.
        """
        Sale = Pool().get('sale.sale')
        Attachment = Pool().get('ir.attachment')
        Address = Pool().get('party.address')
        GenerateLabel = Pool().get('shipping.label', type="wizard")
        ModelData = Pool().get('ir.model.data')

        # save customs value in product
        product_1.customs_value = Decimal('2')
        product_1.save()

        sale, = Sale.create([{
            'party': john_doe.id,
            'invoice_address': john_doe.addresses[0].id,
            'shipment_address': john_doe.addresses[0].id,
            'company': company.id,
            'currency': usd.id,
            'carrier': fedex_carrier.id,
            'channel': manual_channel.id,
            'payment_term': payment_term_advance.id,
            'lines': [('create', [{
                'type': 'line',
                'quantity': 1,
                'product': product_1.id,
                'unit_price': Decimal('119.00'),
                'description': 'KindleFire',
                'unit': uom_unit.id,
                'delivery_mode': 'ship',
            }])]
        }])

        new_warehouse_address = Address(
            party=company.party.id,
            name="Prakash Pandey",
            street="No. 6/50G",
            streetbis="Shanti Path, Chanakyapuri",
            city="Kochi",
            zip="682021",
            country=india.id,
            subdivision=in_kl.id,
        )
        new_warehouse_address.save()
        sale.warehouse.address = new_warehouse_address
        sale.warehouse.save()

        # Quote, confirm and process
        Sale.quote([sale])
        Sale.confirm([sale])
        Sale.process([sale])

        shipment, = sale.shipments

        # Assign, pack and generate labels.
        shipment.assign([shipment])
        shipment.pack([shipment])

        assert shipment.cost == Decimal('0')

        # There are no label generated yet
        assert Attachment.search([], count=True) == 0

        with Transaction().set_context(
            active_model="stock.shipment.out", active_id=shipment.id
        ):
            # Call method to generate labels.
            session_id, start_state, _ = GenerateLabel.create()

            generate_label = GenerateLabel(session_id)
            generate_label.start.shipment = shipment.id
            generate_label.start.override_weight = Decimal('0')
            generate_label.start.carrier = fedex_carrier.id
            generate_label.start.carrier_service = \
                ModelData.get_id('shipping_fedex', 'service_international_economy')
            generate_label.start.box_type = \
                ModelData.get_id('shipping_fedex', 'packaging_fedex_your')

            generate_label.transition_next()
            # Add rates
            generate_label.select_rate.rate = \
                generate_label.select_rate.__class__.rate.selection[0][0]

            # Generate label
            generate_label.transition_generate_labels()

        package, = shipment.packages

        assert package.tracking_number == shipment.tracking_number
        assert Attachment.search([], count=True) == 1
        assert shipment.cost > Decimal('0')

    def test_fedex_labels_multiple_package_international(
        self, company, usd, payment_term_advance, product_1, john_doe,
        product_2, fedex_carrier, india, in_kl, uom_unit, manual_channel
    ):
        """
        Generate fedex label if there are multiple packages.
        """
        Sale = Pool().get('sale.sale')
        Attachment = Pool().get('ir.attachment')
        Package = Pool().get('stock.package')
        ModelData = Pool().get('ir.model.data')
        Address = Pool().get('party.address')
        GenerateLabel = Pool().get('shipping.label', type="wizard")
        ModelData = Pool().get('ir.model.data')

        # save customs value in product
        product_1.customs_value = Decimal('1')
        product_1.save()
        product_2.customs_value = Decimal('2')
        product_2.save()

        sale, = Sale.create([{
            'party': john_doe.id,
            'invoice_address': john_doe.addresses[0].id,
            'shipment_address': john_doe.addresses[0].id,
            'company': company.id,
            'currency': usd.id,
            'carrier': fedex_carrier.id,
            'channel': manual_channel.id,
            'payment_term': payment_term_advance.id,
            'lines': [('create', [{
                'type': 'line',
                'quantity': 1,
                'product': product_1.id,
                'unit_price': Decimal('119.00'),
                'description': 'KindleFire',
                'unit': uom_unit.id,
                'delivery_mode': 'ship',
            }, {
                'type': 'line',
                'quantity': 2,
                'product': product_2.id,
                'unit_price': Decimal('219.00'),
                'description': 'KindleFire HD',
                'unit': uom_unit.id,
                'delivery_mode': 'ship',
            }])]
        }])

        new_warehouse_address = Address(
            party=company.party.id,
            name="Prakash Pandey",
            street="No. 6/50G",
            streetbis="Shanti Path, Chanakyapuri",
            city="Kochi",
            zip="682021",
            country=india.id,
            subdivision=in_kl.id,
        )
        new_warehouse_address.save()
        sale.warehouse.address = new_warehouse_address
        sale.warehouse.save()

        # Quote, confirm and process
        Sale.quote([sale])
        Sale.confirm([sale])
        Sale.process([sale])

        shipment, = sale.shipments

        type_id = ModelData.get_id(
            "shipping", "shipment_package_type"
        )
        package1, package2 = Package.create([{
            'shipment': '%s,%d' % (shipment.__name__, shipment.id),
            'type': type_id,
            'moves': [('add', [shipment.outgoing_moves[0]])],
        }, {
            'shipment': '%s,%d' % (shipment.__name__, shipment.id),
            'type': type_id,
            'moves': [('add', [shipment.outgoing_moves[1]])],
        }])

        # Assign, pack and generate labels.
        shipment.assign([shipment])
        shipment.pack([shipment])

        assert shipment.cost == Decimal('0')

        # There are no label generated yet
        assert Attachment.search([], count=True) == 0

        with Transaction().set_context(
            active_model="stock.shipment.out", active_id=shipment.id
        ):
            # Call method to generate labels.
            session_id, start_state, _ = GenerateLabel.create()

            generate_label = GenerateLabel(session_id)
            generate_label.start.shipment = shipment.id
            generate_label.start.override_weight = Decimal('0')
            generate_label.start.carrier = fedex_carrier.id
            generate_label.start.carrier_service = \
                ModelData.get_id('shipping_fedex', 'service_international_priority')
            generate_label.start.box_type = \
                ModelData.get_id('shipping_fedex', 'packaging_fedex_box')

            generate_label.transition_next()
            # Add rates
            generate_label.select_rate.rate = \
                generate_label.select_rate.__class__.rate.selection[0][0]

            # Generate label
            generate_label.transition_generate_labels()

        assert package1.tracking_number is not None
        assert package2.tracking_number is not None
        assert shipment.tracking_number is not None
        assert Attachment.search([], count=True) == 2
        assert shipment.cost > Decimal('0')
