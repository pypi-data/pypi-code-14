# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__name__), '..', 'src', 'brite_etl'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.inheritance_diagram',
    'autoapi.sphinx',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]
if os.getenv('SPELLCHECK'):
    extensions += 'sphinxcontrib.spelling',
    spelling_show_suggestions = True
    spelling_lang = 'en_US'

source_suffix = '.rst'
master_doc = 'index'
project = u'BriteETL'
year = '2016'
author = u'Hayden Bickerton'
copyright = '{0}, {1}'.format(year, author)
version = release = u'0.1.1'

pygments_style = 'trac'
templates_path = ['.']
extlinks = {
    'issue': ('https://github.com/haydenbbickerton/brite_etl/issues/%s', '#'),
    'pr': ('https://github.com/haydenbbickerton/brite_etl/pull/%s', 'PR #'),
}
# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only set the theme if we're building docs locally
    html_theme = 'sphinx_rtd_theme'

if on_rtd:
    from mock import Mock as MagicMock

    class Mock(MagicMock):
        @classmethod
        def __getattr__(cls, name):
                return Mock()

    MOCK_MODULES = ['xlwings', 'numpy', 'pandas']
    sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)

html_use_smartypants = True
html_last_updated_fmt = '%b %d, %Y'
html_split_index = False
html_sidebars = {
   '**': ['searchbox.html', 'globaltoc.html', 'sourcelink.html'],
}
html_short_title = '%s-%s' % (project, version)

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False

exclude_patterns = ['_build']

add_module_names = False

autoapi_modules = {
   'brite_etl.abstracts': {
      'prune': True,
      'override': True,
      'output': 'api'
   },
   'brite_etl.core.computations': {
      'prune': True,
      'override': True,
      'output': 'api/core'
   },
   'brite_etl.core.io': {
      'prune': True,
      'override': True,
      'output': 'api/core'
   },
   'brite_etl.core.operations': {
      'prune': True,
      'override': True,
      'output': 'api/core'
   },
   'brite_etl.lib': {
      'prune': True,
      'override': True,
      'output': 'api'
   },
   'brite_etl.utils': {
      'prune': True,
      'override': True,
      'output': 'api'
   }
}
