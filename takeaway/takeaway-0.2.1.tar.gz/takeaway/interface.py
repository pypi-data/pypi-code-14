import sys
import datetime
import re
import logging

from progressbar import ProgressBar
from prettytable import PrettyTable, ALL


class Print:
    """
    Print information to stdout
    """

    def __init__(self, country, postcode, takeaway=None):
        self.postcode = postcode.upper()
        self.country = country.upper()
        self.encoding = sys.stdout.encoding
        if takeaway:
            self.takeaway = takeaway
        else:
            self.takeaway = None

    def add_takeaway(self, takeaway):
        self.takeaway = takeaway

    def error(self, e):
        """
        Display error
        :param e: error
        """
        self.print("Error: {}".format(e))

    def custom_error(self, e):
        """
        Display custom_error
        :param e: custom_error
        """
        self.print("Error {}: {}".format(e, e.code[e.args[0]]))

    def db_delete(self, number_restaurant, country, postcode):
        self.print(
            "{} restaurants successfully deleted for {} {}.".format(number_restaurant, country.upper(), postcode))

    def db_make(self, rep):
        self.print("Database successfully created for {} {}".format(self.country, self.postcode), ok=rep,
                   msg_false="Error while creating database for {} {}".format(self.country, self.postcode))

    def db_update(self, rep):
        self.print("Database successfully updated for {} {}".format(self.country, self.postcode), ok=rep,
                   msg_false="No restaurant to update for {} {}".format(self.country, self.postcode))

    def db_consolidate(self, rep):
        self.print("Database successfully consolidated for {} {}.".format(self.country, self.postcode), ok=rep,
                   msg_false="All restaurants already in database.")

    def db_list(self, data):
        if data:
            for postcode in data:
                self.print("-  {} {} with {} saved restaurants.".format(postcode.country, postcode.postcode,
                                                                        len(postcode.restaurants)))
        else:
            self.print("No postcode found in the database.")

    def print_restaurant(self, restaurants, verbose_level):
        table = PrettyTable()
        current_day = datetime.datetime.now().strftime('%A').lower()
        current_time = datetime.datetime.now().time()
        is_open_list = ["restaurant.open.{}_am_open".format(current_day),
                        "restaurant.open.{}_am_close".format(current_day),
                        "restaurant.open.{}_pm_open".format(current_day),
                        "restaurant.open.{}_pm_close".format(current_day)]

        if verbose_level == 2:
            table.field_names = ["Name", "Ratings", "Delivery", "Minimum", "Categories", "Open"]
            table.align = "r"
            table.align["Name"] = "l"
            for restaurant in restaurants:
                if eval(is_open_list[0]) < current_time < eval(is_open_list[1]) or eval(
                        is_open_list[2]) < current_time < eval(is_open_list[3]):
                    is_open = "Yes"
                else:
                    is_open = "No"
                table.add_row([restaurant.name, restaurant.info.ratings, restaurant.info.delivery_fee,
                               restaurant.info.minimum_delivery, len(restaurant.category), is_open])
        elif verbose_level == 3:
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            table.field_names = ["Name", "Ratings", "Delivery", "Minimum", "Categories"] + days
            table.align = "r"
            table.align["Name"] = "l"
            table.hrules = ALL
            for restaurant in restaurants:
                open_list = list()
                for day in days:
                    am_open = eval("restaurant.open.{}_am_open".format(day.lower()))
                    am_close = eval("restaurant.open.{}_am_close".format(day.lower()))
                    pm_open = eval("restaurant.open.{}_pm_open".format(day.lower()))
                    pm_close = eval("restaurant.open.{}_pm_close".format(day.lower()))
                    if am_open == datetime.time.max:
                        open_list.append("/////////////")
                    else:
                        if pm_open == datetime.time.max:
                            open_list.append("{} - {}".format(am_open.strftime("%H:%M"), am_close.strftime('%H:%M')))
                        else:
                            open_list.append(
                                "{} - {}\n{} - {}".format(am_open.strftime("%H:%M"), am_close.strftime('%H:%M'),
                                                          pm_open.strftime("%H:%M"), pm_close.strftime('%H:%M')))
                table.add_row([restaurant.name, restaurant.info.ratings, restaurant.info.delivery_fee,
                               restaurant.info.minimum_delivery, len(restaurant.category)] + open_list)
        else:
            table.field_names = ["Name", "Ratings", "Open"]
            table.align = "r"
            table.align["Name"] = "l"
            for restaurant in restaurants:
                if eval(is_open_list[0]) < current_time < eval(is_open_list[1]) or eval(
                        is_open_list[2]) < current_time < eval(is_open_list[3]):
                    is_open = "Yes"
                else:
                    is_open = "No"
                table.add_row([restaurant.name, restaurant.info.ratings, is_open])

        self.print(table.get_string(sortby="Name"))

    def print_category(self, data):
        table = PrettyTable()
        table.field_names = ["Restaurant", "Category", "Meals"]
        table.align['Restaurant'] = "l"
        table.align["Category"] = "l"
        table.align["Meals"] = "r"
        for category in data:
            table.add_row([category.restaurant.name, category.name, len(category.meal)])
        self.print(table.get_string(sortby="Restaurant"))

    def print_meal(self, data):
        table = PrettyTable()
        table.field_names = ["Index", "Restaurant", "Category", "Meal", "Price"]
        table.align = "l"
        table.align["Price"] = "r"
        table.align["Index"] = "c"
        for meal in data:
            table.add_row([meal.index, meal.category.restaurant.name, meal.category.name, meal.name, meal.price])
        self.print(table.get_string(sortby="Index"))

    def print_basket(self, basket_items):
        table = PrettyTable()
        table.field_names = ["Index", "Name", "Price", "N°", "Restaurant"]
        table.align = "r"
        table.align["Name"] = "l"
        table.align["Restaurant"] = "l"
        table.align['Index'] = "c"
        for restaurant in basket_items:
            for category in basket_items[restaurant]:
                for meal in basket_items[restaurant][category]:
                    table.add_row(
                        [meal.index, meal.name, meal.price, basket_items[restaurant][category][meal], restaurant.name])
        self.print(table.get_string(sortby="Index"))

    def checkout(self, args_list):
        confirm, items, restaurant_name, price_total, address = args_list

        if confirm:
            self.print("Your order to {} was successful.".format(restaurant_name))
            for item in items:
                self.print("-  {}: {}".format(item[0], item[1]))
            self.print('Total: {}'.format(price_total))
            self.print('Delivery to: {}'.format(address))
        else:
            self.print("Test checkout !")
            for item in items:
                self.print("-  {}: {}".format(item[0], item[1]))
            self.print('Total: {}'.format(price_total))
            self.print('Delivery to: {}'.format(address))

    def list_users(self, users):
        info = ("Name", "Email", "Phone", "Postcode", "City", "Address")
        if users == list():
            self.print("No user found in the database.")
        else:
            for user in users:
                self.print("* {}".format(user.username.upper()))
                for entry in info:
                    self.print(" - {}: {}".format(entry, eval("user.{}".format(entry.lower()))))

            if len(users) == 1:
                self.print("\n1 user found in the database")
            else:
                self.print("\n{} users found in the database".format(len(users)))

    def create_user(self, user):
        self.print("User {} successfully saved.".format(user.username))

    def delete_user(self, id_name):
        self.print("User {} successfully deleted.".format(id_name))

    def load_unload_user(self, rep):
        if not rep:
            self.print("Pass an username to load it.")

    def add_basket(self, number_of_items):
        if number_of_items == 1:
            self.print("1 item added to the basket.")
        else:
            self.print("{} items added to the basket".format(number_of_items))

    def del_basket(self, number_of_items):
        if number_of_items == 1:
            self.print("1 item deleted from the basket.")
        else:
            self.print("{} items delete from the basket".format(number_of_items))

    def clear_basket(self, rep):
        self.print("The basket is now empty.", ok=rep, msg_false="Basket already empty.")

    def progress_bar(self, length):
        bar = ProgressBar(max_value=length)
        bar.start()
        return bar

    def update_progress_bar(self, bar, value):
        bar.update(value)

    def end_progress_bar(self, bar):
        bar.finish()

    def print(self, msg_ok, ok=True, end='\n', sep='', msg_false=""):
        if ok:
            print(msg_ok.encode(self.encoding, errors="replace").decode(self.encoding), end=end, sep=sep)
        else:
            print(msg_false.encode(self.encoding, errors="replace").decode(self.encoding), end=end, sep=sep)

    def input(self, msg):
        data = input(msg.encode(self.encoding, errors="replace").decode(self.encoding))
        return data

    def run(self):
        while True:
            self.takeaway.command(user_input=self.get_user_input())

    def get_user_input(self):
        """
        Request commands input from user (interactive mode)
        :return: list of string from user input
        """
        user_input_basket = ""  # Basket info to display
        user_input_user = ""  # User info to display
        user_input_postcode = "Postcode: {} {}\n".format(self.takeaway.database.postcode.country,
                                                         self.takeaway.database.postcode.postcode)
        if self.takeaway.basket.total:  # If total is not 0
            user_input_basket = "Total: {} euros\n".format(self.takeaway.basket.total)
        if self.takeaway.user.user:  # If a user is loaded
            user_input_user = "User: {}\n".format(self.takeaway.user.user.username.title())

        u_input_raw = self.input(
            "\n{}{}{}(-i to quit) Command: ".format(user_input_user, user_input_postcode, user_input_basket))

        # Clean user input to be parse with argparse
        logging.debug("Raw user input: {}".format(u_input_raw))
        u_input_raw = re.findall('\'[^\']*\'|\"[^\"]*\"|\S+', u_input_raw)  # Split the string (keep bracket together)
        # Clean string (add country/postcode as first args)
        u_input = [self.takeaway.database.postcode.country, self.takeaway.database.postcode.postcode]
        for string in u_input_raw:
            string = string.replace('"', "").replace("'", "")  # Delete " and ' from raw string
            u_input.append(string)  # Add clean string to u_input
        logging.debug("Clean user input: {}".format(u_input))

        return u_input  # Output clean reformatted string
