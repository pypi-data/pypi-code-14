import random
import types
from inspect import getmembers, isfunction

import qtmud

import fyreside


def armor(player, amount=0):
    player.armor += amount
    if player.armor < 0:
        player.armor = 0
    return True


def broadcast(channel, speaker, message):
    if hasattr(speaker, 'word_count'):
        if message:
            speaker.word_count += len(message.split(' '))
            if speaker.word_count >= 50:
                speaker.word_count += -50
                speaker.mana += 1
                qtmud.schedule('send', recipient=speaker,
                               text='You gain a `mana` point.')
    return True


def client_disconnect(client):
    qtmud.log.debug('disconnecting {} from Fireside.'.format(client.name))
    if hasattr(client, 'hand'):
        qtmud.schedule('discard', player=client, all=True)
    try:
        fyreside.connected_players.remove(client)
    # If the player hadn't gotten logged in yet, this'll trigger.
    except ValueError:
        pass
    return True


def client_mudlib_login_parser(client, line):
    player = fyreside.Player(**client.__dict__)
    qtmud.active_services['mudsocket'].replace_client_object(client, player)
    for channel in client.channels:
        qtmud.active_services['talker'].tune_channel(player, channel)
    for command, function in [m for m in getmembers(fyreside.cmds) if
                              isfunction(m[1])]:
        player.commands[command] = types.MethodType(function, player)
    qtmud.connected_clients.remove(client)
    qtmud.connected_clients.append(player)
    fyreside.connected_players.append(player)
    qtmud.schedule('send', recipient=player, text=fyreside.txt.SPLASH)


def damage(player, amount=0):
    if player.armor > 0:
        player.armor += -amount
        amount = 0
        if player.armor < 0:
            amount = abs(player.armor)
            player.armor = 0
    player.health += -amount
    if player.health <= 0:
        qtmud.schedule('death', player=player)
    return True


def death(player):
    qtmud.log.debug('{} killed.'.format(player.name))
    qtmud.schedule('discard', player=player, all=True)
    qtmud.schedule('heal', player=player, full=True)
    player.armor = 0


def discard(player, cards=None, all=False):
    if all is True:
        cards = [c for c in player.hand]
    for card in cards:
        qtmud.log.debug('moving {} from {}\'s hand to the deck.'
                        ''.format(card.name, player.name))
        player.hand.remove(card)
        fyreside.DECK.append(card)
    return


def draw(player, count=1):
    random.shuffle(fyreside.DECK)
    drawn_cards = list()
    for c in range(count):
        try:
            drawn_cards.append(fyreside.DECK.pop())
        except Exception as err:
            qtmud.schedule('send', recipient=player,
                           text='The deck is empty! Wait for someone to play '
                                'a card before drawing something.')
    if drawn_cards:
        for card in drawn_cards:
            player.hand.append(card)
            card.owner = player
            fyreside.player_hands[player.name] = player.hand
        qtmud.schedule('send', recipient=player,
                       text='Drew {} card[s]'.format(', '.join([c.name for c in
                                                                drawn_cards])))
    return True


def heal(player, amount=0, full=False):
    if full is True:
        player.health = 20
    else:
        player.health += amount
        if player.health > 20:
            player.health = 20