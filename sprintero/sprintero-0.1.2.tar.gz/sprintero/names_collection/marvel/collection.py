# -*- coding: utf-8 -*-

from sprintero.names_collection.base import BaseCollection


class MarvelCollection(BaseCollection):

    def __init__(self):
        self.rightful = 'hero'
        self.vicious = 'badass'
        self.path = 'marvel'

    @property
    def hero(self):
        return self._read_file(name='rightful', relative_path=self.path)

    @property
    def badass(self):
        return self._read_file(name='vicious', relative_path=self.path)
