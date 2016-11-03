# -*- coding: utf-8 -*-
"""steenzout namespace package."""

try:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)
except ImportError:
    __import__('pkg_resources').declare_namespace(__name__)
