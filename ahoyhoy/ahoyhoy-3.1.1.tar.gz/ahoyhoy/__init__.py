pkgresources = __import__('pkg_resources')

_distribution = pkgresources.get_distribution("ahoyhoy")

PROJECT_NAME = _distribution.project_name
__version__ = _distribution.version if _distribution else '0.0'
