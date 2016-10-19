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
Fabric library for Apache web server
"""

from __future__ import unicode_literals, absolute_import

from fabric.api import sudo

from rattail.fablib import apt, get_debian_version


def install():
    """
    Install the Apache web service
    """
    apt.install('apache2')


def install_wsgi(python_home=None):
    """
    Install the mod_wsgi Apache module, with optional ``WSGIPythonHome`` value.
    """
    apt.install('libapache2-mod-wsgi')
    if python_home:
        if get_debian_version() < 8: # pre-jessie has apache 2.2
            sudo('echo WSGIPythonHome {} > /etc/apache2/conf.d/wsgi'.format(python_home))
        else:
            sudo('echo WSGIPythonHome {} > /etc/apache2/conf-available/wsgi.conf'.format(python_home))
            enable_conf('wsgi')


def enable_conf(*names):
    """
    Enable the given Apache configurations
    """
    for name in names:
        sudo('a2enconf {}'.format(name))


def enable_mod(*names):
    """
    Enable the given Apache modules
    """
    for name in names:
        sudo('a2enmod {}'.format(name))


def restart():
    """
    Restart the Apache web service
    """
    sudo('service apache2 restart')


def start():
    """
    Start the Apache web service
    """
    sudo('service apache2 start')


def stop():
    """
    Stop the Apache web service
    """
    sudo('service apache2 stop')
