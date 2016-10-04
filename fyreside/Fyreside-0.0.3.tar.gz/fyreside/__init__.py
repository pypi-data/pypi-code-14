from inspect import getmembers, isfunction, isclass

import qtmud
import qtmud.subscriptions

from fyreside import cards, cmds, services, subscriptions, txt

__version__ = '0.0.3'

connected_players = list()
""" The currently connected players. """
player_hands = dict()
""" All the hands currently held by different players, in the format of
``{ player : [ list, of, cards ] }``"""
DECK = list()
""" built from the classes in :mod:`fyreside.cards` when :func:`load` is
called. """


class Player(qtmud.Client):
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.max_hand = 7
        self.max_health = 20
        self.history = list()
        self.hand = list()
        self.health = 20
        self.mana = 10
        self.armor = 0
        self.word_count = 0
        qtmud.active_services['talker'].tune_channel(client=self,
                                                     channel='fyreside')


def search_connected_players_by_name(name, singular=False):
    matches = [p for p in connected_players if p.name.lower() == name.lower()]
    if singular:
        if len(matches) == 1:
            return matches[0]
        else:
            return None
    return matches


def search_hand(player, text):
    """ Searches player's hands for any cards whose name matches text,
    or whose name has one word matching with text if text is one word.
    """
    matches = list()
    digit = None
    if text[-1].isdigit():
        digit = text.split(' ')[-1]
        text = ' '.join(text.split(' ')[0:-1])
    if text == 'card':
        matches += player.hand
    else:
        for card in player.hand:
            if text == card.name.lower() or \
                    (len(text.split(' ')) == 1 and
                             text == card.name.split(' ')[-1].lower()):
                matches.append(card)
    if matches and digit:
        try:
            # TODO better translation from user reference to list position
            matches = [matches[int(digit) - 1]]
        except IndexError:
            raise SyntaxWarning('You have that card, but not that many.')
    return matches


def load():
    """ Adds Fyreside :mod:`subscriptions <fyreside.subscriptions>` to
    :attr:`qtmud.active_subscribers` and builds :attr:`DECK` from the classes
    in :mod:`fyreside.cards`.
    """
    global DECK
    qtmud.log.info('load()ing Fyreside')
    qtmud.log.info('adding fyreside.subscriptions to qtmud.subscribers')
    for s in getmembers(subscriptions):
        if isfunction(s[1]):
            if not s[1].__name__ in qtmud.subscribers:
                qtmud.subscribers[s[1].__name__] = list()
            qtmud.subscribers[s[1].__name__].append(s[1])
    qtmud.active_services['talker'].new_channel('fyreside')
    for card in [c[1]() for c in getmembers(cards) if isclass(c[1])]:
        for _ in range(card.rarity):
            DECK.append(card.__class__())
    qtmud.log.info('Built the Fireside deck - {} cards total.'
                   ''.format(len(DECK)))
    return True


def start():
    return True

