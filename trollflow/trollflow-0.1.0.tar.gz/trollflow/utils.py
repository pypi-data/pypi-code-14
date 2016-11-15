import importlib
import logging

logger = logging.getLogger(__name__)


def get_class(clazz_path):
    parts = clazz_path.split('.')
    module_name = ".".join(parts[:-1])
    clazz_name = parts[-1]
    module = importlib.import_module(module_name)
    clazz = getattr(module, clazz_name)
    logger.info("Initialized {0}".format(clazz))
    return clazz
