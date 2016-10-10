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
from typing import List, Dict
from bs4 import BeautifulSoup


class ComunioFetcher(object):
    u"""
    A class containing various methods for parsing information from comunio.de
    """

    @staticmethod
    def get_own_player_list(session):
        u"""
        Creates dictionaries modelling the user's current players and returns them
        in a list.

        The format of these dictionaries is:

        name:     The player's name
        value:    The player's current value
        points:   The player's currently accumulated performance points
        position: The player's position

        :param:   The requests session initialized by the ComunioSession
        :return:  A list of the user's players as dictionaries
        """
        player_list = []

        sell_html = session.get(u"http://www.comunio.de/putOnExchangemarket.phtml")
        on_sale_html = session.get(u"http://www.comunio.de/exchangemarket.phtml?takeplayeroff_x=22")
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

    @staticmethod
    def get_today_transfers(screen_name, recent_news):
        u"""
        Fetches the transfer activity for today from comunio's news section. Only fetches
        transfers related to the logged in player

        :param screen_name:   The user's screen name
        :param recent_news:   The recent news as parsed by get_recent_news_articles()
        :return:              A list of transfer dictionaries, consisting of the following attributes:
                                    - name:   the name of the player
                                    - amount: the transfer amount
                                    - type:   "bought" or "sold" to differentiate between the two transfer types
        """
        date = datetime.datetime.utcnow()
        date = unicode(date.day).zfill(2) + u"." + unicode(date.month).zfill(2) + u"." + unicode(date.year)[2:4]

        transfers = []
        for article in recent_news:
            if article[u"type"] == u"Transfers" and article[u"date"] == date:

                transfer_text = article[u"content"]

                while True:
                    player_name, transfer_text = transfer_text.split(u" wechselt für ", 1)
                    amount, transfer_text = transfer_text.split(u" von ", 1)
                    seller_name, transfer_text = transfer_text.split(u" zu ", 1)
                    buyer_name, transfer_text = transfer_text.split(u".", 1)

                    transfer = {u"name": player_name,
                                u"amount": int(amount.replace(u".", u""))}

                    if seller_name == screen_name or buyer_name == screen_name:
                        transfer[u"type"] = u"bought" if buyer_name == screen_name else u"sold"
                        transfers.append(transfer)

                    if len(transfer_text) == 0:
                        break

        return transfers

    @staticmethod
    def get_recent_news_articles(session):
        u"""
        Fetches the most recent news articles for the logged in player

        :param:  The requests session initialized by the ComunioSession
        :return: List of article dictionaries with the following attributes:
                    - date:    The article's date
                    - type:    The type of the article, e.g. 'transfers'
                    - content: The article's content
        """
        html = session.get(u"http://www.comunio.de/team_news.phtml").text
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
