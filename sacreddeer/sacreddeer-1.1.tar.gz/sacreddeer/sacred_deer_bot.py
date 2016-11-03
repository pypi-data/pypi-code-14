#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random

from sacreddeer import base


class SacredDeer(base.Bot):
    def prepare_response(self, cmd):
        responses = {
            'en': [
                u"Yes",
                u"No",
                u"It doesn't matter",
                u"Chill, bro",
                u"Ha-ha, very funny",
                u"Yes, but shouldn't",
                u"Never",
                u"100%",
                u"1 of 100",
                u"Try again"
            ],
            'ru': [
                u"Да",
                u"Нет",
                u"Это не важно",
                u"Спок, бро",
                u"Толсто",
                u"Да, хотя зря",
                u"Никогда",
                u"100%",
                u"1 из 100",
                u"Еще разок"
            ],
            'ua': [
                u"Так",
                u"Ні",
                u"Немає значення",
                u"Не сци, козаче",
                u"Товсто",
                u"Так, хоча даремно",
                u"Ніколи",
                u"100%",
                u"1 із 100",
                u"Спробуй ще"
            ],
            'de': [
                u"Ja",
                u"Nein",
                u"Das ist nicht jebachtung",
                u"Uspokojten, Bruder",
                u"Tolstische",
                u"Ja, aber Dolbojobist",
                u"Nie",
                u"100%",
                u"1 von 100",
                u"Poprobiren es noch einmal"
            ]
        }
        lang = cmd[:2] if len(cmd) >= 2 else 'ru'
        responses_list = responses.get(lang) or responses['ru']
        return random.choice(responses_list)


if __name__ == "__main__":
    bot = SacredDeer('sacred_deer', os.environ.get('TOKEN'), 'Sacred Deer')
    bot.run()
