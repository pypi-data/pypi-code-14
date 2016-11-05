# -*- coding: utf-8 -*-
import random


class NameGenerator(object):

    def __init__(self, collection, badass):
        self.collection = collection
        self.badass = badass

    def choose_list(self):
        if self.badass:
            return self.collection.the_vicious()
        return self.collection.the_rightful()

    def choose_name(self):
        return random.choice(self.choose_list())
