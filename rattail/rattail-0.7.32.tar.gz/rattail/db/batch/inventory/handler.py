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
Handler for inventory batches
"""

from __future__ import unicode_literals, absolute_import

from rattail.db import api, model
from rattail.db.batch.handler import BatchHandler


class InventoryBatchHandler(BatchHandler):
    """
    Handler for inventory batches.
    """
    batch_model_class = model.InventoryBatch
    show_progress = True

    def refresh_data(self, session, batch, progress=None):
        """
        Refresh all data for the batch.
        """
        del batch.data_rows[:]
        data = list(self.read_handheld_rows(session, batch.handheld_batch))
        self.make_rows(session, batch, data, progress=progress)

    def read_handheld_rows(self, session, handheld_batch):
        """
        Read data rows from handheld batch.
        """
        for hh in handheld_batch.data_rows:
            if not hh.removed:
                row = model.InventoryBatchRow()
                row.upc = hh.upc
                row.cases = hh.cases
                row.units = hh.units
                yield row

    def cognize_row(self, session, row):
        """
        Inspect a row from the source data and populate additional attributes
        for it, according to what we find in the database.
        """
        if not row.upc:
            row.status_code = row.STATUS_PRODUCT_NOT_FOUND
            return

        product = api.get_product_by_upc(session, row.upc)
        if not product:
            row.status_code = row.STATUS_PRODUCT_NOT_FOUND
            return

        # current / static attributes
        row.product = product
        if product.brand:
            row.brand_name = product.brand.name
        row.description = product.description
        row.size = product.size
        row.status_code = row.STATUS_OK
