#!/usr/bin/env python

from takeaway.scrapper.error import ScrapperError
from takeaway.main import TakeAway
from logging.handlers import RotatingFileHandler
from takeaway.parser import get_parser

import sys
import logging
import os


def log(debug):
    logger_formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(filename)s:%(funcName)s - %(message)s')
    path = os.path.dirname(__file__)
    file_handler = RotatingFileHandler(os.path.join(path, "takeaway.log"), maxBytes=100000, backupCount=1)
    file_handler.setFormatter(logger_formatter)
    logger = logging.getLogger()
    logger.addHandler(file_handler)

    if debug is not False:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logger_formatter)
        logger.addHandler(console_handler)
        if type(debug) is int:
            logger.setLevel(debug)
        else:
            logger.setLevel(20)
    else:
        logger.setLevel(40)


def main():

    parser = get_parser()
    args = parser.parse_args()  # argparse
    log(args.log_lvl)

    try:
        takeaway = TakeAway(country=args.country, postcode=args.postcode, args=args)  # Init PizzaCli class
        takeaway.interface.run()
    except ScrapperError as e:  # If postcode not in database and no network access the init fail.
        logging.critical("Can not init PizzaCli: {} {}".format(args.country.upper(), args.postcode))
        print("Error {}: {}".format(e, e.code[e.args[0]]))
        sys.exit(0)

if __name__ == "__main__":
    main()
