import random


import qtmud
import fyreside


# todo: player accounts
# search_by_connceted_player
# serach by player accounts
#

class Card(object):
    def __init__(self):
        self.name = 'Basic Card'
        self.owner = None
        self.needs_singular_target = False
        self.needs_target = False
        self.rarity = 0
        self.cost = 0

    def play(self, player, target):
        return True


class ConvenientPortal(Card):
    def __init__(self):
        super(ConvenientPortal, self).__init__()
        self.name = 'Convenient Portal'
        self.rarity = 5
        self.cost = 4
        self.needs_singular_target = True
        self.ability = ('Steals a random card from another players hand!')

    def play(self, player, target):
        if target.hand:
            card = random.choice(target.hand)
            target.hand.remove(card)
            player.hand.append(card)
            card.owner = player
            qtmud.schedule('send', recipient=player,
                           text='You steal their {}'.format(card.name))
            qtmud.schedule('send', recipient=target,
                           text='{} steals your {}!'.format(player.name,
                                                            card.name))
        else:
            card = random.choice(fyreside.DECK)
            card.cost += -2
            player.hand.append(card)
            qtmud.schedule('send', recipient=player,
                           text='They didn\'t have any cards, but you '
                                'received this {}, with -2 to its cost.'
                                ''.format(card.name))


class ClockworkWeasel(Card):
    def __init__(self):
        super(ClockworkWeasel, self).__init__()
        self.name = 'Clockwork Weasel'
        self.rarity = 4
        self.cost = 3
        self.needs_singular_target = True
        self.ability = ('Tells you the cards an opponent has in their hands - '
                        'and the opponent will be none the wiser!')

    def play(self, player, target):
        output = ''
        spied_hand = '\n'.join([c.name for c in target.hand])
        output += ('You send your clockwork weasel scurrying toward {} '
                   'and after a moment, the weasel tells you cards they '
                   'have in their hand:\n{}'.format(target.name,
                                                    spied_hand))

        qtmud.schedule('send', recipient=player, text=output)


class Fireball(Card):
    def __init__(self):
        super(Fireball, self).__init__()
        self.name = 'Fireball'
        self.rarity = 5
        self.cost = 2
        self.stats = {'damage' : 3}

    def play(self, player, target):
        damage = self.stats['damage']
        target.health += -damage
        qtmud.schedule('send', recipient=player,
                       text='Your fireball hits {} for {} damage'
                            ''.format(target.name, damage))
        qtmud.schedule('send', recipient=player,
                       text='{} throws a fireball at you for {} damage'
                            ''.format(player.name, damage))

class HamfistedOgre(Card):
    def __init__(self):
        super(HamfistedOgre, self).__init__()
        self.name = 'Hamfisted Ogre'
        self.owner = None
        self.rarity = 3
        self.cost = 6
        self.stats = {'damage' : 6 }
        self.ability = ('Does {} to whoever its played against, but in its '
                        'eagerness to cause damage, does {} to whoever played '
                        'it.'.format(self.stats['damage'],
                                     int(self.stats['damage']/2)))

    def play(self, player, target):
        damage = self.stats['damage']
        qtmud.schedule('damage', player=target, amount=damage)
        qtmud.schedule('send', recipient=player,
                       text= ('Your Hamfisted Ogre does {} damage to {}, '
                              'but also does {} damage to you.'
                              ''.format(damage, target.name, int(damage/2))))
        qtmud.schedule('damage', player=player, amount=int(self.damage/2))
        qtmud.schedule('send', recipient=player,
                       text=('{}\'s Hamfisted Ogre does {} damage to you.'
                             ''.format(player.name, damage)))


class RecklessEngineer(Card):
    def __init__(self):
        super(RecklessEngineer, self).__init__()
        self.name = 'Reckless Engineer'
        self.owner = None
        self.rarity = 4
        self.cost = 4
        self.stats = {'repair': 4,
                      'damage': 2}
        self.ability = ('Adds {} to your (or a target\'s) armor, but does {} '
                        'damage to you/them as well. (The armor comes first.)'
                        ''.format(self.stats['repair'], self.stats['damage']))

    def play(self, player, target=None):
        if not target:
            target = player
        repair = self.stats['repair']
        damage = self.stats['damage']
        qtmud.schedule('armor', player=target, amount=repair)
        qtmud.schedule('damage', player=target, amount=damage)
        qtmud.schedule('send', recipient=target,
                       text=('{}\'s RecklessEngineer repairs you for {} '
                             'armor, but then hurts you for {} damage.'
                             ''.format(player.name, repair, damage)))


class Spam(Card):
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
        for client in qtmud.connected_clients:
            if not client == player:
                qtmud.schedule('send', recipient=client,
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


class Ork(Card):
    def __init__(self):
        super(Ork, self).__init__()
        self.name = 'Ork'
        self.owner = None
        self.rarity = 4
        self.cost = 1
        self.stats = {'damage': 2}
        self.ability = {'Does 2 damage to a random player - possibly the one '
                        'who played it!'}

    def play(self, player, target):
        victim = random.choice(qtmud.connected_clients)
        qtmud.schedule('damage', player=victim, amount=self.stats['damage'])
        qtmud.schedule('send',
                       recipient=player,
                       text='You attack {}'.format(victim.name))
        qtmud.schedule('send',
                       recipient=victim,
                       text='{}\'s Ork attacks you.'.format(player.name))



class Grunt(Card):
    def __init__(self):
        super(Grunt, self).__init__()
        self.name = 'Grunt'
        self.owner = None
        self.rarity = 5
        self.cost = 3
        self.stats = {'armor': 2}
        self.ability = ('Boosts the player\'s armor by {}'
                        ''.format(self.stats['armor']))

    def play(self, player, target):
        player.armor += self.stats['armor']
        qtmud.schedule('send', recipient=player,
                       text=('Your Grunt boosts your armor by {}'
                             ''.format(self.stats['armor'])))


class Pablo(Card):
    """ Pablo costs 7 mana, and adds 2 points to every player's armor -
    except one. That unfortunate player (can't be the person who played
    Pablo) loses all of their armor. """
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


class PetulantChild(Card):
    def __init__(self):
        super(PetulantChild, self).__init__()
        self.name = 'Petulant Child'
        self.owner = None
        self.rarity = 5
        self.cost = 0
        self.ability = ('Restores the target\'s health to maximum, but costs '
                        'one more mana the next time its drawn.')

    def play(self, player, target):
        if not target:
            target = player
        target.health = target.max_health
        self.cost += 1


class SecretSquirrel(Card):
    def __init__(self):
        super(SecretSquirrel, self).__init__()
        self.name = 'Secret Squirrel'
        self.rarity = 5
        self.cost = 3
        self.needs_singular_target = True
        self.ability = 'Find the stats & hand of one player.'

    def play(self, player, target):
        hand_string = ', '.join([c.name for c in target.hand])
        output = ('{target.name} has {target.health} health, {target.armor} '
                  'armor, {target.mana} mana, and the following cards in '
                  'their hand: {hand_string}.'.format(**locals()))
        qtmud.schedule('send', recipient=player, text=output)


class ScoutBalloon(Card):
    def __init__(self):
        super(ScoutBalloon, self).__init__()
        self.name = 'Scout Balloon'
        self.rarity = 4
        self.cost = 10
        self.ability = 'Find the stats & hand of every player'

    def play(self, player, target):
        reports = list()
        for target in fyreside.connected_players:
            hand_string = ', '.join([c.name for c in target.hand])
            reports.append('{target.name} has {target.health} health, '
                          '{target.armor} armor, {target.mana} mana, '
                          'and the following cards in their hand:'
                          '{hand_string}.'.format(**locals()))
        qtmud.schedule('send', recipient=player,
                       text='You receive the following reports from your '
                            'scout balloon:\n{}'
                            ''.format(' \n'.join(reports)))


class MysticGiant(Card):
    def __init__(self):
        super(MysticGiant, self).__init__()
        self.name = 'Mystic Giant'
        self.rarity = 0
        self._cost = 35
        self.stats = {'armor': 20}
        return

    @property
    def cost(self):
        return self._cost - len(self.owner.history)

    @cost.setter
    def cost(self, value):
        self._cost = value

    def play(self, player, target):
        output = ('The mystic giant puts you on his shoulders, protecting you '
                  'from harm. (+{} armor)'.format(self.stats['armor']))
        qtmud.schedule('send', recipient=player, text=output)
        return True
