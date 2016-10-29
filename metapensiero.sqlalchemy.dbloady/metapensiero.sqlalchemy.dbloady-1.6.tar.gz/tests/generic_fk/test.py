# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- Test effects
# :Created:   sab 29 ott 2016 02:09:32 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

import sqlite3
import sys

c = sqlite3.connect(sys.argv[1])

result = c.execute("""\
SELECT count(*)
FROM supplier s
 JOIN address a ON a.object_id = s.id AND a.object_kind = 'Supplier'""").fetchone()
assert result == (1,)

result = c.execute("""\
SELECT count(*)
FROM customer c
 JOIN address a ON a.object_id = c.id AND a.object_kind = 'Customer'""").fetchone()
assert result == (1,)
