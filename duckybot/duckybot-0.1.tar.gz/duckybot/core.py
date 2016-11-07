# Copyright: 2016, Vasilii V. Bodnariuk
# Author: Vasilii V. Bodnariuk (http://vasilesk.ru)
# License: MIT
"""
The core of duckybot package: the Duckybot class.
"""

__all__ = ('Duckybot',)


from .system import sns, dbms, existent, files

# import importlib
# importlib.import_module('configparsing', '.system')

class Duckybot:
    def __init__(self):
        """
        Create Duckybot instance.
        """

        self.existent = False
        self.files = files.Files

    def connect_db(self, dbms_name, dict_config):
        """
        Establish db connection.

        :param dbms_name: Database Management System name (see system.dbms.available)
        :param dict_config: dictionary containing data for connection
        """

    def install(self):
        """
        Install duckybot scheme into db.
        Should be used only once.
        Requires db connection to be established (`see self.connect_db()`).
        """

    def uninstall(self):
        """
        Drop duckybot scheme in db.
        Requires db connection to be established (`see self.connect_db()`).
        """

    def create_new(self, codename, sns_name):
        """
        Create a new bot record in db.
        To operate this bot after creation one should call `self.operate_existent()` method.
        Requires db connection to be established (`see self.connect_db()`).

        :param codename: new bot codename
        :param sns_name: new bot social networking service name (see system.sns.available)
        """
        sns.Twitter()

    def delete_existent(self, codename):
        """
        Delete the bot from db.
        Requires db connection to be established (`see self.connect_db()`).

        :param codename: bot codename
        """

    def operate_existent(self, codename, auto_delay=False):
        """
        Operate bot that exists in db.
        Requires db connection to be established (`see self.connect_db()`).
        Makes `self.bot` methods available for usage

        :param codename: existent bot codename
        :param auto_delay: if True the bot will sleep to prevent sns api limiting errors
        """
        self.bot = existent.Existent(codename=codename)

    def update_existent(self, dict_update):
        """
        Update existent bot info.
        Requires existent bot codename to be established (`see self.operate_existent()`).

        :param dict_update: dictionary with info to update
        """
