"""
This file is part of py-mpache.

py-mpache is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

py-mpache is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with py-mpache.  If not, see <http://www.gnu.org/licenses/>

For information on method calls, see 'pydoc libmpache.connection'

----------
Basic example:
----------

import libmpache

conn = libmpache.Connection('http://localhost' , 'admin' , 'password')
print conn.ping()

"""

from connection import *

__version__ = '0.0.1'
