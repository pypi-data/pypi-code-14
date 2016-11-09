# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2015 Róbert Čerňanský



"""Component tests for :term:`Archiving`."""



from .archiving_test_utils import *
from .test_iarchiving import *
from .test_archiving_application import *



__all__ = archiving_test_utils.__all__ + test_iarchiving.__all__ + test_archiving_application.__all__
