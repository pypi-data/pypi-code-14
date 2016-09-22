import logging
from datetime import datetime

def getlogger():

    logger = logging.getLogger()
    # hard code
    now = datetime.now()
    filename="/var/log/update-system.{}-{:02d}-{:02d}.log".format(now.year, now.month,
            now.day)

    # set formatter
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] - [%(module)s %(funcName)s() line:%(lineno)d ]: %(message)s',"%Y-%m-%d %H:%M:%S") 

    # set fh 
    fh = logging.FileHandler(filename, encoding="UTF-8")
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    # set ch
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)
    # set logger with ch and fh
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


logger = getlogger()

