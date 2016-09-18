from .basic import BasicScrapper, BasicThread
from .error import ScrapperError
from .request import Request

from bs4 import BeautifulSoup

import logging
import re


class VietnamScrapper(BasicScrapper):
    def get_postcode_url(self, data=None):
        """
        Search is not by postcode but by city and district. We must first find the value of the district
        Then we request the url with the same method as basic but we a different payload
        :param data:
        :return:
        """
        FIND_DISTRICT_URL = "/fillDistricts.php"
        CITY = {"da nang": 1908884,
                "ha noi": 1908534,
                "ho chi minh city": 1908654,
                }
        logging.info('Get url for postcode {}'.format(self.postcode))
        user_input = self.postcode.split("-")
        if len(user_input) == 1:
            city = user_input[0].strip()
            district_user = None
        elif len(user_input) == 2:
            city = user_input[0].strip()
            district_user = user_input[1].strip().lower()
        else:
            raise ScrapperError(1000, msg="Input error")

        try:
            data = {"locid": CITY[city.lower()],
                    "submit": None}
        except KeyError:
            raise ScrapperError(1004, city=city)

        rep = Request.post(self.website + self.language + FIND_DISTRICT_URL, data=data)
        bs_obj = BeautifulSoup(rep.text, "html.parser")
        districts = bs_obj.find_all("option")
        if district_user is None or district_user == "":
            district_list = list()
            for district in districts:
                district_list.append(district.get_text())
            raise ScrapperError(1003, district=district_list[1:], city=city)
        else:
            district_value = None
            for district in districts:
                if district_user == district.get_text().lower():
                    district_value = district["value"]
            if district_value is None:
                raise ScrapperError(1000)

        data = {
            'customerdeliveryarea': '',
            'geo': 'false',
            'mysearchstring': 'false',
            'redirect': 'false',
            'searchstring1': CITY[city.lower()],
            "searchstring2": district_value,
            'type': 'citydistrict'
        }

        return super().get_postcode_url(data)


class VietnamThread(BasicThread):

    @staticmethod
    def dl_meals_price(text):
        text = text.replace(".", "")
        return text[:-1], text[-1]
