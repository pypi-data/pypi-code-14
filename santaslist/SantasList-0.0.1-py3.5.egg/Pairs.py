import random
from SantasList.Objects import Pair


class Pairs(list):
    _pairs = []

    def __init__(self, people):
        while len(people) > 0:
            a = self._pop_list(people)
            b = self._pop_list(people)

            self._pairs.append(Pair(a, b))

        list.__init__(self, self._pairs)

    def __str__(self):
        return '\n'.join(str(x) for x in self._pairs)

    @staticmethod
    def _pop_list(my_list):
        indices = list(range(0, len(my_list)))

        x = random.choice(indices)
        y = my_list[x]

        del indices[x]
        del my_list[x]

        return y
