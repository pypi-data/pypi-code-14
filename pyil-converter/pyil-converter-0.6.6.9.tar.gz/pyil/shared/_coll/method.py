import re,random
from .error import FileError
def cli(ext: str):
    raise FileError('cannot open file with this extension: %s.' % ext)


def switch_bool(v: bool):
    return False if v else True


def compare(n1: str, n2: str, i=False):
    return re.match(n2.lower(), n1.lower()) is not None if i else re.match(n2, n1) is not None

def random_word(length:int, word_only:bool=False)->str:
    """Generates random letter combinations."""
    if not word_only:
        temp = ('a', 'b', 'c', 'd', 'e', 'f', '1', '2',
                '3', '4','5', '0', 'A', 'h', 'H',
                'B', 'C', 'D', 'E', 'F', '.', ',',
                '?', '<', '>', '!', 'x', 'X', 'G.M')
        temp2 = ''
        for i in range(length):
            temp2 += (random.choice(temp))
        return temp2
    temp = ('a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5', '0', 'A', 'h', 'H',
            'B', 'C', 'D', 'E', 'F', 'x', 'X')
    temp2 = ''
    for i in range(length):
        temp2 += (random.choice(temp))
    return temp2
