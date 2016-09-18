from .error import UserError

import logging


class User:
    def __init__(self, database, interface):
        logging.info("Init User")
        self.database = database
        self.interface = interface
        self.user = None

    def load_unload_user(self, username):
        """
        Load or unload user
        :param username: username of user or true to unload
        """
        if username is True:
            logging.info("Unload user {}".format(username))
            # If no username we unload user or return false if nothing to unload
            if self.user:
                self.user = None
                return True
            else:
                return False
        else:
            logging.info("Load user {}".format(username))
            # If username we load user from database based on username
            username = username.lower()
            self.user = self.database.get_user(username)
            return True

    def create_user(self, username="anonymous", info=None):
        """
        Create or modify user.
        If no user specify for checkout create an anonymous user. Call get_user_info to request info from user
        :param username: username of user
        :param info: information about the user
        :return: username of user
        """
        logging.info("Creating user {}".format(username))
        username = username.lower()  # username always lower
        if username == "anonymous":
            self.interface.print("In order to continue with your order some information are needed.")
            if info is None:
                info = self.get_user_info()
        else:
            user = self.database.get_user(username, error=False)
            if user:  # Check if user in database
                logging.debug(user)
                self.interface.print("In order to modify user {} some information are needed.".format(user.id_name))
            else:
                self.interface.print("In order to create user {} some information are needed.".format(username))
            if info is None:
                info = self.get_user_info(user=user)  # Get new user information from user

        user = self.database.create_user(username, info)  # Create user in database

        return user

    def get_user_info(self, user=None):
        """
        Get information from user. Called by create_user
        :param user: user object if we are modifying an user
        :return:
        """
        info_list = ["Name", "City", "Postcode", "Address", "Phone", "Email"]
        info = {"Name": "", "Email": "", "Phone": "", "Postcode": "", "City": "", "Address": ""}
        for entry in info_list:
            if user:
                previous = eval("user.{}".format(entry.lower()))
                user_input = self.interface.input("{} ({}): ".format(entry, previous))
                if user_input == "":
                    user_input = previous
            else:
                user_input = self.interface.input("{}: ".format(entry))
            info[entry] = user_input

        return info

    def list_users(self):
        return self.database.get_user()

    def delete_user(self, username):
        if username is True:
            if self.user:
                logging.info("Deleting user {}".format(self.user.username))
                self.database.delete_user(self.user.username)
                self.user = None
                return self.user.username
            else:
                raise UserError(3001)
        elif username:
            logging.info("Deleting user {}".format(username))
            self.database.delete_user(username)
            return username
