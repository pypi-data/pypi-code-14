from .request import Request
from .error import ScrapperError
from .output import OutputThread
from ..database.declarative import Restaurant, Category, Meal, Restaurant_open, Restaurant_info
from ..basket.error import BasketError

import re
import threading
import ast
import logging
import requests
import datetime
import time

from queue import Queue
from bs4 import BeautifulSoup


class BasicScrapper:
    """
    Basic scrapper class
    Working for:
        BE: https://www.pizza.be
        FR: https://www.pizza.fr
        NL: https://www.thuisbezorgd.nl
        AT: https://www.lieferservice.at
        CH: https://www.lieferservice.ch
        LU: https://www.pizza.lu
        PT: https://www.pizza.pt
    """

    def __init__(self, postcode, master_url, language, number_of_thread, dl_thread):
        logging.info("Init scrapper: {} {} {}".format(postcode, master_url, language))
        self.postcode = postcode
        self.website = master_url
        self.language = language
        self.number_of_thread = number_of_thread
        self.session = requests.session()
        self.thread = dl_thread

    def get_postcode_url(self, data=None):
        """
        Get the url for the postcode web page. Postcode url not always the same format
        :param data: Payload to post
        :return: string of the url
        """
        FIND_RESTAURANT_URL = "/findRestaurants.php"

        logging.info('Get url for postcode {}'.format(self.postcode))
        url = self.website + self.language + FIND_RESTAURANT_URL  # Url to request

        # Data to send
        if data is None:
            data = {
                'customerdeliveryarea': '',
                'geo': 'false',
                'mysearchstring': 'false',
                'redirect': 'false',
                'searchstring': self.postcode,
                'type': 'postcode'
            }
        req = Request.post(url, data=data)

        try:
            # The response is a dictionary so we evaluate it and take the value inside
            rep_eval = ast.literal_eval(req.text)
            # The website can response with an url
            # an custom_error or something else (if too much request were sent for ex.)
            if rep_eval["type"] == "url":
                # We omit the first character because value is : \/url
                url_arg = rep_eval["value"].replace("\\", "")
            elif rep_eval["type"] == "error":
                # Raise custom_error if the response is an custom_error (bad postcode for ex.)
                bs_obj = BeautifulSoup(rep_eval['value'], "html.parser")
                raise ScrapperError(1001, postcode=self.postcode, website_msg=bs_obj.get_text()[32:])
            else:
                # Is the response is something else we raise an custom_error
                raise ScrapperError(1002, url=url)
        except SyntaxError:
            # When the scrapper_request limit is exceeded the response is not a dict so can't be eval
            raise ScrapperError(1002, url=url)

        return self.website + url_arg  # url of postcode

    def get_restaurants_name(self, url):
        """
        Get the name and url of all restaurants in the postcode page

        :return: list([name, url], ...)
        """
        logging.info("Get restaurants for {}, url: {}".format(self.postcode, url))
        data = list()
        req = Request.get(url)

        bs_obj = BeautifulSoup(req.text, "html.parser")
        restaurants_names = bs_obj.findAll("a", {"class": "restaurantname"})
        # For all the restaurant we find on the page we create a dictionary with the name and the url
        if restaurants_names:
            double = dict()  # Dict used when two (or more) restaurants have the same name
            for restaurant in restaurants_names:
                name = restaurant.get_text()
                url = self.website + restaurant['href']

                if [name, url] in data:  # If the name is already in the dict
                    logging.debug("{} {} in double".format(name, url))
                    if double.get(name) is None:  # If the name is not in the double
                        double[name] = 2  # Set the restaurant number
                    else:  # If name already in double. restaurant is triple or more
                        double[name] += 1
                    # Append to the restaurant name the restaurant number
                    name += str(double[name])
                data.append([name, url])
        else:
            # If no restaurant name could be found
            raise ScrapperError(1201, postcode=self.postcode)

        return data

    def get_restaurants_info(self, data, interface, output=False):
        """
        Get all the information from a restaurant.

        Create a thread by restaurant
        :param data: dict to store the downloaded data dict[restaurant_name][url]
        :param output: True for the thread to output print statements
        :param interface: Output interface
        :return: list of restaurant object
        """

        logging.info("Download information about {} restaurants".format(len(data)))
        if len(data) != 0:
            download_queue = Queue()  # Queue of restaurants
            output_queue = Queue()  # Queue for print statements
            thread_list = list()
            restaurants_list = list()
            if output:
                # Thread to print from scrapper thread
                output_thread = OutputThread(output_queue, output, interface, len(data))
                output_thread.daemon = True
                output_thread.start()

            # Create Queue
            for restaurant_name, restaurant_url in data:
                download_queue.put([restaurant_name, restaurant_url, output_queue, restaurants_list, self.session])

            # Create thread
            for i in range(self.number_of_thread):
                thread = self.thread(download_queue, self.website)
                thread.daemon = True
                thread_list.append(thread)
                thread.start()

            download_queue.join()  # Wait for all the items in queue to finish

            return restaurants_list

        else:
            logging.warning("No restaurants to download")
            return False

    def checkout(self, items, confirm, remarks, user_info, postcode):
        """
        Order the items in the basket

        :param items: items to order
        :param confirm: confirm checkout
        :param remarks: remarks to add to order
        :param user_info: user info for checkout
        :param postcode: postcode object
        :return:  items checked
        """
        self.session = requests.session()  # New session to be sure online basket is empty
        logging.info("Checking out, confirm: {}, items: {}, remarks: {}".format(confirm, items, remarks))
        if len(items) == 0:  # If items to order
            raise ScrapperError(1103)
        elif len(items) > 1:  # If not more than 1 restaurant
            raise ScrapperError(1101)
        else:
            items_checked = False
            payment_url = None

            # Needed for website back-end
            Request.get(self.website, session=self.session)
            self.session.cookies.set("searchstring", postcode.postcode, domain="www.pizza.be")  # TODO Try to disable
            self.session.cookies.set("postcode", postcode.postcode, domain="www.pizza.be")  # TODO Try to disable
            Request.get(postcode.url, session=self.session)

            for restaurant in items:  # Request the restaurant url and add items to the online basket
                Request.get(restaurant.url, session=self.session)
                items_checked, payment_url = self.checkout_basket(items, self.session)

            if confirm and payment_url is not None:  # If order is confirm checkout
                self.checkout_payment(url=payment_url, remarks=remarks, user_info=user_info)

            return items_checked, restaurant.name

    def checkout_basket(self, items, session):
        """
        Add items from basket to online basket
        :param items: dictionary of items to add
        :param session: session to use
        :return: list of items checked, url for payment and restaurant name
        """
        BASKET_URL = "/basket.php"

        logging.info("Checking out the basket")
        data = {'action': 'add'}  # Cookie
        url = self.website + self.language + BASKET_URL  # Url of basket

        response = None
        restaurant = None

        for index, restaurant in enumerate(items):
            for category in items[restaurant]:
                data["menucat"] = category.category_id
                for meal in items[restaurant][category]:
                    data["domid"] = meal.dom_id
                    data["product"] = meal.product_id
                    data["rest"] = meal.rest
                    data["productnumber"] = items[restaurant][category][meal]
                    response = Request.post(url, data=data, session=session)

        if response:  # Parse the server last response to check the items in the online basket and get the payment url
            bs_obj = BeautifulSoup(response.text, "html.parser")
            try:
                basket_entry = bs_obj.find('div', {'id': 'products'})
                products = basket_entry.findAll('div', {'class': 'basketentry'})
                payment_url = bs_obj.find('div', {'class': 'basketorderbuttoncontainer'}).find('form')["action"]
            except AttributeError:
                logging.info("AttributeError while checking out for {}".format(restaurant.name))
                raise ScrapperError(1104, restaurant_name=restaurant.name)
            except KeyError:
                website_msg = bs_obj.find('div', {"class": "basketorderbuttoncontainer"}).find('div').get_text()
                raise ScrapperError(1105, website_msg=website_msg)
            else:
                items_checked = list()
                for product in products:
                    # Add product to the items checked list
                    product_quantity = product.find('span', {"class": "basketproductnr"}).get_text()
                    product_name = product.find('div', {"class": "basketproductleft basketproductdesc"}).get_text()
                    items_checked.append([product_name, product_quantity])

                if not items_checked:  # If items checked is empty raise custom_error
                    raise ScrapperError(1104)

            logging.info(items_checked)
            return items_checked, payment_url

        else:  # If no response from server raise custom_error
            raise (BasketError(1102, url=url))

    def checkout_payment(self, url, remarks, user_info):
        SCRIPT_AUTOCOMPLETE_URL = "/scripts/autocomplete/autocomplete.js"

        logging.info("Checking out payment page.")

        data = {'action': 'order',
                'customeradress': '',
                'deliverytime': '',
                'paymentmethod': 0,
                'payswith': '',
                'remarks': remarks,
                'selectpayment': 0,
                'address': user_info.address,
                'email': user_info.email,
                'phonenumber': user_info.phone,
                'postcode': int(user_info.postcode),  # TODO check without int
                'surname': user_info.name,
                'town': user_info.city,
                }

        Request.get(self.website + SCRIPT_AUTOCOMPLETE_URL, session=self.session)
        rep = Request.post(url, session=self.session, data=data)
        bs_obj = BeautifulSoup(rep.text, 'html.parser')

        notification = bs_obj.find("div", {"class": "notificationalert"})

        if notification:
            raise ScrapperError(1105, website_msg=notification.get_text(" "))

        return True


class BasicThread(threading.Thread):
    """
    Thread to download information for a restaurant
    """

    def __init__(self, queue, url):
        super(BasicThread, self).__init__()
        logging.info("Init of ScrapThread")
        self.website = url
        self.queue = queue
        self.session = None
        self.name = None
        self.url = None
        self.r = None

    def run(self):
        """
        Download and parse information from the url of a restaurant. Add them to restaurant[restaurant_name]
        """
        i = 0
        while not self.queue.empty():
            if i != 0:  # Wait two second between each download (don't get ban by server)
                time.sleep(2)
            i = 1
            # Get data from the queue
            self.name, self.url, output, restaurants, self.session = self.queue.get()
            self.r = Restaurant(name=self.name, url=self.url)
            self.r.info = Restaurant_info()
            self.r.open = Restaurant_open()

            try:
                out_msg = self.download()
                output.put([out_msg, self.name])  # Log
                restaurants.append(self.r)

            except ScrapperError as e:
                output.put([e, self.name])

            finally:
                self.queue.task_done()

        logging.info("End of scrap thread")

    def download(self):
        main_page_obj = self.dl_main_page()
        info_page_obj = self.dl_info_page(main_page_obj)

        self.dl_meals(main_page_obj)
        self.dl_ratings(main_page_obj)
        self.dl_delivery_fee(main_page_obj)
        self.dl_minimum_delivery(main_page_obj)
        self.dl_address(info_page_obj)
        self.dl_website(info_page_obj)
        self.dl_description(main_page_obj)
        self.dl_open_hours(info_page_obj)

        return True

    def dl_main_page(self):

        req = Request.get(self.url, session=self.session)
        main_page_obj = BeautifulSoup(req.text, "html.parser")
        return main_page_obj

    def dl_info_page(self, page_obj):
        info_page_obj = page_obj.find('a', {'class': 'restaurantinfotab', 'id': 'infotab_RestaurantInfo'})
        if info_page_obj:
            self.r.info_url = self.website + info_page_obj['href']

            # Request info page
            req = Request.get(self.r.info_url, session=self.session)
            if req.url == self.r.info_url:
                info_page_obj = BeautifulSoup(req.text, 'html.parser')
            else:
                raise ScrapperError(1203, restaurant_name=self.name)
        else:
            raise ScrapperError(1203, restaurant_name=self.name)

        return info_page_obj

    def dl_meals(self, page_obj):

        categories = page_obj.findAll("span", {"class": "menucategorytitle"})  # Find categories
        products = page_obj.findAll("div", {"class": "menucardproducts"})  # Find all meal by category

        if categories == [] or products == []:
            raise ScrapperError(1202, restaurant_name=self.name)
        else:
            for index, category in enumerate(categories):
                c = Category(name=category.text)
                # Scrap Product of the category n° index
                product_list = products[index].findAll('div', {'class': "menucardproduct"})
                category_id = None
                for product in product_list:
                    # Scrap the products
                    product_name = product.find('h3', {'class': 'menucardproductname'})
                    product_id = product.find('input', {'name': 'product'})["value"]
                    category_id = product.find('input', {'name': 'menucat'})["value"]
                    dom_id = product.find('input', {'name': 'domid'})["value"]
                    rest = product.find('input', {'name': 'rest'})["value"]
                    # Regex the price to convert to float and get currency
                    price, currency = self.dl_meals_price(product_name.find('span').text)
                    d = Meal(name=product_name.contents[0].strip(), price=price, product_id=product_id, dom_id=dom_id,
                             rest=rest, currency=currency)
                    c.meal.append(d)

                c.category_id = category_id
                self.r.category.append(c)

    @staticmethod
    def dl_meals_price(text):
        text = text.replace(",", ".")
        return float(text[1:]), text[0]

    def dl_ratings(self, page_obj):
        stars = page_obj.find("div", {"class": "restaurantinfostars"})
        if stars:
            stars_img = stars.find('img')
            if stars_img:
                self.r.info.ratings = int(re.search('\d+', stars_img["alt"]).group())
            else:
                self.r.info.ratings = None

    def dl_delivery_fee(self, page_obj):
        delivery_fee = page_obj.find('div', {"class": "restaurantinfodelivery"})
        if delivery_fee:
            self.r.info.delivery_fee = delivery_fee.find("span").get_text().lower()
        else:
            self.r.info.delivery_fee = None

    def dl_minimum_delivery(self, page_obj):
        delivery_minimum = page_obj.find_all("div", {"class": "restaurantinfominimum"})
        if delivery_minimum[1]:
            self.r.info.minimum_delivery = delivery_minimum[1].find('span').get_text().lower()
        else:
            self.r.info.minimum_delivery = None

    def dl_address(self, page_obj):
        address = page_obj.find('div', {'class': 'moreinfo_address'})
        if address:
            address_street = address.find('span', {'itemprop': 'streetAddress'}).get_text()
            address_locality = address.find('span', {'itemprop': 'addressLocality'}).get_text()
            if address_locality and address_street:
                self.r.info.street = address_street
                self.r.info.city = address_locality
            else:
                self.r.info.street = None
                self.r.info.city = None

    def dl_website(self, page_obj):
        restaurant_website = page_obj.find('div', {'class': 'moreinfo_minisite'})
        if restaurant_website:
            website_url = restaurant_website.find('a')["href"]
            if website_url:
                self.r.info.website = website_url
        else:
            self.r.info.website = None

    def dl_description(self, page_obj):
        description = page_obj.find("div", {"class": "restaurantnotification"})
        if description:
            self.r.info.description = description.get_text()
        else:
            self.r.info.description = None

    def dl_open_hours(self, page_obj):
        open_day = page_obj.find('table', {'class': 'restaurantopentimes'})
        days_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if open_day:
            regex = re.compile('((\d\d):(\d\d))')
            week = open_day.findAll('tr')
            for index, day in enumerate(week):
                hours = regex.findall(day.findAll('td')[1].get_text(" "))
                if len(hours) == 2:
                    exec("self.r.open.{}_am_open = {}".format(days_list[index],
                                                              "datetime.time(int(hours[0][1]), int(hours[0][2]))"))
                    exec("self.r.open.{}_am_close = {}".format(days_list[index],
                                                               "datetime.time(int(hours[1][1]), int(hours[1][2]))"))
                    exec("self.r.open.{}_pm_open = {}".format(days_list[index], "datetime.time.max"))
                    exec("self.r.open.{}_pm_close = {}".format(days_list[index], "datetime.time.max"))
                elif len(hours) == 4:
                    exec("self.r.open.{}_am_open = {}".format(days_list[index],
                                                              "datetime.time(int(hours[0][1]), int(hours[0][2]))"))
                    exec("self.r.open.{}_am_close = {}".format(days_list[index],
                                                               "datetime.time(int(hours[1][1]), int(hours[1][2]))"))
                    exec("self.r.open.{}_pm_open = {}".format(days_list[index],
                                                              "datetime.time(int(hours[2][1]), int(hours[2][2]))"))
                    exec("self.r.open.{}_pm_close = {}".format(days_list[index],
                                                               "datetime.time(int(hours[3][1]), int(hours[3][2]))"))
                else:
                    exec("self.r.open.{}_am_open = {}".format(days_list[index], "datetime.time.max"))
                    exec("self.r.open.{}_am_close = {}".format(days_list[index], "datetime.time.max"))
                    exec("self.r.open.{}_pm_open = {}".format(days_list[index], "datetime.time.max"))
                    exec("self.r.open.{}_pm_close = {}".format(days_list[index], "datetime.time.max"))
