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
Handler for handheld batches
"""

from __future__ import unicode_literals, absolute_import

import csv
import datetime

from sqlalchemy import orm

from rattail.db import api, model
from rattail.db.batch.handler import FileBatchHandler
from rattail.gpc import GPC
from rattail.util import load_object
from rattail.batches import get_provider
from rattail.wince import parse_batch_file


class LabelDataProxy(object):
    
    def __init__(self, session, handheld_batch):
        self.session = session
        self.handheld_batch = handheld_batch

    def __iter__(self):
        for row in self.handheld_batch.data_rows:
            if row.product:
                yield row.product

    def count(self):
        return len(self.handheld_batch.data_rows)


class HandheldBatchHandler(FileBatchHandler):
    """
    Handler for handheld batches.
    """
    batch_model_class = model.HandheldBatch
    show_progress = True

    def refresh_data(self, session, batch, progress=None):
        """
        Refresh all data for the batch.
        """
        del batch.data_rows[:]
        data = list(self.parse_rows(batch.filepath(self.config), progress=progress))
        self.make_rows(session, batch, data, progress=progress)

    def parse_rows(self, data_path, progress=None):
        """
        Parse a data path and generate initial row objects.
        """
        with open(data_path, 'rb') as f:
            line = f.readline()
        if '\x00' in line:
            return self.parse_rows_ce(data_path, progress=progress)
        else:
            return self.parse_rows_csv(data_path)

    def parse_rows_ce(self, data_path, progress=None):
        """
        Parse a RattailCE file to generate initial rows.
        """
        for scancode, cases, units in parse_batch_file(data_path, progress=progress):
            row = model.HandheldBatchRow()
            row.upc = GPC(int(scancode), calc_check_digit='upc')
            row.cases = cases
            row.units = units
            yield row

    def parse_rows_csv(self, data_path):
        """
        Parse a CSV file to generate initial rows.
        """
        with open(data_path, 'rb') as f:
            reader = csv.DictReader(f)
            for data in reader:
                row = model.HandheldBatchRow()
                row.upc = GPC(int(data['upc']), calc_check_digit='upc')
                row.cases = int(data['cases'])
                row.units = int(data['units'])
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

    def execute(self, batch, user=None, action='make_inventory_batch', progress=None, **kwargs):
        if action == 'make_inventory_batch':
            return self.make_inventory_batch(batch, user, progress=progress)
        elif action == 'make_label_batch':
            return self.make_label_batch(batch, user, progress=progress)
        return True

    def make_inventory_batch(self, handheld_batch, user, progress=None):
        # TODO: clearly this should leverage registered default
        inventory_handler = load_object('rattail.db.batch.inventory.handler:InventoryBatchHandler')(self.config)
        session = orm.object_session(handheld_batch)
        inventory_batch = inventory_handler.make_batch(session, created_by=user,
                                                       handheld_batch=handheld_batch)
        inventory_handler.refresh_data(session, inventory_batch)
        inventory_batch.cognized = datetime.datetime.utcnow()
        inventory_batch.cognized_by = user
        return inventory_batch

    def make_label_batch(self, handheld_batch, user, progress=None):
        # TODO: this is all legacy code, needs to be refactored for new-style batch
        batch_type = self.config.get('rattail.batch', 'handheld.legacy_label_batch_type',
                                     default='print_labels')
        provider = get_provider(self.config, batch_type)
        session = orm.object_session(handheld_batch)
        data = LabelDataProxy(session, handheld_batch)
        batch = provider.make_batch(session, data)
        batch.description = "Print Labels (from Handheld Batch {})".format(handheld_batch.id_str)
        return batch
