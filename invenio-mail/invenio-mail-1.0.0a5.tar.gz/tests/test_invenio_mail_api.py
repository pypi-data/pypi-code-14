# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
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

"""Test package API."""

from __future__ import absolute_import, print_function

from invenio_mail.api import TemplatedMessage


def test_templated_message(email_api_app, email_params, email_ctx):
    """Test that all the fields given are inside the message."""
    with email_api_app.app_context():
        msg = TemplatedMessage(template_body='invenio_mail/base.txt',
                               template_html='invenio_mail/base.html',
                               ctx=email_ctx, **email_params)

        for key in email_params:
            assert email_params[key] == getattr(msg, key), key

        # let's check that the body and html are correctly formatted
        assert '<p>Dear {0},</p>'.format(email_ctx['user']) in msg.html
        assert 'Dear {0},'.format(email_ctx['user']) in msg.body
        assert '<p>{0}</p>'.format(email_ctx['content']) in msg.html
        assert '{0}'.format(email_ctx['content']) in msg.body
        assert email_ctx['sender'] in msg.html
        assert email_ctx['sender'] in msg.body
