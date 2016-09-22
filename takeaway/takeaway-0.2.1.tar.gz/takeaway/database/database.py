from .declarative import Base, Postcode, Restaurant, Meal, Category, UserTbl, Restaurant_open
from .error import DatabaseError

from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker

import os.path
import logging
import datetime
import time


class Database:
    def __init__(self, country, postcode, scrapper, interface, path):
        logging.info("Init database")

        # Create database engine
        self.engine = create_engine('sqlite:///{}'.format(os.path.join(path, "takeaway.db")),
                                    connect_args={'check_same_thread': False})
        if not os.path.isfile('{}'.format(os.path.join(path, "takeaway.db"))):  # Create database if doesn't exist
            Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine
        session = sessionmaker(bind=self.engine)
        self.session = session()

        self.postcode = self.set_postcode(country, postcode, scrapper, interface)

        # Search
        self.search_index = 0
        self.all_search = list()  # List of last search terms

    def set_postcode(self, country, postcode, scrapper, interface):
        """
        Query postcode object from database
        :param country: Country of postcode object
        :param postcode: Postcode of postcode object
        :param scrapper: the scrapper for this postcode
        :return: postcode object
        """
        postcode_obj = self.session.query(Postcode).filter(Postcode.postcode == postcode,
                                                           Postcode.country == country).first()
        logging.debug(postcode)
        if postcode_obj is None:
            logging.info("Postcode {} {} not in the database".format(country, postcode))
            interface.print("Searching for {} {}...".format(country, postcode))
            postcode_obj = self.create_postcode(country, postcode, scrapper.get_postcode_url())
        return postcode_obj

    def create_postcode(self, country, postcode, url):
        """
        Create new postcode in database
        :param country: country of postcode object
        :param postcode: postcode of postcode object
        :param url: url of postcode
        :return: postcode object
        """
        postcode_obj = Postcode(postcode=postcode, country=country, url=url)
        self.session.add(postcode_obj)
        self.session.commit()
        return postcode_obj

    def delete_postcode(self, country, postcode):
        """
        Delete postcode and restaurants from database
        :param country country of the postcode to delete
        :param postcode postcode of the postcode to delete
        :return: number of restaurant deleted
        """
        logging.info("Delete postcode {} {} from database".format(country, postcode))

        p = self.session.query(Postcode).filter(Postcode.postcode == postcode,
                                                Postcode.country == country.upper()).first()
        if p:
            number_restaurants = len(p.restaurants)
            for r in p.restaurants:
                if len(r.postcodes) == 1:
                    # if restaurant is associated with only one postcode delete restaurant
                    self.session.delete(r)

            self.session.delete(p)
            self.session.commit()
            return number_restaurants
        else:  # If postcode no in db
            raise DatabaseError(4001, country=country.upper(), postcode=postcode)

    def list_postcode(self, country="all"):
        """
        List the postcodes in the database
        :param country: Query of the postcode to list. Default is all
        :return: list of postcode object
        """
        if country == "all":
            p = self.session.query(Postcode).all()
        else:
            p = self.session.query(Postcode).filter(Postcode.country == country.upper()).all()

        return p

    def update_database(self, new_restaurants, interface):
        """
        Make or update all the database for the postcode

        We need to delete all the restaurant when making the database to be sure some restaurants didn't stop delivering
        :param new_restaurants: updated restaurants
        :return:
        """
        logging.info("Saving {} restaurant to databases".format(len(new_restaurants)))
        bar = interface.progress_bar(len(new_restaurants))
        for index, restaurant in enumerate(new_restaurants):  # Add the new restaurants
            self.add_restaurant(restaurant)
            interface.update_progress_bar(bar, index + 1)  # First index = 0
        interface.end_progress_bar(bar)
        time.sleep(0.2)
        return len(new_restaurants)

    def add_restaurant(self, restaurant):
        """
        Add restaurants to the database
        :param restaurant: list of restaurant object to add to database
        :return: True
        """
        logging.info(restaurant)
        restaurant_db, _ = self.search(restaurant_searches=True,
                                       url=restaurant.url)  # Check if restaurant exist in the database
        if restaurant_db:  # If exist we delete, update and add all the postcodes back
            logging.debug("restaurant_db is true")
            # search_restaurant return a list of 1 item (url is unique)
            postcodes = self.delete_restaurant(restaurant_db[0])
            logging.debug(postcodes)
            for postcode in postcodes:
                restaurant.postcodes.append(postcode)
            if self.postcode not in restaurant.postcodes:  # We check if the current postcode is in (don't want double)
                restaurant.postcodes.append(self.postcode)
            self.session.add(restaurant)
        else:  # if not in db we create a new one
            restaurant.postcodes.append(self.postcode)
            self.session.add(restaurant)
        restaurant.updated = datetime.datetime.now()
        self.session.commit()
        return True

    def delete_restaurant(self, restaurant):
        """
        Delete the restaurant
        :param restaurant: restaurant obj to delete
        :return:
        """
        logging.info(restaurant)
        postcodes = list(restaurant.postcodes)  # Copy the postcodes of the restaurant
        self.session.delete(restaurant)
        self.session.commit()
        return postcodes

    def search_time(self, query):
        current_day = datetime.datetime.now().strftime('%A').lower()
        current_time = datetime.datetime.now().time()

        query = query.join(Restaurant_open).filter(or_(
            and_(eval("Restaurant_open.{}_am_open".format(current_day)) < current_time,
                 eval("Restaurant_open.{}_am_close".format(current_day)) > current_time),
            and_(eval("Restaurant_open.{}_pm_open".format(current_day)) < current_time,
                 eval("Restaurant_open.{}_pm_close".format(current_day)) > current_time)))

        return query

    def search_restaurant(self, restaurant_searches=True, updated=None, url=None):
        """
        Search for restaurants in the database by search term or by update older than a date
        :param restaurant_searches: list of search term or True for all
        :param updated: select restaurant with a inferior date in the updated column
        :param url: url to search in db
        :return: list of restaurants
        """
        logging.info("search: {}, updated {}, url {}".format(restaurant_searches, updated, url))
        q = self.session.query(Restaurant).filter(Restaurant.postcodes.contains(self.postcode))

        if restaurant_searches is True:
            # Search all the restaurant
            if updated:
                # Search restaurant.updated older than date
                q = q.filter(Restaurant.updated < updated)
                logging.debug(q)
            elif url:
                q = self.session.query(Restaurant).filter(Restaurant.url == url)
        else:
            # Search by all the terms in restaurant_searches
            q = q.filter(or_(Restaurant.name.like('%{}%'.format(s)) for s in restaurant_searches))

        return q

    def search_category(self, category_searches):
        """
        Search for category in the database
        :param category_searches: list of search term
        :return: list of category
        """
        q = self.session.query(Category).join(Category.restaurant).filter(Restaurant.postcodes.contains(self.postcode))
        if category_searches is not True:
            q = q.filter(or_(Category.name.like('%{}%'.format(s)) for s in category_searches))

        return q

    def search_meal(self, meal_searches):
        """
        Search for meal in the database
        :param meal_searches: list of search term
        :return: list of meal
        """
        q = self.session.query(Meal).join(Meal.category, Category.restaurant).filter(
            Restaurant.postcodes.contains(self.postcode))
        if meal_searches is not True:
            q = q.filter(or_(Meal.name.like('%{}%'.format(s)) for s in meal_searches))

        return q

    def search_meal_category(self, meal_searches, category_searches):
        """
        Search for a meal in a category
        :param meal_searches: list of search term
        :param category_searches: list of search term
        :return: list of meal
        """
        if category_searches is True:
            q = self.search_meal(meal_searches)
        else:
            q = self.session.query(Meal).join(Meal.category, Category.restaurant).filter(
                Restaurant.postcodes.contains(self.postcode))

            if meal_searches is True:
                q = q.filter(or_(Category.name.like('%{}%'.format(s)) for s in category_searches))
            else:
                q = q.filter(or_(Category.name.like('%{}%'.format(s)) for s in category_searches)).filter(
                    or_(Meal.name.like('%{}%'.format(s)) for s in meal_searches))

        return q

    def search_meal_restaurant(self, meal_searches, restaurant_searches):
        """
        Search for a meal in a restaurant
        :param meal_searches: list of search term
        :param restaurant_searches: list of search term
        :return: list of meal
        """

        if restaurant_searches is True:
            q = self.search_meal(meal_searches)
        else:
            q = self.session.query(Meal).join(Meal.category, Category.restaurant).filter(
                Restaurant.postcodes.contains(self.postcode))
            if meal_searches is True:
                q = q.filter(or_(Restaurant.name.like('%{}%'.format(s)) for s in restaurant_searches))
            else:
                q = q.filter(or_(Restaurant.name.like('%{}%'.format(s)) for s in restaurant_searches)).filter(
                    or_(Meal.name.like('%{}%'.format(s)) for s in meal_searches))
        return q

    def search_category_restaurant(self, category_searches, restaurant_searches, rep_type="category"):
        """
        Search for a category in a restaurant
        :param category_searches: list of search term
        :param restaurant_searches: list of search term
        :param rep_type: type of the response. List of category object or meal object
        :return: list of category
        """
        if rep_type == "meal":
            q = self.session.query(Meal).join(Meal.category, Category.restaurant).filter(
                Restaurant.postcodes.contains(self.postcode))
        else:
            q = self.session.query(Category).join(Category.restaurant).filter(
                Restaurant.postcodes.contains(self.postcode))

        if restaurant_searches is True:
            q = self.search_category(category_searches)
        elif category_searches is True:
            q = q.filter(or_(Restaurant.name.like('%{}%'.format(s)) for s in restaurant_searches))
        else:
            q = q.filter(or_(Restaurant.name.like('%{}%'.format(s)) for s in restaurant_searches)).filter(
                or_(Category.name.like("%{}%".format(s)) for s in category_searches))

        return q

    def search_all(self, meal_searches, category_searches, restaurant_searches):

        q = self.session.query(Meal).join(Meal.category, Category.restaurant).filter(
            Restaurant.postcodes.contains(self.postcode)).filter(
            or_(Restaurant.name.like('%{}%'.format(s)) for s in restaurant_searches)).filter(
            or_(Category.name.like('%{}%'.format(s)) for s in category_searches)).filter(
            or_(Meal.name.like('%{}%'.format(s)) for s in meal_searches))

        return q

    def search(self, meal_searches=False, category_searches=False, restaurant_searches=False, searchtime=False,
               updated=None,
               url=None):
        """
        Search for a meal and/or category and/or restaurant in the database
        :param meal_searches: list of search term
        :param category_searches: list of search term
        :param restaurant_searches: list of search term
        :param searchtime: return only open restaurant
        :param updated: Search restaurant updated older than updated (Date obj)
        :param url: Search restaurant by url
        :return: list of items (meal/category or restaurant)
        """
        logging.info("Search database, meal: {}, category: {}, restaurant: {}".format(meal_searches, category_searches,
                                                                                      restaurant_searches))
        if meal_searches and category_searches and restaurant_searches:
            if meal_searches is True and category_searches is True and restaurant_searches is True:
                q = self.search_meal(meal_searches)
                rep_type = "meal"
            elif restaurant_searches is True and category_searches is True:
                q = self.search_meal(meal_searches)
                rep_type = "meal"
            elif restaurant_searches is True and meal_searches is True:
                q = self.search_meal_category(meal_searches, category_searches)
                rep_type = "meal"
            elif meal_searches is True and category_searches is True:
                q = self.search_restaurant(restaurant_searches)
                rep_type = "meal"
            elif restaurant_searches is True:
                q = self.search_meal_category(meal_searches, category_searches)
                rep_type = "meal"
            elif category_searches is True:
                q = self.search_meal_restaurant(meal_searches, restaurant_searches)
                rep_type = "meal"
            elif meal_searches is True:
                q = self.search_category_restaurant(category_searches, restaurant_searches, rep_type="meal")
                rep_type = "meal"
            else:
                q = self.search_all(meal_searches, category_searches, restaurant_searches)
                rep_type = "meal"
        elif category_searches and restaurant_searches:
            q = self.search_category_restaurant(category_searches, restaurant_searches, rep_type="category")
            rep_type = "category"
        elif meal_searches and restaurant_searches:
            q = self.search_meal_restaurant(meal_searches, restaurant_searches)
            rep_type = "meal"
        elif meal_searches and category_searches:
            q = self.search_meal_category(meal_searches, category_searches)
            rep_type = "meal"
        elif meal_searches:
            q = self.search_meal(meal_searches)
            rep_type = "meal"
        elif category_searches:
            q = self.search_category(category_searches)
            rep_type = "category"
        elif restaurant_searches:
            q = self.search_restaurant(restaurant_searches, url=url, updated=updated)
            rep_type = "restaurant"
        else:
            raise DatabaseError(4000)

        if searchtime:
            q = self.search_time(q)

        rep = q.all()
        if rep_type == "meal":  # If meal we add them to the search list and give them an index
            self.all_search += rep
            for meal in rep:
                meal.index = self.search_index
                self.search_index += 1

        return rep, rep_type

    def get_users(self):
        """
        Get all the users in the database
        :return: list of users
        """
        return self.session.query(UserTbl).all()

    def get_user(self, username, error=True):
        """
        Get an user from the database
        :param username: username of the user
        :param error: raise an custom_error if user not in database
        :return: user object
        """
        logging.info("Get user {} from database".format(username))
        user = self.session.query(UserTbl).filter(UserTbl.username == username).first()
        if not user and error:
            raise DatabaseError(4002, username=username)
        elif not user:
            return False

        return user

    def create_user(self, username, info):
        """
        Create or modify an user in the database
        :param username: username of user
        :param info: dict of information about the user
        :return: user object
        """
        logging.info("Create user {} in database".format(username))
        user = self.get_user(username, error=False)
        if not user:
            # If user not in database create new
            user = UserTbl(username=username)

        user.name = info.get("Name")
        user.email = info.get("Email")
        user.phone = info.get("Phone")
        user.postcode = info.get("Postcode")
        user.city = info.get("City")
        user.address = info.get("Address")

        if username != "anonymous":
            logging.debug("Save user in database")
            self.session.add(user)
            self.session.commit()

        return user

    def delete_user(self, username):
        """
        Delete user from database
        :param username: username of user to delete
        :return: True
        """
        logging.info("Delete user {} from database".format(username))
        q = self.session.query(UserTbl).filter(UserTbl.username == username).delete()
        if q == 0:
            raise DatabaseError(4002, username=username)

        self.session.commit()
        return True
