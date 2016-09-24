# -*- coding: utf-8 -*-
from DocumentTemplate.DT_HTML import HTML
from DocumentTemplate.DT_String import String

import logging
import os


logger = logging.getLogger('experimental.nodtml')
SHOW = os.environ.get('SHOW_ORIGINAL_DTML')
VALUE = os.environ.get('DEBUG_DTML_VALUE', u'')


def quotedHTML(self, *args, **kwargs):
    if SHOW:
        logger.info('hacked quotedHTML')
        logger.info(self._orig_quotedHTML(*args, **kwargs))
    return VALUE

HTML._orig_quotedHTML = HTML.quotedHTML
HTML._orig__str__= HTML.quotedHTML
HTML.quotedHTML = quotedHTML


def __call__(self, *args, **kwargs):
    if SHOW:
        logger.info('hacked string call')
        logger.info(self._orig__call__(*args, **kwargs))
    return VALUE

String._orig__call__ = String.__call__
String.__call__ = __call__


def __str__(self):
    if SHOW:
        logger.info('hacked string str')
        logger.info(self._orig__str__(*args, **kwargs))
    return VALUE

String._orig__str__ = String.__str__
String.__str__ = __str__

if VALUE:
    logger.info('Patched DTML to show: %r.', VALUE)
else:
    logger.info('Patched DTML to not show anything.')
