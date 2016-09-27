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

"""Templated message class for improved messages."""

from __future__ import absolute_import, print_function

from flask import render_template
from flask_mail import Message


class TemplatedMessage(Message):
    """Siplify creation of templated messages."""

    def __init__(self, template_body=None, template_html=None, ctx=None,
                 **kwargs):
        r"""Build message body and HTML based on provided templates.

        Provided templates can use keyword arguments ``body`` and ``html``
        respectively.

        :param template_body: Path to the text template.
        :param template_html: Path to the html template.
        :param ctx: A mapping containing additional information passed to the
            template.
        :param \*\*kwargs: Keyword arguments as defined in
            :class:`flask_mail.Message`.
        """
        if template_body:
            kwargs['body'] = render_template(
                template_body, body=kwargs.get('body'), **ctx
            )
        if template_html:
            kwargs['html'] = render_template(
                template_html, html=kwargs.get('html'), **ctx
            )
        super(TemplatedMessage, self).__init__(**kwargs)
