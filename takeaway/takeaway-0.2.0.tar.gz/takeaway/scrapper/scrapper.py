from .basic import BasicScrapper, BasicThread
from .vietnamm import VietnamScrapper, VietnamThread
from .de import DeScrapper, DeThread
from .error import ScrapperError

import logging

NUMBER_OF_THREAD = 5

WEBSITE = {'BE': ['https://www.pizza.be', ["/en", "/nl", "/fr", "/de"]],  # Ok
           'FR': ['https://www.pizza.fr', [""]],  # Ok
           'NL': ['https://www.thuisbezorgd.nl', [""]],  # Ok
           'AT': ['https://www.lieferservice.at', [""]],  # Ok
           'CH': ['https://www.lieferservice.ch', [""]],  # Ok
           'LU': ['https://www.pizza.lu', [""]],  # Ok
           'PT': ['https://www.pizza.pt', [""]],  # Ok
           'DE': ['https://www.lieferando.de', ["/en"]],  # Not working (website different)
           'PL': ['https://pyszne.pl', [""]],  # Not working (website different)
           'VT': ['https://www.vietnammm.com', ["/en"]]  # Ok
           }

BASIC_SCRAPPER = ['BE', 'FR', 'NL', 'AT', 'CH', 'LU', 'PT', ]
VIETNAM_SCRAPPER = ["VT"]
DE_SCRAPPER = ['DE']  # Not working


def get_scrapper(country, postcode):
    website = WEBSITE[country][0]
    language = WEBSITE[country][1][0]

    if country in BASIC_SCRAPPER:
        logging.info("Basic scrapper")
        return BasicScrapper(postcode, website, language, NUMBER_OF_THREAD, BasicThread)
    elif country in VIETNAM_SCRAPPER:
        logging.info("Vietnam scrapper")
        return VietnamScrapper(postcode, website, language, NUMBER_OF_THREAD, VietnamThread)
    elif country in DE_SCRAPPER:
        logging.info("DE Scrapper")
        return DeScrapper(postcode, website, language, NUMBER_OF_THREAD, DeThread)
    else:
        raise ScrapperError(1999, country=country)
