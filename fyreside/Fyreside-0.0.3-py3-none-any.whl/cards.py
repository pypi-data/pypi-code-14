import random

import qtmud

import fyreside


class Card(object):
    """ The base class all other cards build off of.

        :param kwargs:      If any arguments are passed when Card() is called,
                            they'll be passed on as arguments to Card.update()
    """
    def __init__(self, **kwargs):
        self.name = 'Basic Card'
        """ The card's name can be used to reference the card within the
        game. If a ``name`` is more than one word, the last word can be used
        as an abbreviation."""
        self.owner = None
        """ The player who 'owns' the card. Ownership is an arbitrary game
        concept, and doesn't necessarily reflect the player whose hand the
        card is in."""
        self.needs_singular_target = False
        """ This will be set to True if the card requires one, and only one,
        target. """
        self.needs_target = False
        """ This will be set to True if a card requires one or more targets. """
        self.rarity = 0
        """ Rarity defines how many of the card will be placed into the deck
        when the Fyreside game was :func:`load <fyreside.load>`ed. ``0``
        means the card won't be in the deck. In my head, rarity works out to:

        ============  ============
         ``rarity``    Descriptor
        ============  ============
              1       Unique
              2       Rare
              3       Uncommon
              4       Common
              5       Basic
        ============  ============
        """
        self.cost = 0
        """ How many :attr:`mana <fyreside.Player.mana>` it takes to play this
        card."""
        self.stats = dict()
        self.ability = None
        self.update(**kwargs)

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            self.__dict__[attr] = value


class BasikOrk(Card):
    """ Cheap card that attacks a random player. """
    def __init__(self):
        super(BasikOrk, self).__init__()
        self.update(name='Basik Ork', rarity=5, cost=1,
                    stats={'damage': 2},
                    ability='Randomly hits a player.')

    def play(self, player):
        victim = random.choice(fyreside.connected_players)
        qtmud.schedule('damage', player=victim, amount=self.stats['damage'])
        qtmud.schedule('send', recipient=player,
                       text='You attack {}'.format(victim.name))
        qtmud.schedule('send', recipient=victim,
                       text='{}\'s Ork attacks you.'.format(player.name))


class ClockworkWeasel(Card):
    """ Sneakily reports its target's hand. """

    def __init__(self):
        super(ClockworkWeasel, self).__init__()
        self.update(name='Clockwork Weasel', rarity=4, cost=3,
                    needs_singular_target=True,
                    ability='Secretly tells you an opponent\'s hand.')

    def play(self, player, target):
        output = ''
        spied_hand = '\n'.join([c.name for c in target.hand])
        output += ('You send your clockwork weasel scurrying toward `{}` '
                   'and after a moment, the weasel returns, showing you the '
                   'cards they have in their hand:\n{}'.format(target.name,
                                                               spied_hand))

        qtmud.schedule('send', recipient=player, text=output)


class ConvenientPortal(Card):
    """ Steals a random card from its target. """
    def __init__(self):
        super(ConvenientPortal, self).__init__()
        self.update(name='Convenient Portal', rarity=4, cost=4,
                    needs_singular_target=True,
                    ability='Steal a random `card` from `target`\'s hand.')

    def play(self, player, target):
        if target.hand:
            random.shuffle(target.hand)
            card = target.hand.pop()
            player.hand.append(card)
            card.owner = player
            qtmud.schedule('send', recipient=player,
                           text='You steal their `{}`'.format(card.name))
            qtmud.schedule('send', recipient=target,
                           text='`{}` steals your `{}`!'.format(player.name,
                                                                card.name))
        else:
            random.shuffle(fyreside.DECK)
            card = fyreside.DECK.pop()
            card.cost += -2
            player.hand.append(card)
            card.owner = player
            qtmud.schedule('send', recipient=player,
                           text='They didn\'t have any cards, '
                                'so we drew this {} and gave it `-2` '
                                'cost.'.format(card.name))


class Fireball(Card):
    """ Does a small amount of damage to its target """
    def __init__(self):
        super(Fireball, self).__init__()
        self.update(name='Fireball', rarity=5, cost=2,
                    stats={'damage': 3})
        self.needs_singular_target = True

    def play(self, player, target):
        damage = self.stats['damage']
        target.health += -damage
        qtmud.schedule('send', recipient=player,
                       text='Your fireball hits {} for {} damage'
                            ''.format(target.name, damage))
        qtmud.schedule('send', recipient=player,
                       text='{} throws a fireball at you for {} damage'
                            ''.format(player.name, damage))
        return True


class Grunt(Card):
    """ Boosts the target's armor. """
    def __init__(self):
        super(Grunt, self).__init__()
        self.name = 'Grunt'
        self.owner = None
        self.rarity = 5
        self.cost = 3
        self.stats = {'armor': 2}
        self.ability = ('Boosts the player\'s armor by {}'
                        ''.format(self.stats['armor']))

    def play(self, player):
        player.armor += self.stats['armor']
        qtmud.schedule('send', recipient=player,
                       text=('Your Grunt boosts your armor by {}'
                             ''.format(self.stats['armor'])))


class HamfistedOgre(Card):
    """ Does a fair amount of damage to its target - and half that to whoever
    plays it. """
    def __init__(self):
        super(HamfistedOgre, self).__init__()
        self.update(name='Hamfisted Ogre', rarity=3, cost=6,
                    stats={'damage': 6})
        self.ability = ('Does {} to its target, but half as much to its '
                        'owner!'.format(self.stats['damage']))

    def play(self, player, target):
        damage = self.stats['damage']
        qtmud.schedule('damage', player=target, amount=damage)
        qtmud.schedule('send', recipient=player,
                       text=('Your Hamfisted Ogre does {} damage to {}, '
                             'but also does {} damage to you.'
                             ''.format(damage, target.name, int(damage / 2))))
        qtmud.schedule('damage', player=player, amount=int(damage / 2))
        qtmud.schedule('send', recipient=player,
                       text=('{}\'s Hamfisted Ogre does {} damage to you.'
                             ''.format(player.name, damage)))


class PetulantChild(Card):
    """ Fully heals its target, but gets more expensive each time it's played.
    """
    def __init__(self):
        super(PetulantChild, self).__init__()
        self.update(name='Petulant Child', rarity=5, cost=0,
                    ability=('Completely restore\'s `target`\'s health, '
                             'but its own cost goes up by one each time.'))

    def play(self, player, target):
        if not target:
            target = player
        target.health = target.max_health
        qtmud.schedule('send', recipient=player,
                       text=('You use your {} to heal {}'.format(self.name,
                                                                 target.name)))
        qtmud.schedule('send', recipient=target,
                       text=('{} heals you with their {}.'
                             ''.format(player.name,
                                       self.name)))
        self.cost += 1

class RecklessEngineer(Card):
    """ Gives its target four armor, then takes away two health.

        .. warning:: This card is broken atm, and won't show up in the deck.
    """
    def __init__(self):
        super(RecklessEngineer, self).__init__()
        self.update(name='Reckless Engineer', rarity=0, cost=4,
                    stats={'repair': 4, 'damage': 2},
                    ability='Repairs then damages a `target`.')

    def play(self, player, target=None):
        if not target:
            target = player
        repair, damage = self.stats['repair'], self.stats['damage']
        qtmud.schedule('armor', player=target, amount=repair)
        qtmud.schedule('damage', player=target, amount=damage)
        qtmud.schedule('send', recipient=target,
                       text=('{}\'s {} repairs you for {} '
                             'armor, but then hurts you for {} damage.'
                             ''.format(player.name, self.name, repair, damage)))
        return True


class Spam(Card):
    """ Boosts the armor by however many players there are, who all receive
    spam. """
    def __init__(self):
        super(Spam, self).__init__()
        self.name = 'Spam'
        self.rarity = 2
        self.cost = 7
        self.stats = {'armor' : 1}
        self.ability = ('Sends a spammy message to every player, and you gain '
                        '{} for every player it hits.'
                        ''.format(self.stats['armor']))

    def play(self, player, target=None):
        target_count = 0
        for target in fyreside.connected_players:
            if not target == player:
                qtmud.schedule('send', recipient=target,
                               text= ('{} played the SPAM card!\n'
                                      '       SSSSS  PPPP   AA   M  M  M\n'
                                      '       S      P  P  A  A  MM M MM\n'
                                      '       SSSSS  PPPP  AAAA  M M M M\n'
                                      '           S  P     A  A  M     M\n'
                                      '       SSSSS  P     A  A  M     M '
                                      ''.format(player.name)))
                target_count += 1
        player.armor += target_count * self.stats['armor']
        qtmud.schedule('send', recipient=player,
                       text=('Hit {} players with your SPAM, so you\'ve '
                             'gained that much armor'.format(target_count)))







class Pablo(Card):
    """ Adds to every player's armor (including whoever played it) - except
    one, who loses all of their armor. """
    def __init__(self):
        super(Pablo, self).__init__()
        self.name = 'Pablo'
        self.rarity = 1
        self.cost = 7
        self.stats = {'armor':2}
        self.ability = ('Pablo adds {} to every player\'s armor - except one'
                        'at random, who loses all of theirs.'
                        ''.format(self.stats['armor']))

    def play(self, player, target):
        players = fyreside.connected_players
        if len(players) == 1:
            qtmud.schedule('send', recipient=player,
                           text=('You\'re the only player, so Pablo chills '
                                 'with you for a bit. You gain 8 mana.'))
            player.mana += 8
            return True
        random.shuffle(players)
        victim = players.pop()
        if victim == player:
            _victim = players.pop()
            players.append(victim)
            victim = _victim
        victim.armor = 0
        qtmud.schedule('send', recipient=victim,
                       text=('{} funds Pablo\'s war against you, destroying '
                             'your armor.'.format(player.name)))
        for p in players:
            p.armor += self.stats['armor']
            qtmud.schedule('send',recipient=p,
                       text=('{} and Pablo are a rising tide. {} armor '
                             'for everyone.'.format(player.name,
                                                    self.stats['armor'])))
        return True




class SecretSquirrel(Card):
    """ Sneakily reports the hand & stats of its target. """
    def __init__(self):
        super(SecretSquirrel, self).__init__()
        self.update(name='Secret Squirrel', rarity=4, cost=4,
                    needs_singular_target=True,
                    ability='Sneakily report stats & hand of a `target`')

    def play(self, player, target):
        hand_string = ', '.join([c.name for c in target.hand])
        output = ('{target.name} has {target.health} health, {target.armor} '
                  'armor, {target.mana} mana, and the following cards in '
                  'their hand: {hand_string}.'.format(**locals()))
        qtmud.schedule('send', recipient=player, text=output)
        return True


class ScoutBalloon(Card):
    """ Reports the stats & hand of every player. """
    def __init__(self):
        super(ScoutBalloon, self).__init__()
        self.update(name='Scout Balloon', rarity=4, cost=10,
                    ability='Find the stats & hand of every player.')

    def play(self, player):
        reports = list()
        for target in fyreside.connected_players:
            hand_string = ', '.join([c.name for c in target.hand])
            reports.append('{target.name} has {target.health} health, '
                           '{target.armor} armor, {target.mana} mana, '
                           'and the following cards in their hand:'
                           '{hand_string}.'.format(**locals()))
            qtmud.schedule('send', recipient=player,
                           text='{} releases a scout balloon.'
                                ''.format(player.name))
        qtmud.schedule('send', recipient=player,
                       text='You receive the following reports from your '
                            'scout balloon:\n{}'
                            ''.format(' \n'.join(reports)))
        return True


class MysticGiant(Card):
    """ Heavily armors the player. Costs less the more cards you've played. """
    def __init__(self):
        super(MysticGiant, self).__init__()
        self.update(name='Mystic Giant', rarity=2,
                    stats={'armor': 20})
        self._cost = 35
        return

    @property
    def cost(self):
        return self._cost - len(self.owner.history)

    @cost.setter
    def cost(self, value):
        self._cost = value

    def play(self, player):
        output = ('The mystic giant puts you on his shoulders, protecting you '
                  'from harm. (+{} armor)'.format(self.stats['armor']))
        qtmud.schedule('send', recipient=player, text=output)
        return True
