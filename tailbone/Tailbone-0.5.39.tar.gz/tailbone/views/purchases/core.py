# -*- coding: utf-8 -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2016 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
#  more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Views for "true" purchase orders
"""

from __future__ import unicode_literals, absolute_import

from rattail import enum
from rattail.db import model

import formalchemy as fa

from tailbone import forms
from tailbone.db import Session
from tailbone.views import MasterView


class PurchaseView(MasterView):
    """
    Master view for purchase orders.
    """
    model_class = model.Purchase
    creatable = False
    editable = False

    has_rows = True
    model_row_class = model.PurchaseItem
    row_model_title = 'Purchase Item'

    def _preconfigure_grid(self, g):
        g.joiners['store'] = lambda q: q.join(model.Store)
        g.filters['store'] = g.make_filter('store', model.Store.name)
        g.sorters['store'] = g.make_sorter(model.Store.name)

        g.joiners['vendor'] = lambda q: q.join(model.Vendor)
        g.filters['vendor'] = g.make_filter('vendor', model.Vendor.name,
                                            default_active=True, default_verb='contains')
        g.sorters['vendor'] = g.make_sorter(model.Vendor.name)

        g.joiners['buyer'] = lambda q: q.join(model.Employee).join(model.Person)
        g.filters['buyer'] = g.make_filter('buyer', model.Person.display_name,
                                           default_active=True, default_verb='contains')
        g.sorters['buyer'] = g.make_sorter(model.Person.display_name)

        g.filters['date_ordered'].label = "Ordered"
        g.filters['date_ordered'].default_active = True
        g.filters['date_ordered'].default_verb = 'equal'

        g.default_sortkey = 'date_ordered'
        g.default_sortdir = 'desc'

        g.date_ordered.set(label="Ordered")
        g.status.set(renderer=forms.renderers.EnumFieldRenderer(enum.PURCHASE_STATUS))

    def configure_grid(self, g):
        g.configure(
            include=[
                g.store,
                g.vendor,
                g.buyer,
                g.date_ordered,
                g.status,
            ],
            readonly=True)

    def _preconfigure_fieldset(self, fs):
        fs.vendor.set(renderer=forms.renderers.VendorFieldRenderer)
        fs.status.set(renderer=forms.renderers.EnumFieldRenderer(enum.PURCHASE_STATUS),
                      readonly=True)
        fs.po_number.set(label="PO Number")
        fs.po_total.set(label="PO Total")

    def configure_fieldset(self, fs):
        fs.configure(
            include=[
                fs.store,
                fs.vendor,
                fs.buyer,
                fs.date_ordered,
                fs.po_number,
                fs.po_total,
                fs.status,
                fs.created,
                fs.created_by,
            ])

    def get_parent(self, item):
        return item.purchase

    def get_row_data(self, purchase):
        return Session.query(model.PurchaseItem)\
                      .filter(model.PurchaseItem.purchase == purchase)

    def _preconfigure_row_grid(self, g):
        g.default_sortkey = 'sequence'
        g.sequence.set(label="Seq")
        g.upc.set(label="UPC")
        g.brand_name.set(label="Brand")
        g.cases_ordered.set(label="Cases")
        g.units_ordered.set(label="Units")
        g.po_total.set(label="PO Total")

    def configure_row_grid(self, g):
        g.configure(
            include=[
                g.sequence,
                g.upc,
                g.brand_name,
                g.description,
                g.size,
                g.cases_ordered,
                g.units_ordered,
                g.po_total,
            ],
            readonly=True)

    def _preconfigure_row_fieldset(self, fs):
        fs.vendor_code.set(label="Vendor Item Code")
        fs.upc.set(label="UPC")
        fs.po_unit_cost.set(label="PO Unit Cost")
        fs.po_total.set(label="PO Total")
        fs.append(fa.Field('department', value=lambda i: '{} {}'.format(i.department_number, i.department_name)))

    def configure_row_fieldset(self, fs):

        fs.configure(
            include=[
                fs.sequence,
                fs.vendor_code,
                fs.upc,
                fs.product,
                fs.department,
                fs.case_quantity,
                fs.cases_ordered,
                fs.units_ordered,
                fs.po_unit_cost,
                fs.po_total,
            ])


def includeme(config):
    PurchaseView.defaults(config)
