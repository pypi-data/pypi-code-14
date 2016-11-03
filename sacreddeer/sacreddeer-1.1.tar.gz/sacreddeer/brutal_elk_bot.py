#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random

from sacreddeer import base


class BrutalElk(base.Bot):
    def prepare_response(self, cmd):
        responses_list = [
            u"Say hello to my little friend",
            u"Yippee ki-yay, motherfucker!",
            u"No women no kids",
            u"Dead or alive, you're coming with me",
            u"Hasta la vista, baby",
            u"Если голова болит, значит она есть",
            u"Ошибки учатся на мне",
            u"Заплатил налоги и сплю спокойно на лавочках, в подвалах, на"
            u"вокзале",
            u"Никакое моральное удовлетворение не может сравниться с"
            u"аморальным",
            u"Можно поподробнее? Чтобы не вникать",
            u"Вскружил девушке голову так, что её тошнило 9 месяцев",
            u"Если некоторых людей смешать с дерьмом, то получится однородная"
            u"масса",
            u"Больной пошёл на поправку. Но не дошёл...",
            u"Кажется, у вас повысился градус неадеквата",
            u"O RLY?",
            u"WAT",
            u"OH SHI--",
            u"You gonna get raped",
            u"This is SPARTAAAAA!!!!111",
            u"It's all the same shit",
            u"GET OUT",
            u"PROFIT!",
            u"Bitches don't know bout my dick",
            u"All your base are belong to us!",
            u"Enlarge your penis",
            u"Everyone else has had more sex than you",
            u"HAHAHA DISREGARD THAT, I SUCK COCKS",
            u"Haters gonna hate",
            u"I dunno LOL",
            u"Just as planned",
            u"Mindfuck",
            u"NO WAI",
            u"Nuff said",
            u"*Poker face*",
            u"Sad but true",
            u"Shit happens",
            u"Use the force, Luke",
            u"Я тебя помножу на ноль",
            u"Истина где-то рядом",
            u"Нет времени объяснять",
            u"Слоупок",
            u"Моар!",
            u"Дыа",
            u"Быстро, решительно!",
            u"Голос со стороны параши",
            u"Мужской половой хуй",
            u"Проблемы с доступом в ДЖОЙКАЗИНО?",
            u"Ебала жаба гадюку!",
            u"Залей все маянезиком",
            u"В этой стране все через жопу",
            u"Who are you to fucking lecture me?",
            u"Arbeit macht frei",
            u"Забудьте все, чему вас учили",
            u"Я ведь не настоящий сварщик",
            u"Джигурда",
            u"Отвечает Александр Друзь",
            u"Русский вопрос, бессмысленный и беспощадный",
            u"Ибо ваистену",
            u"Потому что пошел на хуй",
            u"Казалось бы, причем здесь бобры",
            u"Лец ми спик фром май харт ин инглиш",
            u"Но это уже совсем другая история",
            u"Дауншифтинг",
            u"Неведомая ёбаная хуйня",
            u"Отака хуйня, малята",
            u"Огромные боевые человекоподобные роботы",
            u"Канонiчно",
            u"I came",
            u":areyoukiddingme:",
            u":butthurt:",
            u":dangerfrog:",
            u":happyfrog:",
            u":scaredfrog:",
            u":smugfrog:",
            u":sweetjesus:"
        ]
        return random.choice(responses_list)


if __name__ == "__main__":
    bot = BrutalElk('brutal_elk', os.environ.get('TOKEN'), 'Brutal Elk')
    bot.run()
