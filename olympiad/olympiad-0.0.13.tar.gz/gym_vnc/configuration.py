import logging
from gym import configuration

# Should be "gym_vnc", but we'll support people doing somewhat crazy
# things.
package_name = '.'.join(__name__.split('.')[:-1])
gym_vnc_logger = logging.getLogger(package_name)

gym_vnc_logger.setLevel(logging.INFO)

if hasattr(configuration, '_extra_loggers'):
    configuration._extra_loggers.append(gym_vnc_logger)
