__author__ = "Kiran Vemuri"
__email__ = "kkvemuri@uh.edu"
__status__ = "Development"
__maintainer__ = "Kiran Vemuri"

import logging


class Log:
    """
    Class to facilitate logging
    """

    def __init__(self, logfile):
        """
        :param logfile(str): file path to the log file to which logs are to be written to
        """
        self.logfile = logfile

    def log_handler(self):
        """
        Method to create a log handler for the specified log file
        :return log handler
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler(self.logfile)
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger
