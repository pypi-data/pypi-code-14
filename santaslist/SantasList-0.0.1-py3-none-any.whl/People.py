from SantasList.Objects import Person


class People(list):
    _people = []

    def __init__(self, people):
        self._people = [Person(x) for x in people]

        list.__init__(self, self._people)

    def __str__(self):
        return ','.join(str(x) for x in self._people)
