#
# growler_ext/SassMiddleware.py
#
"""
Loader script for the MakoRenderer class.

This script overloads the expected module object with the class MakoRenderer.
"""

import sys
from growler_sass import SassMiddleware

sys.modules[__name__] = SassMiddleware
