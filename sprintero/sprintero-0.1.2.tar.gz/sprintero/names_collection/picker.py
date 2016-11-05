# -*- coding: utf-8 -*-

from sprintero.constants import NamesCollectionsE
from sprintero.names_collection.marvel.collection import MarvelCollection


class CollectionPicker(object):

    COLLECTION_MAP = {
        NamesCollectionsE.MARVEL: MarvelCollection
    }

    def __init__(self, collection):
        self.collection = collection

    def read_collection(self):
        return self.COLLECTION_MAP.get(self.collection)()
