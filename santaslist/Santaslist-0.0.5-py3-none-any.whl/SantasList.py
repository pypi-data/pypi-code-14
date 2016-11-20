from SantasList.Objects import People
from SantasList.Objects import Pairs


class SantasList(object):
    def __init__(self, people):
        self._people = People(people)

    def people(self):
        return self._people

    def matches(self):
        return Pairs(self._people)
