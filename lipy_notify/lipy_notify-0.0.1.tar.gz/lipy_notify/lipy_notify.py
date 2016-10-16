# -*- coding: utf-8 -*-
import sys
import requests
import json
from xml.etree import ElementTree as ET


class LipyNotify(object):

    def __init__(self):
        self.url = "https://notify-api.line.me/api/notify"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.token = None

    def set_token(self, token):
        self.token = token
        self.headers["Authorization"] = "Bearer " + token

    def send_txt(self, message):
        if self.token is None:
            sys.stderr.write(
                "Message can't be sent. You must set your authorization token with set_token method")
        else:
            payload = {"message": message}
            resp = requests.post(self.url, data=payload, headers=self.headers)

    def send_image(self, message, image_url):
        if self.token is None:
            sys.stderr.write(
                "Message can't be sent. You must set your authorization token with set_token method")
        else:
            payload = {
                "message": message,
                "imageThumbnail": image_url,
                "imageFullsize": image_url}
            resp = requests.post(self.url, data=payload, headers=self.headers)
            self._validate_response(resp)

    def send_cat_image(self):
        api_url = "http://thecatapi.com/api/images/get"
        params = {
            "type": "jpg",
            "size": "med",
            "format": "xml"
        }
        r = requests.get(api_url, params=params)
        tree = ET.fromstring(r.text)
        image_url = tree.findall(".//url")[0].text

        self.send_image(message="にゃーん", image_url=image_url)

    def _validate_response(self, resp):
        resp = resp.json()
        if resp["status"] == 200:
            sys.stderr.write("Message sent successfully")
        else:
            sys.stderr.write("Message was not sent properly")
