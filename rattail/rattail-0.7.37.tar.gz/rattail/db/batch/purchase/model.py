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
Models for purchase order batches
"""

from __future__ import unicode_literals, absolute_import

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr

from rattail.db.model import Base
from rattail.db.batch.model import BatchMixin, BatchRowMixin
from rattail.db.model.purchase import PurchaseBase, PurchaseItemBase


class PurchaseBatch(BatchMixin, PurchaseBase, Base):
    """
    Hopefully generic batch used for entering new purchases into the system, etc.?
    """
    batch_key = 'purchase'
    __tablename__ = 'purchase_batch'
    __batchrow_class__ = 'PurchaseBatchRow'

    @declared_attr
    def __table_args__(cls):
        return cls.__batch_table_args__() + cls.__purchase_table_args__()

    complete = sa.Column(sa.Boolean(), nullable=True, doc="""
    Flag to indicate whether the batch is complete.  This may be used to assist
    with workflow when entering/executing new purchases.
    """)


class PurchaseBatchRow(BatchRowMixin, PurchaseItemBase, Base):
    """
    Row of data within a purchase batch.
    """
    __tablename__ = 'purchase_batch_row'
    __batch_class__ = PurchaseBatch

    @declared_attr
    def __table_args__(cls):
        return cls.__batchrow_table_args__() + cls.__purchaseitem_table_args__()

    STATUS_OK                           = 1
    STATUS_PRODUCT_NOT_FOUND            = 2
    STATUS_COST_NOT_FOUND               = 3
    STATUS_CASE_QUANTITY_UNKNOWN        = 4

    STATUS = {
        STATUS_OK                       : "ok",
        STATUS_PRODUCT_NOT_FOUND        : "product not found",
        STATUS_COST_NOT_FOUND           : "product found but not cost",
        STATUS_CASE_QUANTITY_UNKNOWN    : "case quantity not known",
    }
