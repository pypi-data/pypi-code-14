u"""
LICENSE:
Copyright 2016 Hermann Krumrey

This file is part of comunio-manager.

    comunio-manager is a program that allows a user to track his/her comunio.de
    profile

    comunio-manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    comunio-manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with comunio-manager.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""


# imports
from __future__ import absolute_import
import sys
from comunio.ui.dialogs.login import Ui_LoginDialog
from comunio.scraper.ComunioSession import ComunioSession
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from comunio.credentials.CredentialsManager import CredentialsManager


class LoginScreen(QDialog, Ui_LoginDialog):
    u"""
    The Login Dialogue that allows the user to log in.
    """

    def __init__(self, credentials):
        u"""
        Initializes a new Login Dialog with a configurable default username and password

        :param credentials: The CredentialsManager holding the default username and password
        """
        super(LoginScreen, self).__init__()
        self.setupUi(self)

        self.comunio_session = None
        self.credentials = credentials

        self.username_field.setText(credentials.get_credentials()[0])
        self.password_field.setText(credentials.get_credentials()[1])
        self.cancel_button.clicked.connect(self.close)
        self.login_button.clicked.connect(self.login)

    def get_comunio_session(self):
        u"""
        :return: the internal comunio session after a login.
        """
        return self.comunio_session

    def login(self):
        u"""
        Tries to Log in the user, and handles failures by showing message dialogs

        :return: None
        """
        try:
            username = self.username_field.text()
            password = self.password_field.text()

            self.comunio_session = ComunioSession(username, password)
            if self.remember_check.checkState():
                self.credentials.set_credentials((username, password))
                self.credentials.store_credentials()
            self.accept()
        except ConnectionError:
            self.show_error_dialog(u"Login Failed", u"Network Error", u"The Comunio Servers could not be reached. "
                                                                    u"Check if your internet connection is working.")
        except PermissionError:
            self.show_error_dialog(u"Login Failed", u"Authentication Error", u"Your credentials were not accepted by the "
                                                                           u"Comunio servers. This may be due to a bad "
                                                                           u"username/password combination, or due to "
                                                                           u"the Comunio servers currently only "
                                                                           u"allowing logins from Pro players")
        except ReferenceError:
            self.show_error_dialog(u"Login Failed", u"5 players on transfer list", u"Your comunio information could not "
                                                                                 u"be loaded due to 5 players being on "
                                                                                 u"the transfer list currently. Remove "
                                                                                 u"a player from the transfer list to "
                                                                                 u"log in.")

    @staticmethod
    def show_error_dialog(title, message, secondary_text):
        u"""
        Shows an error Dialog

        :param title:          The title of the dialog
        :param message:        The primary message of the dialog
        :param secondary_text: The secondary message of the dialog
        :return:               None
        """

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setInformativeText(secondary_text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


def start(credentials):
    u"""
    Starts the Login Dialog

    :param credentials: the credentials to be used on startup
    :return:            a logged in comunio session
    """

    app =QApplication(sys.argv)
    form = LoginScreen(credentials)
    return form.get_comunio_session() if form.exec_() else None
