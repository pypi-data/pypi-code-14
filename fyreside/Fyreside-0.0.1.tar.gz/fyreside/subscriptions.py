import pickle
import random


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
                speaker.word_count = speaker.word_count - 50
                speaker.mana += 1
                qtmud.schedule('send', recipient=speaker,
                               text='You gain a mana point.')
    return True


def client_mudlib_login_parser(client, line):
    qtmud.schedule('send', recipient=client,
                   text=fyreside.txt.SPLASH)
    player = fyreside.build_player(client)
    qtmud.active_services['talker'].tune_in(channel='one', client=player)
    player.input_parser = 'client_command_parser'


def client_disconnect(client):
    qtmud.log.debug('disconnecting {} from Fireside.'.format(client.name))
    if hasattr(client, 'hand'):
        qtmud.schedule('discard', player=client, all=True)
    fyreside.connected_players.remove(client)
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


def damage(player, amount=0):
    # if a player dies, zero their mana and discard their hand
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