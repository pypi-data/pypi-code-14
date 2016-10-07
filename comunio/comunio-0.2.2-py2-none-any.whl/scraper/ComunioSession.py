u"""
LICENSE:
Copyright 2014 Javier Corbín (MIT License), 2016 Hermann Krumrey

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
import requests
import datetime
from bs4 import BeautifulSoup
from typing import Dict, List


class ComunioSession(object):
    u"""
    The Comunio Web scraping class, which stores the authenticated comunio session
    """

    def __init__(self, username, password):
        u"""
        Constructor that creates the logged in session. If any sort of network or authentication
        error occurs, the session switches into offline mode by unsetting the __connected flag

        :param username:         the user's user name for comunio.de
        :param password:         the user's password
        """
        # We don't store the username and password to avoid having this stored in memory,
        # instead, we use a session to stay logged in

        self.__connected = True
        self.__cash = 0
        self.__team_value = 0
        self.__comunio_id = u""
        self.__player_name = username
        self.__screen_name = username

        self.__session = requests.session()

        # Can raise Exception on wrong credentials, unexpected network state
        # and whenever comunio.de blocks the site for any non-pro users
        try:
            self.__login(username, password)
        except (requests.exceptions.ConnectionError, ConnectionError):
            self.__connected = False

    def __login(self, username, password):
        u"""
        Logs in the user and creates a logged in session object for further queries

        :param username: the user's user name for comunio.de
        :param password: the user's password
        :return:         None
        """
        payload = {u"login": username,
                   u"pass": password,
                   u"action": u'login'}
        
        self.__session.post(u"http://www.comunio.de/login.phtml", data=payload)
        self.__load_info()
  
    def __load_info(self):
        u"""
        Loads the user's most important profile information

        :raises ConnectionError: if the log in process failed
        :return:                 None
        """
        html = self.__session.get(u"http://www.comunio.de/team_news.phtml").text
        soup = BeautifulSoup(html, u"html.parser")

        if soup.find(u"div", {u"id": u"userid"}) is not None:

            self.__cash = int(soup.find(u"div", {u"id": u"manager_money"}).p.text.strip().replace(u".", u"")[12:-2])
            self.__team_value = int(soup.find(u"div", {u"id": u"teamvalue"}).p.text.strip().replace(u".", u"")[17:-2])
            self.__comunio_id = soup.find(u"div", {u"id": u"userid"}).p.text.strip()[6:]

            screen_name_html = self.__session.get(
                u"http://www.comunio.de/playerInfo.phtml?pid=" + self.__comunio_id).text
            screen_name_soup = BeautifulSoup(screen_name_html, u"html.parser")

            self.__player_name = screen_name_soup.find(u"div", {u"id": u"title"}).h1.text
            self.__screen_name = self.__player_name.split(u"\xa0")[0]

        else:
            raise ConnectionError(u"Log In failed, incorrect credentials?")

    def __fetch_recent_news_articles(self):
        u"""
        Fetches the most recent news articles for the logged in player

        :return: List of article dictionaries with the following attributes:
                    - date:    The article's date
                    - type:    The type of the article, e.g. 'transfers'
                    - content: The article's content
        """
        html = self.__session.get(u"http://www.comunio.de/team_news.phtml").text
        soup = BeautifulSoup(html, u"html.parser")

        article_headers = soup.select(u".article_header1") + soup.select(u".article_header2")
        article_content = soup.select(u".article_content1") + soup.select(u".article_content2")

        articles = []

        for index in xrange(0, len(article_headers)):

            header = article_headers[index].text.strip()
            content = article_content[index].text.strip()

            article = {
                u"date": header.split(u" ", 1)[0],
                u"type": header.split(u" > ", 1)[1],
                u"content": content
            }

            articles.append(article)

        return articles

    def is_connected(self):
        u"""
        :return: If the session is connected or not
        """
        return self.__connected

    def get_cash(self):
        u"""
        :return: The player's current amount of liquid assets
        """
        return self.__cash

    def get_team_value(self):
        u"""
        :return: The player's team's current market value on comunio
        """
        return self.__team_value

    def get_screen_name(self):
        u"""
        :return: The Comunio Screen Name
        """
        return self.__screen_name

    def get_own_player_list(self):
        u"""
        Creates dictionaries modelling the user's current players and returns them
        in a list.

        The format of these dictionaries is:

        name:     The player's name
        value:    The player's current value
        points:   The player's currently accumulated performance points
        position: The player's position

        :return:  A list of the user's players as dictionaries
        """
        if not self.__connected:
            return []

        player_list = []

        sell_html = self.__session.get(u"http://www.comunio.de/putOnExchangemarket.phtml")
        on_sale_html = self.__session.get(u"http://www.comunio.de/exchangemarket.phtml?takeplayeroff_x=22")
        soups = (BeautifulSoup(sell_html.text, u"html.parser"), BeautifulSoup(on_sale_html.text, u"html.parser"))

        for i, soup in enumerate(soups):
            players = soup.select(u".tr1") + soup.select(u".tr2")

            for player in players:

                attrs = player.select(u"td")
                if i == 0:
                    player_info = {u"name": attrs[0].text.strip(),
                                   u"value": int(attrs[2].text.strip().replace(u".", u"")),
                                   u"points": int(attrs[3].text.strip()),
                                   u"position": attrs[4].text.strip()}
                elif i == 1:
                    player_info = {u"name": attrs[1].text.strip(),
                                   u"value": int(attrs[4].text.strip().replace(u".", u"")),
                                   u"points": int(attrs[5].text.strip()),
                                   u"position": attrs[7].text.strip()}
                else:
                    player_info = {}
                player_list.append(player_info)

        return player_list

    def get_today_transfers(self):
        u"""
        Fetches the transfer activity for today from comunio's news section. Only fetches
        transfers related to the logged in player

        :return: A list of transfer dictionaries, consisting of the following attributes:
                    - name:   the name of the player
                    - amount: the transfer amount
                    - type:   "bought" or "sold" to differentiate between the two transfer types
        """
        if not self.__connected:
            return []

        date = datetime.datetime.utcnow()
        date = unicode(date.day).zfill(2) + u"." + unicode(date.month).zfill(2) + u"." + unicode(date.year)[2:4]

        transfers = []
        for article in self.__fetch_recent_news_articles():
            if article[u"type"] == u"Transfers" and article[u"date"] == date:

                transfer_text = article[u"content"]

                while True:
                    player_name, transfer_text = transfer_text.split(u" wechselt für ", 1)
                    amount, transfer_text = transfer_text.split(u" von ", 1)
                    seller_name, transfer_text = transfer_text.split(u" zu ", 1)
                    buyer_name, transfer_text = transfer_text.split(u".", 1)

                    transfer = {u"name": player_name,
                                u"amount": int(amount.replace(u".", u""))}

                    if seller_name == self.__screen_name or buyer_name == self.__screen_name:
                        transfer[u"type"] = u"bought" if buyer_name == self.__screen_name else u"sold"
                        transfers.append(transfer)

                    if len(transfer_text) == 0:
                        break

        return transfers
