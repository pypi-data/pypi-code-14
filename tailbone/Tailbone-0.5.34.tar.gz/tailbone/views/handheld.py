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
Views for handheld batches
"""

from __future__ import unicode_literals, absolute_import

from rattail import enum
from rattail.db import model
from rattail.db.batch.handheld.handler import HandheldBatchHandler
from rattail.util import OrderedDict

import formalchemy as fa
import formencode as fe
from webhelpers.html import tags

from tailbone import forms
from tailbone.views.batch import FileBatchMasterView


ACTION_OPTIONS = OrderedDict([
    ('make_label_batch', "Make a new Label Batch"),
    ('make_inventory_batch', "Make a new Inventory Batch"),
])


class ExecutionOptions(fe.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    action = fe.validators.OneOf(ACTION_OPTIONS)


class InventoryBatchFieldRenderer(fa.FieldRenderer):
    """
    Renderer for handheld batch's "inventory batch" field.
    """

    def render_readonly(self, **kwargs):
        batch = self.raw_value
        if batch:
            return tags.link_to(
                batch.id_str,
                self.request.route_url('batch.inventory.view', uuid=batch.uuid))
        return ''



class HandheldBatchView(FileBatchMasterView):
    """
    Master view for handheld batches.
    """
    model_class = model.HandheldBatch
    model_title_plural = "Handheld Batches"
    batch_handler_class = HandheldBatchHandler
    route_prefix = 'batch.handheld'
    url_prefix = '/batch/handheld'
    execution_options_schema = ExecutionOptions
    editable = False
    refreshable = False

    model_row_class = model.HandheldBatchRow
    rows_creatable = False
    rows_editable = True

    def configure_grid(self, g):
        g.configure(
            include=[
                g.id,
                g.created,
                g.created_by,
                g.device_name,
                g.executed,
                g.executed_by,
            ],
            readonly=True)

    def configure_fieldset(self, fs):
        fs.configure(
            include=[
                fs.id,
                fs.created,
                fs.created_by,
                fs.filename,
                fs.device_type.with_renderer(forms.renderers.EnumFieldRenderer(enum.HANDHELD_DEVICE_TYPE)),
                fs.device_name,
                fs.executed,
                fs.executed_by,
            ])
        if self.creating:
            del fs.id
        elif self.viewing and fs.model.inventory_batch:
            fs.append(fa.Field('inventory_batch', value=fs.model.inventory_batch, renderer=InventoryBatchFieldRenderer))

    def configure_row_grid(self, g):
        g.configure(
            include=[
                g.sequence,
                g.upc.label("UPC"),
                g.brand_name.label("Brand"),
                g.description,
                g.size,
                g.cases,
                g.units,
                g.status_code.label("Status"),
            ],
            readonly=True)

    def row_grid_row_attrs(self, row, i):
        attrs = {}
        if row.status_code == row.STATUS_PRODUCT_NOT_FOUND:
            attrs['class_'] = 'warning'
        return attrs

    def _preconfigure_row_fieldset(self, fs):
        super(HandheldBatchView, self)._preconfigure_row_fieldset(fs)
        fs.upc.set(readonly=True, label="UPC", renderer=forms.renderers.GPCFieldRenderer,
                   attrs={'link': lambda r: self.request.route_url('products.view', uuid=r.product_uuid)})
        fs.brand_name.set(readonly=True)
        fs.description.set(readonly=True)
        fs.size.set(readonly=True)

    def configure_row_fieldset(self, fs):
        fs.configure(
            include=[
                fs.sequence,
                fs.upc,
                fs.brand_name,
                fs.description,
                fs.size,
                fs.status_code,
                fs.cases,
                fs.units,
            ])

    def get_exec_options_kwargs(self, **kwargs):
        kwargs['ACTION_OPTIONS'] = list(ACTION_OPTIONS.iteritems())
        return kwargs

    def get_execute_success_url(self, batch, result, **kwargs):
        if kwargs['action'] == 'make_inventory_batch':
            return self.request.route_url('batch.inventory.view', uuid=result.uuid)
        elif kwargs['action'] == 'make_label_batch':
            return self.request.route_url('batch.rows', uuid=result.uuid)
        return super(HandheldBatchView, self).get_execute_success_url(batch)

    @classmethod
    def defaults(cls, config):

        # fix permission group title
        config.add_tailbone_permission_group('batch.handheld', "Handheld Batches")

        cls._filebatch_defaults(config)
        cls._batch_defaults(config)
        cls._defaults(config)


def includeme(config):
    HandheldBatchView.defaults(config)
