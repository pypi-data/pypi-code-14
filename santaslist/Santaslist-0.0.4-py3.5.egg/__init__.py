from SantasList.SantasList import SantasList

__author__ = 'Jeffrey Hann'
__version__ = '0.0.4'

_theList = None


def load_people(people):
    global _theList
    _theList = SantasList(people)


def list_matches():
    global _theList
    return _theList.matches()
