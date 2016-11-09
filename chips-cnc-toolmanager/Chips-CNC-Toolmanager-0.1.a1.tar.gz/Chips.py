#!/usr/bin/python
# -*- coding: utf-8 -*-

##This file is part of Chips - CNC tool test and management suite
##Copyright (C) 2016  Sebastian Stetter
##https://bitbucket.org/sebste/chips

##This program is free software; you can redistribute it and/or
##modify it under the terms of the GNU General Public License
##as published by the Free Software Foundation; either version 2
##of the License, or (at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU General Public License for more details.
##
##You should have received a copy of the GNU General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import logging
from camelot.core.conf import settings, SimpleSettings

logging.basicConfig( level = logging.ERROR )
logger = logging.getLogger( 'main' )

# begin custom settings
class MySettings( SimpleSettings ):

    # add an ENGINE or a CAMELOT_MEDIA_ROOT method here to connect
    # to another database or change the location where files are stored
    #
    # def ENGINE( self ):
    #     from sqlalchemy import create_engine
    #     return create_engine( 'postgresql://user:passwd@127.0.0.1/database' )

    def setup_model( self ):
        """This function will be called at application startup, it is used to
        setup the model"""
        from camelot.core.sql import metadata
        from camelot.core.orm import setup_all
        metadata.bind = self.ENGINE()
        import camelot.model.authentication
        import camelot.model.i18n
        import camelot.model.memento

        setup_all(create_tables=True)
        metadata.create_all()
        # Load sample data with the fixure mechanism
        from chips.fixtures import update_fixtures
#        update_fixtures()


my_settings = MySettings( 'Sebastian Stetter', 'Chips - CNC tool test and management suite' )
settings.append( my_settings )
# end custom settings

def start_application():
    from camelot.view.main import main
    from chips.application_admin import MyApplicationAdmin
    main(MyApplicationAdmin())

if __name__ == '__main__':
    start_application()
