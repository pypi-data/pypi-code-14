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
Handler for label batches
"""

from __future__ import unicode_literals, absolute_import

import csv
import logging

import sqlalchemy as sa

from rattail import enum
from rattail.db import model, api
from rattail.gpc import GPC
from rattail.db.batch.handler import BatchHandler
from rattail.util import progress_loop
from rattail.time import make_utc
from rattail.config import parse_bool


log = logging.getLogger(__name__)


class LabelBatchHandler(BatchHandler):
    """
    Handler for Print Labels batches.
    """
    batch_model_class = model.LabelBatch
    model_title = "Label Batch"
    show_progress = True

    def make_batch(self, session, filepath=None, products=None, progress=None, **kwargs):
        """
        Create a new label batch and maybe fill it, if we were given something
        good to work with.  A HandheldBatch or sequence/query of Product
        objects are supported for source data.
        """
        self.label_profile = self.get_label_profile(session)
        assert self.label_profile
        self.now = make_utc()
        self.setup()
        self.sequence = 1

        if filepath:
            kwargs['progress'] = progress
            batch = self.make_batch_from_file(session, filepath, **kwargs)
        elif products:
            batch = model.LabelBatch(**kwargs)
            self.rebuild_from_products(session, batch, products, progress)

        self.teardown()
        return batch

    def make_batch_from_file(self, session, path, skip_first_line=False,
                             calc_check_digit='upc', progress=None, **kwargs):
        """
        Make a new batch using the given file as data source.
        """
        skip_first_line = parse_bool(skip_first_line)
        if calc_check_digit != 'upc':
            calc_check_digit = parse_bool(calc_check_digit)

        batch = model.LabelBatch(**kwargs)
        with open(path, 'rb') as f:
            if skip_first_line:
                f.readline()
            reader = csv.reader(f)
            lines = list(reader)

        def convert(line, i):
            upc = line[0].strip()
            if not upc:
                return

            upc = GPC(upc, calc_check_digit=calc_check_digit)
            product = api.get_product_by_upc(session, upc)
            if not product:
                log.warning("product not found: {}".format(upc))
                return

            row = model.LabelBatchRow(sequence=self.sequence)
            self.sequence += 1
            row.product = product
            row.label_code = self.label_profile.code
            row.label_profile = self.label_profile
            row.label_quantity = 1
            batch.data_rows.append(row)
            self.cognize_row(session, row)

        progress_loop(convert, lines, progress,
                      message="Adding batch rows from file")
        return batch

    def rebuild_from_products(self, session, batch, products, progress=None):
        """
        Rebuild the given batch from the given products.
        """
        def convert(product, i):
            row = model.LabelBatchRow(sequence=self.sequence)
            self.sequence += 1
            row.product = product
            row.label_code = self.label_profile.code
            row.label_profile = self.label_profile
            row.label_quantity = 1
            batch.data_rows.append(row)
            self.cognize_row(session, row)

        progress_loop(convert, products, progress, count=products.count(),
                      message="Copying product rows to label batch")

    def refresh_data(self, session, batch, progress=None):
        """
        Refresh all data for the batch.
        """
        self.label_profile = self.get_label_profile(session)
        assert self.label_profile

        self.setup()

        if batch.handheld_batch:

            del batch.data_rows[:]
            self.sequence = 1
            self.now = make_utc()

            def convert(handheld_row, i):
                if handheld_row.product and not handheld_row.removed:
                    row = model.LabelBatchRow(sequence=self.sequence)
                    self.sequence += 1
                    row.product = handheld_row.product
                    row.label_code = self.label_profile.code
                    row.label_profile = self.label_profile
                    row.label_quantity = handheld_row.units
                    batch.data_rows.append(row)
                    self.cognize_row(session, row)
                if i % 250 == 0:    # seems to help progress UI (?)
                    session.flush()

            progress_loop(convert, batch.handheld_batch.data_rows, progress,
                          message="Copying handheld rows to label batch")

        else:
            def refresh(row, i):
                self.cognize_row(session, row)

            progress_loop(refresh, batch.data_rows, progress,
                          message="Refreshing label product data")

        self.teardown()

    def get_label_profile(self, session):
        code = self.config.get('rattail.batch', 'labels.default_code')
        if code:
            return session.query(model.LabelProfile)\
                          .filter(model.LabelProfile.code == code)\
                          .one()
        else:
            return session.query(model.LabelProfile)\
                          .order_by(model.LabelProfile.ordinal)\
                          .first()

    def cognize_row(self, session, row):
        """
        Inspect a row from the source data and populate additional attributes
        for it, according to what we find in the database.
        """
        product = row.product
        assert product
        row.upc = product.upc
        row.brand_name = unicode(product.brand or '')
        row.description = product.description
        row.size = product.size
        department = product.department
        row.department_number = department.number if department else None
        row.department_name = department.name if department else None
        category = product.category
        row.category_code = category.code if category else None
        row.category_name = category.name if category else None
        regular_price = product.regular_price
        row.regular_price = regular_price.price if regular_price else None
        row.pack_quantity = regular_price.pack_multiple if regular_price else None
        row.pack_price = regular_price.pack_price if regular_price else None
        sale_price = product.current_price
        if sale_price:
            if (sale_price.type == enum.PRICE_TYPE_SALE and
                sale_price.starts and sale_price.starts <= self.now and
                sale_price.ends and sale_price.ends >= self.now):
                pass            # this is what we want
            else:
                sale_price = None
        row.sale_price = sale_price.price if sale_price else None
        row.sale_start = sale_price.starts if sale_price else None
        row.sale_stop = sale_price.ends if sale_price else None
        cost = product.cost
        vendor = cost.vendor if cost else None
        row.vendor_id = vendor.id if vendor else None
        row.vendor_name = vendor.name if vendor else None
        row.vendor_item_code = cost.code if cost else None
        row.case_quantity = cost.case_size if cost else None
        if row.regular_price:
            row.status_code = row.STATUS_OK
        else:
            row.status_code = row.STATUS_REGULAR_PRICE_UNKNOWN

    def execute(self, batch, progress=None, **kwargs):
        """
        Print some labels!
        """
        return self.print_labels(batch, progress)

    def print_labels(self, batch, progress=None):
        """
        Print all labels for the given batch.
        """
        profiles = {}

        def organize(row, i):
            profile = row.label_profile
            if profile.uuid not in profiles:
                profiles[profile.uuid] = profile
                profile.labels = []
            profile.labels.append((row.product, row.label_quantity))

        # filter out removed rows, and maybe inactive product rows
        rows = [row for row in batch.data_rows if not row.removed]
        if self.config.getbool('rattail.batch', 'labels.exclude_inactive_products', default=False):
            rows = [row for row in rows if row.status_code != row.STATUS_PRODUCT_APPEARS_INACTIVE]

        if not progress_loop(organize, rows, progress,
                             message="Organizing labels by type"):
            return False # user canceled

        # okay now print for real
        # TODO: this is compatible with legacy code but will re-read all needed
        # product data from master table instead of levaraging batch rows
        for profile in profiles.itervalues():
            printer = profile.get_printer(self.config)
            printer.print_labels(profile.labels, progress=progress)

        return True
