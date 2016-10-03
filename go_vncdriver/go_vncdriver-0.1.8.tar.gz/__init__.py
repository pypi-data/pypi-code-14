# We need to ensure this gets imported before tensorflow.
# This at least ensures we're not failing for import ordering reasons.
# See github issue #49 for more info.
# https://github.com/openai/gym-vnc/issues/49
from __future__ import absolute_import
import sys
if 'tensorflow' in sys.modules:
    raise error.Error('go_vncdriver must be imported before tensorflow')

from go_vncdriver.go_vncdriver import *
