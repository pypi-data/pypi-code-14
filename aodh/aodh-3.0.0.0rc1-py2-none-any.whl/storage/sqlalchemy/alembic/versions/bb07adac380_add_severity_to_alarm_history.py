# Copyright 2015 OpenStack Foundation
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

"""add severity to alarm history

Revision ID: bb07adac380
Revises: 12fe8fac9fe4
Create Date: 2015-08-06 15:15:43.717068

"""

# revision identifiers, used by Alembic.
revision = 'bb07adac380'
down_revision = '12fe8fac9fe4'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('alarm_history',
                  sa.Column('severity', sa.String(length=50), nullable=True))
