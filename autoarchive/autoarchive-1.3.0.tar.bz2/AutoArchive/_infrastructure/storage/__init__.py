# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2014 Róbert Čerňanský



"""Implementation of storage :term:`Storage`.

Implements application's persistent storage interface :class:`.IStorage`.  The implementation is provided by
:class:`.FileStorage` class.  It should be constructed by some infrastructure component and distributed to other
components.  Individual components should not instantiate it directly."""
