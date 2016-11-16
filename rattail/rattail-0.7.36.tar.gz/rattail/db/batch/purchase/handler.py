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
Handler for purchase order batches
"""

from __future__ import unicode_literals, absolute_import

from sqlalchemy import orm

from rattail import enum
from rattail.db import model
from rattail.db.batch.handler import BatchHandler
from rattail.util import progress_loop
from rattail.time import make_utc


class PurchaseBatchHandler(BatchHandler):
    """
    Handler for purchase order batches.
    """
    batch_model_class = model.PurchaseBatch
    show_progress = True

    def refresh_data(self, session, batch, progress=None):
        """
        Refreshing a Purchase Batch will cause each row to be refreshed,
        i.e. with the latest product data.  All rows will be left intact.  This
        also will recalculate the batch PO total.
        """
        batch.po_total = 0
        rows = [row for row in batch.data_rows if not row.removed]
        progress_loop(self.refresh_row, rows, progress,
                      message="Refreshing batch data")

    def refresh_row(self, row, i=None):
        """
        Refreshing a row will A) assume that ``row.product`` is already set to
        a valid product, and B) update various other fields on the row
        (description, size, etc.)  to reflect the current product data.  It
        also will adjust the batch PO total per the row PO total.
        """
        product = row.product
        cost = row.product.cost_for_vendor(row.batch.vendor)
        assert cost
        row.upc = product.upc
        row.brand_name = unicode(product.brand or '')
        row.description = product.description
        row.size = product.size
        if product.department:
            row.department_number = product.department.number
            row.department_name = product.department.name
        else:
            row.department_number = None
            row.department_name = None
        row.vendor_code = cost.code
        row.case_quantity = cost.case_size
        row.po_unit_cost = cost.unit_cost
        row.po_total = (row.po_unit_cost * (row.units_ordered or 0)) + (
            row.po_unit_cost * (row.cases_ordered or 0) * row.case_quantity)
        row.batch.po_total = (row.batch.po_total or 0) + row.po_total
        row.status_code = row.STATUS_OK

    def execute(self, batch, user, progress=None):
        """
        Default behavior for executing a purchase batch will create a new
        purchase, by invoking :meth:`make_purchase()`.
        """
        return self.make_purchase(batch, user, progress)

    def make_purchase(self, batch, user, progress=None):
        """
        Effectively clones the given batch, creating a new Purchase in the
        Rattail system.
        """
        session = orm.object_session(batch)
        purchase = model.Purchase()

        # TODO: should be smarter and only copy certain fields here
        for prop in orm.object_mapper(batch).iterate_properties:
            if hasattr(purchase, prop.key):
                setattr(purchase, prop.key, getattr(batch, prop.key))

        def clone(row, i):
            item = model.PurchaseItem()
            # TODO: should be smarter and only copy certain fields here
            for prop in orm.object_mapper(row).iterate_properties:
                if hasattr(item, prop.key):
                    setattr(item, prop.key, getattr(row, prop.key))
            purchase.items.append(item)

        rows = [row for row in batch.data_rows if not row.removed]
        progress_loop(clone, rows, progress,
                      message="Creating purchase items")

        purchase.created = make_utc()
        purchase.created_by = user
        purchase.status = enum.PURCHASE_STATUS_ORDERED
        session.add(purchase)
        return purchase
