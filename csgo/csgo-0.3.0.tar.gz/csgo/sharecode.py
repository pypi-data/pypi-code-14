import re

dictionary = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefhijkmnopqrstuvwxyz23456789"

def decode(code):
    """Decodes a match share code

    :param code: match share code (e.g. ``CSGO-Ab1cD-xYz23-7bcD9-uVZ23-12aBc``)
    :type code: str
    :raises: :class:`ValueError`
    :return: dict with matchid, outcomeid and token
    :rtype: dict

    .. code:: python

        {'matchid': 0,
         'outomceid': 0,
         'token': 0
         }
    """
    if not re.match(r'^(CSGO)?(-?[ABCDEFGHJKLMNOPQRSTUVWXYZabcdefhijkmnopqrstuvwxyz23456789]{5}){5}$', code):
        raise ValueError("Invalid share code")

    code = re.sub('CSGO\-|\-', '', code)[::-1]

    a = b = 0
    for c in code:
        a = a*len(dictionary) + dictionary.index(c)

    for n in range(0, 144, 8):
        b = (b << 8) + ((a >> n) & 0xFF)

    return {
        'matchid': b & (2**64-1),
        'outcomeid': b >> 64 & (2**64-1),
        'token': b >> 128 & 0xFFFF
    }

def encode(matchid, outcomeid, token):
    """Encodes (matchid, outcomeid, token) to match share code

    :param matchid: match id
    :type matchid: int
    :param outcomeid: outcome id
    :type outcomeid: int
    :param token: token
    :type token: int
    :return: match share code (e.g. ``CSGO-Ab1cD-xYz23-7bcD9-uVZ23-12aBc``)
    :rtype: str
    """
    b = (token << 128) | (outcomeid << 64) | matchid

    a = 0
    for n in range(0, 144, 8):
        a = (a << 8) + ((b >> n) & 0xFF)

    code = ''
    for _ in range(25):
        a, r = divmod(a, len(dictionary))
        code += dictionary[r]

    return "CSGO-%s-%s-%s-%s-%s" % (code[:5], code[5:10], code[10:15], code[15:20], code[20:])
