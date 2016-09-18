from .error import BasketError

import logging


class Basket:

    def __init__(self, url, database):
        self.total = 0
        self.items = dict()
        self.database = database
        self.url = url + "/basket.php"
        logging.info("Init of basket. url: {}".format(self.url))

    def add(self, items_indexes):
        """
        Add an item to the basket
        :param items_indexes: index of search_items items to add
        :return: True
        """
        for item_index in items_indexes:  # For each item
            try:  # if index in the search items index
                item = self.database.all_search[item_index]
            except IndexError:
                raise BasketError(2002)

            # Add the items in the dictionary and add the number
            logging.info("Add item {} to basket".format(item.name))
            if item.category.restaurant not in self.items:
                self.items[item.category.restaurant] = dict()
                self.items[item.category.restaurant][item.category] = dict()
                self.items[item.category.restaurant][item.category][item] = 1
            elif item.category not in self.items[item.category.restaurant]:
                self.items[item.category.restaurant][item.category] = dict()
                self.items[item.category.restaurant][item.category][item] = 1
            elif item not in self.items[item.category.restaurant][item.category]:
                self.items[item.category.restaurant][item.category][item] = 1
            else:
                self.items[item.category.restaurant][item.category][item] += 1

            self.total += item.price

        return len(items_indexes)

    def delete(self, items_indexes):
        """
        Delete an item from the basket
        :param items_indexes: index of search_items items to delete from basket
        :return: True
        """
        for item_index in items_indexes:  # for each item
            try:
                item = self.database.all_search[item_index]  # if index in the current search
            except IndexError:
                raise BasketError(2002)

            # Delete item from the dictionary or decrement by 1
            logging.info("Delete item {} from basket.".format(item.name))
            try:
                self.items[item.category.restaurant][item.category][item] -= 1
                if self.items[item.category.restaurant][item.category][item] < 1:
                    self.items[item.category.restaurant][item.category].pop(item)
                    if len(self.items[item.category.restaurant][item.category]) == 0:
                        self.items[item.category.restaurant].pop(item.category)
                        if len(self.items[item.category.restaurant]) == 0:
                            self.items.pop(item.category.restaurant)
            except KeyError:
                raise BasketError(2001, meal=item.name)

            self.total -= item.price

        return len(items_indexes)

    def delete_all(self):
        """
        Empty the basket
        :return: True
        """
        logging.info("Clear items in basket")
        if len(self.items) != 0:
            self.items = dict()
            return True
        else:
            return False
