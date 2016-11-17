#!/usr/bin/env python
# Copyright 2012-2016, Damian Johnson and The Tor Project
# See LICENSE for licensing information

import distutils.core
import stem

DRY_RUN = True
DRY_RUN_DESCRIPTION = "Ignore this package. This is dry-run release creation to work around PyPI limitations (https://github.com/pypa/packaging-problems/issues/74#issuecomment-260716129)."

distutils.core.setup(
  name = 'stem-dry-run' if DRY_RUN else 'stem',
  version = stem.__version__,
  description = DRY_RUN_DESCRIPTION if DRY_RUN else 'Controller library for interacting with Tor <https://www.torproject.org/>',
  license = stem.__license__,
  author = stem.__author__,
  author_email = stem.__contact__,
  url = stem.__url__,
  packages = ['stem', 'stem.descriptor', 'stem.interpreter', 'stem.response', 'stem.util'],
  keywords = 'tor onion controller',
  scripts = ['tor-prompt'],
  package_data = {'stem': ['cached_tor_manual.cfg', 'settings.cfg'], 'stem.descriptor': ['fallback_directories.cfg'], 'stem.interpreter': ['settings.cfg'], 'stem.util': ['ports.cfg']},
)
