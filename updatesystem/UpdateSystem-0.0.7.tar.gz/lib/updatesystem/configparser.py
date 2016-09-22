
import os.path
from log import logger as logging
import ConfigParser

config_local_default={ 
"orchestra_file_path": "",
"orchestra_file_name": "",
    }

def safe_get(cf,section,key,default):
    """safe_get

    :param cf: ConfigParser object
    :param section: section in ini file
    :param key: field in section 
    :param default: if field or value is not exists , return the default

    """
    try:
        return cf.get(section,key)
    except ConfigParser.NoOptionError, e:
        logging.debug("NoOptionError" ,exc_info=True)
        return default 
    except:
        logging.warn("exception",exc_info=True)
        return default


def get_config(filename="/etc/us/config.ini",section_name="local",config_default=config_local_default):
    """get_config

    :param filename: 
    :param section_name: 
    :param config_default:
    """
    config = dict()
    cf = ConfigParser.ConfigParser()
    if not  os.path.isfile(filename):
        logging.error("config file {} is not exists".format(filename))
        return config
    try:
        logging.debug("read file {}".format(filename))
        cf.read(filename)
        for key in config_default:
            config[key] = safe_get(cf,section_name, key, config_default[key])
    except IOError,e:
        logging.error("read file failed: {}".format(filename),exc_info=True)
    except ConfigParser.NoOptionError, e:
        logging.error("NoOptionError" ,exc_info=True)
    except:
        logging.error("Exception",exc_info=True)
    return config

if __name__ == "__main__":
    print(get_config())

