# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Admin tests."""

from __future__ import absolute_import, print_function

import pytest
from invenio_admin import InvenioAdmin
from wtforms.validators import ValidationError

from invenio_files_rest.admin import require_slug
from invenio_files_rest.models import Bucket, ObjectVersion


def test_require_slug():
    """Test admin views."""
    class TestField(object):
        def __init__(self, data):
            self.data = data

    assert require_slug(None, TestField('aslug')) is None
    pytest.raises(ValidationError, require_slug, None, TestField('Not A Slug'))


def test_admin_views(app, db, dummy_location):
    """Test admin views."""
    app.config['SECRET_KEY'] = 'CHANGEME'
    InvenioAdmin(app, permission_factory=None, view_class_factory=lambda x: x)

    b1 = Bucket.create(location=dummy_location)
    obj = ObjectVersion.create(b1, 'test').set_location('placeuri', 1, 'chk')
    db.session.commit()

    with app.test_client() as client:
        res = client.get('/admin/bucket/')
        assert res.status_code == 200
        assert str(b1.id) in res.get_data(as_text=True)

        res = client.get('/admin/fileinstance/')
        assert res.status_code == 200
        assert str(obj.file_id) in res.get_data(as_text=True)

        res = client.get('/admin/location/')
        assert res.status_code == 200
        assert str(b1.location.name) in res.get_data(as_text=True)

        res = client.get('/admin/objectversion/')
        assert res.status_code == 200
        assert str(obj.version_id) in res.get_data(as_text=True)
