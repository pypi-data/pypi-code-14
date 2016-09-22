from .basic import BasicScrapper, BasicThread
from .request import Request
from .error import ScrapperError

from bs4 import BeautifulSoup

import logging
import json.decoder



class DeScrapper(BasicScrapper):
    def get_postcode_url(self):
        logging.info('Get url for postcode {}'.format(self.postcode))
        FIND_RESTAURANT_URL = "/location/cities/{}.json?YD_X_DOMAIN={}".format(self.postcode[0:2],
                                                                               self.website[13:])

        rep = Request.get(self.website + FIND_RESTAURANT_URL)

        try:
            for data in rep.json():
                if data.get("plz") == self.postcode:
                    url = data.get('url')
                    return self.website + self.language + "/deliveryservice-" + url

        except json.decoder.JSONDecodeError:
            raise ScrapperError(1001, postcode=self.postcode, website_msg="")

        raise ScrapperError(1001, postcode=self.website, website_msg="")

    def get_restaurants_name(self, url):
        """
        Get name and url of the restaurant for this postcode

        :param url: url of postcode
        :return:
        """
        logging.info("Get restaurants for {}, url: {}".format(self.postcode, url))
        data = list()
        double = dict()
        req = Request.get(url)
        bs_obj = BeautifulSoup(req.text, "html.parser")
        restaurants = bs_obj.findAll("div", {"class": "yd-jig-service-dl"})
        for restaurant in restaurants:
            name = restaurant.find('a').get_text().strip()
            url = self.website + restaurant.find('a')['href']

            if [name, url] in data:
                if double.get(name) is None:
                    double[name] = 1
                else:
                    double[name] += 1
                name = name + str(double[name])
            data.append([name, url])

        if len(data) == 0:
            raise ScrapperError(1201, postcode=self.postcode)

        return data


class DeThread(BasicThread):
    pass
