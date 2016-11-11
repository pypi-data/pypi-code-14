from datetime import datetime


_NOW = datetime.now()


CHANGES = """ChangeLog
=========

0.0.1 (%02d-%02d-%02d)
--------------------

Bug Handling
~~~~~~~~~~~~

-


Features
~~~~~~~~

-


""" % (_NOW.year, _NOW.month, _NOW.day)
