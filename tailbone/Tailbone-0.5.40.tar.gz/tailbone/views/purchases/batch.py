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
Views for purchase order batches
"""

from __future__ import unicode_literals, absolute_import

from sqlalchemy import orm

from rattail import enum
from rattail.db import model, api
from rattail.gpc import GPC
from rattail.time import localtime
from rattail.core import Object
from rattail.util import OrderedDict

import formalchemy as fa

from tailbone import forms
from tailbone.db import Session
from tailbone.views.batch import BatchMasterView


class PurchaseBatchView(BatchMasterView):
    """
    Master view for purchase order batches.
    """
    model_class = model.PurchaseBatch
    model_title_plural = "Purchase Batches"
    model_row_class = model.PurchaseBatchRow
    default_handler_spec = 'rattail.batch.purchase:PurchaseBatchHandler'
    route_prefix = 'purchases.batch'
    url_prefix = '/purchases/batches'
    rows_creatable = True
    rows_editable = True
    edit_with_rows = False

    def _preconfigure_grid(self, g):
        super(PurchaseBatchView, self)._preconfigure_grid(g)

        g.joiners['vendor'] = lambda q: q.join(model.Vendor)
        g.filters['vendor'] = g.make_filter('vendor', model.Vendor.name,
                                            default_active=True, default_verb='contains')
        g.sorters['vendor'] = g.make_sorter(model.Vendor.name)

        g.joiners['buyer'] = lambda q: q.join(model.Employee).join(model.Person)
        g.filters['buyer'] = g.make_filter('buyer', model.Person.display_name,
                                           default_active=True, default_verb='contains')
        g.sorters['buyer'] = g.make_sorter(model.Person.display_name)

        if self.request.has_perm('purchases.batch.execute'):
            g.filters['complete'].default_active = True
            g.filters['complete'].default_verb = 'is_true'

        g.date_ordered.set(label="Ordered")

    def configure_grid(self, g):
        g.configure(
            include=[
                g.id,
                g.vendor,
                g.buyer,
                g.date_ordered,
                g.created,
                g.created_by,
                g.executed,
            ],
            readonly=True)

    def _preconfigure_fieldset(self, fs):
        super(PurchaseBatchView, self)._preconfigure_fieldset(fs)
        fs.vendor.set(renderer=forms.renderers.VendorFieldRenderer)
        fs.buyer.set(renderer=forms.renderers.EmployeeFieldRenderer)
        fs.po_number.set(label="PO Number")
        fs.po_total.set(label="PO Total", readonly=True)

        fs.append(fa.Field('vendor_email', readonly=True,
                           value=lambda b: b.vendor.email.address if b.vendor.email else None))
        fs.append(fa.Field('vendor_fax', readonly=True,
                           value=self.get_vendor_fax_number))
        fs.append(fa.Field('vendor_contact', readonly=True,
                           value=lambda b: b.vendor.contact or None))
        fs.append(fa.Field('vendor_phone', readonly=True,
                           value=self.get_vendor_phone_number))

    def get_vendor_phone_number(self, batch):
        for phone in batch.vendor.phones:
            if phone.type == 'Voice':
                return phone.number

    def get_vendor_fax_number(self, batch):
        for phone in batch.vendor.phones:
            if phone.type == 'Fax':
                return phone.number

    def configure_fieldset(self, fs):
        fs.configure(
            include=[
                fs.id,
                fs.store,
                fs.vendor,
                fs.vendor_email,
                fs.vendor_fax,
                fs.vendor_contact,
                fs.vendor_phone,
                fs.buyer,
                fs.date_ordered,
                fs.po_number,
                fs.po_total,
                fs.created,
                fs.created_by,
                fs.complete,
                fs.executed,
                fs.executed_by,
            ])

        if self.creating:
            del fs.po_total
            del fs.complete
            del fs.vendor_email
            del fs.vendor_fax
            del fs.vendor_phone
            del fs.vendor_contact

            # default store may be configured
            store = self.rattail_config.get('rattail', 'store')
            if store:
                store = api.get_store(Session(), store)
                if store:
                    fs.model.store = store

            # default buyer is current user
            if self.request.method != 'POST':
                buyer = self.request.user.employee
                if buyer:
                    fs.model.buyer = buyer

            # default order date is today
            fs.model.date_ordered = localtime(self.rattail_config).date()

        elif self.editing:
            fs.store.set(readonly=True)
            fs.vendor.set(readonly=True)

    def template_kwargs_view(self, **kwargs):
        kwargs = super(PurchaseBatchView, self).template_kwargs_view(**kwargs)
        vendor = kwargs['batch'].vendor
        kwargs['vendor_cost_count'] = Session.query(model.ProductCost)\
                                             .filter(model.ProductCost.vendor == vendor)\
                                             .count()
        kwargs['vendor_cost_threshold'] = self.rattail_config.getint(
            'tailbone', 'purchases.order_form.vendor_cost_warning_threshold', default=699)
        return kwargs

    def _preconfigure_row_grid(self, g):
        super(PurchaseBatchView, self)._preconfigure_row_grid(g)

        g.filters['upc'].label = "UPC"
        g.filters['brand_name'].label = "Brand"

        g.upc.set(label="UPC")
        g.brand_name.set(label="Brand")
        g.cases_ordered.set(label="Cases")
        g.units_ordered.set(label="Units")
        g.po_total.set(label="Total")

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
                g.status_code,
            ],
            readonly=True)

    def make_row_grid_tools(self, batch):
        return self.make_default_row_grid_tools(batch)

#     def row_grid_row_attrs(self, row, i):
#         attrs = {}
#         if row.status_code in (row.STATUS_NOT_IN_PURCHASE,
#                                row.STATUS_NOT_IN_INVOICE,
#                                row.STATUS_DIFFERS_FROM_PURCHASE):
#             attrs['class_'] = 'notice'
#         if row.status_code in (row.STATUS_NOT_IN_DB,
#                                row.STATUS_COST_NOT_IN_DB,
#                                row.STATUS_NO_CASE_QUANTITY):
#             attrs['class_'] = 'warning'
#         return attrs

    def _preconfigure_row_fieldset(self, fs):
        super(PurchaseBatchView, self)._preconfigure_row_fieldset(fs)
        fs.upc.set(label="UPC")
        fs.brand_name.set(label="Brand")
        fs.po_unit_cost.set(label="PO Unit Cost")
        fs.po_total.set(label="PO Total")
        fs.append(fa.Field('item_lookup', label="Item Lookup Code", required=True,
                           validate=self.item_lookup))

    def item_lookup(self, value, field=None):
        """
        Try to locate a single product using ``value`` as a lookup code.
        """
        batch = self.get_instance()
        product = api.get_product_by_vendor_code(Session(), value, vendor=batch.vendor)
        if product:
            return product.uuid
        if value.isdigit():
            product = api.get_product_by_upc(Session(), GPC(value))
            if not product:
                product = api.get_product_by_upc(Session(), GPC(value, calc_check_digit='upc'))
            if product:
                if not product.cost_for_vendor(batch.vendor):
                    raise fa.ValidationError("Product {} exists but has no cost for vendor {}".format(
                        product.upc.pretty(), batch.vendor))
                return product.uuid
        raise fa.ValidationError("Product not found")

    def configure_row_fieldset(self, fs):

        if self.creating:
            fs.configure(
                include=[
                    fs.item_lookup,
                    fs.cases_ordered,
                    fs.units_ordered,
                ])

        elif self.editing:
            fs.configure(
                include=[
                    fs.upc.readonly(),
                    fs.product.readonly(),
                    fs.cases_ordered,
                    fs.units_ordered,
                ])

    def before_create_row(self, form):
        row = form.fieldset.model
        batch = self.get_instance()
        row.sequence = max([0] + [r.sequence for r in batch.data_rows]) + 1
        row.batch = batch
        # TODO: this seems heavy-handed but works..
        row.product_uuid = self.item_lookup(form.fieldset.item_lookup.value)

    def after_create_row(self, row):
        self.handler.refresh_row(row)

    def redirect_after_create_row(self, row):
        self.request.session.flash("Added item: {} {}".format(row.upc.pretty(), row.product))
        return self.redirect(self.request.current_route_url())

    def delete_row(self):
        """
        Update the PO total in addition to marking row as removed.
        """
        row = self.Session.query(self.model_row_class).get(self.request.matchdict['uuid'])
        if not row:
            raise httpexceptions.HTTPNotFound()
        if row.po_total:
            row.batch.po_total -= row.po_total
        row.removed = True
        return self.redirect(self.get_action_url('view', row.batch))

    # TODO: redirect to new purchase...
    # def get_execute_success_url(self, batch, result, **kwargs):
    #     # return self.get_action_url('view', batch)
    #     return

    def order_form(self):
        """
        View for editing a purchase batch as an order form.
        """
        batch = self.get_instance()
        if batch.executed:
            return self.redirect(self.get_action_url('view', batch))

        # organize existing batch rows by product
        order_items = {}
        for row in batch.data_rows:
            if not row.removed:
                order_items[row.product_uuid] = row

        # organize vendor catalog costs by dept / subdept
        departments = {}
        costs = self.get_order_form_costs(batch.vendor)\
                    .order_by(model.Brand.name,
                              model.Product.description,
                              model.Product.size)
        for cost in costs:

            department = cost.product.department
            if department:
                departments.setdefault(department.uuid, department)
            else:
                if None not in departments:
                    department = Object()
                    departments[None] = department
                department = departments[None]
            
            subdepartments = getattr(department, '_order_subdepartments', None)
            if subdepartments is None:
                subdepartments = department._order_subdepartments = {}

            subdepartment = cost.product.subdepartment
            if subdepartment:
                subdepartments.setdefault(subdepartment.uuid, subdepartment)
            else:
                if None not in subdepartments:
                    subdepartment = Object()
                    subdepartments[None] = subdepartment
                subdepartment = subdepartments[None]

            subdept_costs = getattr(subdepartment, '_order_costs', None)
            if subdept_costs is None:
                subdept_costs = subdepartment._order_costs = []
            subdept_costs.append(cost)
            cost._batchrow = order_items.get(cost.product_uuid)

            # do anything else needed to satisfy template display requirements etc.
            self.decorate_order_form_cost(cost)

        # fetch last 6 purchases for this vendor, organize line items by product
        history = OrderedDict()
        purchases = Session.query(model.Purchase)\
                           .filter(model.Purchase.vendor == batch.vendor)\
                           .filter(model.Purchase.status >= enum.PURCHASE_STATUS_ORDERED)\
                           .order_by(model.Purchase.date_ordered.desc(), model.Purchase.created.desc())\
                           .options(orm.joinedload(model.Purchase.items))[:6]
        for purchase in purchases[:6]:
            items = {}
            for item in purchase.items:
                items[item.product_uuid] = item
            history[purchase.uuid] = {'purchase': purchase, 'items': items}

        # reverse sorting and pad history as needed, for template convenience
        for i in range(6 - len(history)):
            history[i] = None
        history = OrderedDict([(i, v) for i, v in enumerate(reversed(list(history.itervalues())))])

        title = self.get_instance_title(batch)
        return self.render_to_response('order_form', {
            'batch': batch,
            'instance': batch,
            'instance_title': title,
            'index_title': "{}: {}".format(self.get_model_title(), title),
            'index_url': self.get_action_url('view', batch),
            'vendor': batch.vendor,
            'departments': departments,
            'history': history,
            'get_upc': lambda p: p.upc.pretty() if p.upc else '',
        })

    def get_order_form_costs(self, vendor):
        return Session.query(model.ProductCost)\
                      .join(model.Product)\
                      .outerjoin(model.Brand)\
                      .filter(model.ProductCost.vendor == vendor)

    def decorate_order_form_cost(self, cost):
        pass

    def order_form_update(self):
        """
        Handles AJAX requests to update current batch, from Order Form view.
        """
        batch = self.get_instance()

        cases_ordered = self.request.POST.get('cases_ordered', '0')
        if not cases_ordered or not cases_ordered.isdigit():
            return {'error': "Invalid value for cases ordered: {}".format(cases_ordered)}
        cases_ordered = int(cases_ordered)

        units_ordered = self.request.POST.get('units_ordered', '0')
        if not units_ordered or not units_ordered.isdigit():
            return {'error': "Invalid value for units ordered: {}".format(units_ordered)}
        units_ordered = int(units_ordered)

        uuid = self.request.POST.get('product_uuid')
        product = Session.query(model.Product).get(uuid) if uuid else None
        if not product:
            return {'error': "Product not found"}

        rows = [row for row in batch.data_rows if row.product_uuid == uuid]
        if rows:
            assert len(rows) == 1
            row = rows[0]
            if row.po_total and not row.removed:
                batch.po_total -= row.po_total
            if cases_ordered or units_ordered:
                row.cases_ordered = cases_ordered
                row.units_ordered = units_ordered
                row.removed = False
                self.handler.refresh_row(row)
            else:
                row.removed = True

        elif cases_ordered or units_ordered:
            row = model.PurchaseBatchRow()
            row.sequence = max([0] + [r.sequence for r in batch.data_rows]) + 1
            row.product = product
            batch.data_rows.append(row)
            row.cases_ordered = cases_ordered
            row.units_ordered = units_ordered
            self.handler.refresh_row(row)

        return {
            'row_cases_ordered': '' if row.removed else int(row.cases_ordered),
            'row_units_ordered': '' if row.removed else int(row.units_ordered),
            'row_po_total': '' if row.removed else '${:0,.2f}'.format(row.po_total),
            'batch_po_total': '${:0,.2f}'.format(batch.po_total),
        }

    @classmethod
    def defaults(cls, config):
        route_prefix = cls.get_route_prefix()
        url_prefix = cls.get_url_prefix()
        permission_prefix = cls.get_permission_prefix()
        model_key = cls.get_model_key()
        model_title = cls.get_model_title()

        cls._batch_defaults(config)
        cls._defaults(config)

        # order form
        config.add_tailbone_permission(permission_prefix, '{}.order_form'.format(permission_prefix),
                                       "Edit new {} in Order Form mode".format(model_title))
        config.add_route('{}.order_form'.format(route_prefix), '{}/{{{}}}/order-form'.format(url_prefix, model_key))
        config.add_view(cls, attr='order_form', route_name='{}.order_form'.format(route_prefix),
                        permission='{}.order_form'.format(permission_prefix))
        config.add_route('{}.order_form_update'.format(route_prefix), '{}/{{{}}}/order-form/update'.format(url_prefix, model_key))
        config.add_view(cls, attr='order_form_update', route_name='{}.order_form_update'.format(route_prefix),
                        renderer='json', permission='{}.order_form'.format(permission_prefix))


def includeme(config):
    PurchaseBatchView.defaults(config)
