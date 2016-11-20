import sys

if sys.version_info < (3, 0):
    import inject_methods
else:
    try:
        from . import inject_methods
        # this for python 3 __main__, ugly!!
    except SystemError:
        import inject_methods


__author__ = 'Colin Ji'
__versioninfo__ = (1, 0, 0)
__version__ = '.'.join(map(str, __versioninfo__))

__all__ = []
