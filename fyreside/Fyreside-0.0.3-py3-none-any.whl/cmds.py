import qtmud

import fyreside


def deck(player, *, H=False, h=False):
    """ Shows the player how many cards are in the deck.

        :param player:      The player issuing the command. (That'd be you.)
                            *This isn't part of the command you enter.*
        :param H:           Shows the player this docstring
        :param h:           Shows the player a brief help
    """
    output = ''
    brief = ('score [-Hh]\n\n'
             'Shows you how many cards are in the deck.')
    if H:
        output += score.__doc__
    if h:
        output += brief
    else:
        output += 'There are {} in the deck.'.format(len(fyreside.DECK))
    if output:
        qtmud.schedule('send', recipient=player, text=output)


def draw(player, *, H=False, h=False):
    """ Draws a card from :attr:`fyreside.DECK` into the player's hand.

        :param player:      The player issuing the command. (That'd be you.)
                            *This isn't part of the command you enter.*
        :param H:           Shows the player this docstring
        :param h:           Shows the player a brief help

    """
    output = ''
    brief = ('draw [-Hh]\n\n'
             'Draws a card from the deck.')
    if H:
        output += hand.__doc__
    if h:
        output += brief
    elif len(player.hand) >= player.max_hand:
        output += 'Can\'t draw any more cards, hand full.'
    else:
        qtmud.schedule('draw', player=player, count=1)
    qtmud.schedule('send', recipient=player, text=output)


def hand(player, *, H=False, h=False):
    """ Sends a list of the cards in the player's hands to them.

        :param player:      The player issuing the command. (That'd be you.)
                            *This isn't part of the command you enter.*
        :param H:           Shows the player this docstring
        :param h:           Shows the player a brief help

        Pretty straightforward - shows the player their hand.
    """
    output = ''
    brief = ('hand [-Hh]\n\n'
             'Shows you the cards in your hand.')
    if H:
        output += hand.__doc__
    if h:
        output += brief
    else:
        output += ('You have {} of a maximum {} cards in your hand:\n'
                   '{}'.format(len(player.hand), player.max_hand,
                               ', '.join([c.name for c in player.hand])))
    if output:
        qtmud.schedule('send', recipient=player, text=output)


def info(player, *card, H=False, h=False):
    """ Shows a card's info

        :param player:      The client issuing the command. (That'd be you.)
                            *This isn't part of the command you enter.*
        :param H:           Shows the client this docstring.
        :param h:           Shows the client a brief help.
    """
    output = ''
    brief = ('info [-Hh] card\n\n'
             'Shows you the info about card.')
    if H:
        output += info.__doc__
    if h:
        output += brief
    elif card:
        card = ' '.join(card)
        cards = fyreside.search_hand(player, card)
        if len(cards) == 1:
            card = cards[0]
            output += ('--- {card.name} ---\n'
                       'COST .....  {card.cost:.>5}\n'
                       'RARITY....  {card.rarity:.>5}\n'.format(**locals()))
            if card.stats:
                for stat in card.stats:
                      output += ('{:.<10}  {:.>5}\n'.format(stat.upper(),
                                                     card.stats[stat]))
            if card.ability:
                output += card.ability+'\n'
        if len(cards) == 0:
            output += 'Couldn\'t find {} in your hand'.format(card)
        if len(cards) > 1:
            output += ('More than one match found: {}'
                       ''.format(', '.join([c.name for c in cards])))
    else:
        output += brief
    if output:
        qtmud.schedule('send', recipient=player, text=output)


def play(player, *card, H=False, h=False, target=''):
    """ Command for playing a card from the player's hand, optionally at a
    target.

        :param player:      The client issuing the command. (That'd be you.)
                            *This isn't part of the command you enter.*
        :param H:           Shows the client this docstring.
        :param h:           Shows the client a brief help.
        :param card:        The name of the card to be played.
        :param target:      The name of the player the card will be
                            targeted at.
    """
    output = ''
    brief = ('play [-Hh] [--target=`target`[,`target 2`[, ...]] <`card`>'
             'play grunt\n'
             'play petulant child\n'
             'play ork --target=emsenn\n\n'
             'Plays `card` in in your hand, optionally at `target`.')
    if H:
        output += play.__doc__
    if h:
        output += brief
    elif card:
        card = ' '.join(card)
        cards = fyreside.search_hand(player, card)
        if len(cards) == 1:
            card = cards[0]
            if target in ['me', 'self']:
                target = player
            else:
                targets = fyreside.search_connected_players_by_name(target)
                if len(targets) == 1:
                    target = targets[0]
                else:
                    target = None
            if card.needs_singular_target and not target:
                output += ('{} needs a target, try again.'.format(card.name))
            elif player.mana >= card.cost:
                try:
                    card.play(player=player)
                except TypeError as err:
                    card.play(player=player, target=target)
                player.hand.remove(card)
                fyreside.DECK.append(card)
                player.history.append(card.name)
                player.mana += -card.cost
                card.owner = None
                output += ('After your play succeeded, you shuffled {} '
                           'back into the deck.'.format(card.name))
            else:
                output += ('Don\'t have enough mana.')
        elif len(cards) == 0:
            output += ('You don\'t have that card.')
        elif len(cards) > 1:
            output += ('More than one match found, try using numbers like '
                       '`{} 1`:\n{}'.format(
                cards[0].name.split(' ')[-1].lower(),
                '\n'.join([c.name for c in cards])))
        else:
            output += 'Shouldn\'t end up in this part of the loop...'
    else:
        raise FyresideWarning('invalid user input')
    qtmud.schedule('send', recipient=player, text=output)


def score(player, *, H=False, h=False):
    """ Shows the player their current statistics.

        :param player:      The player issuing the command. (That'd be you.)
                            *This isn't part of the command you enter.*
        :param H:           Shows the player this docstring
        :param h:           Shows the player a brief help
    """
    output = ''
    brief = ('score [-Hh]\n\n'
             'Tells you your score.')
    if H:
        output += score.__doc__
    if h:
        output += brief
    else:
        output += ('HEALTH: {player.health}\n'
                   'ARMOR:  {player.armor}\n'
                   'MANA:   {player.mana}\n'.format(**locals()))
    if output:
        qtmud.schedule('send', recipient=player, text=output)





