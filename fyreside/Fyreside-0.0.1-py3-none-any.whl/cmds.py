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


def info(player, card, *, H=False, h=False):
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
    else:
        cards = fyreside.search_hand(player, card)
        if len(cards) == 1:
            card = cards[0]
            output += ('--- {card.name} ---\n'
                       'NAME .....  {card.cost:.>5}\n'
                       'RARITY....  {card.rarity:.>5}\n'.format(**locals()))
            if hasattr(card, 'stats'):
                for stat in card.stats:
                      output += ('{:.<10}  {:.>5}\n'.format(stat.upper(),
                                                     card.stats[stat]))
            if hasattr(card, 'ability'):
                output += card.ability+'\n'
        if len(cards) == 0:
            output += 'Couldn\'t find {} in your hand'.format(card)
        if len(cards) > 1:
            output += ('More than one match found: {}'
                       ''.format(', '.join([c.name for c in cards])))
    if output:
        qtmud.schedule('send', recipient=player, text=output)


def play(player, card, *, H=False, h=False, target=''):
    """ Command for playing a card from the player's hand, optionally at a
    target.

        :param player:      The client issuing the command. (That'd be you.)
                            *This isn't part of the command you enter.*
        :param H:           Shows the client this docstring.
        :param h:           Shows the client a brief help.
        :param card:        The name of the card to be played.
        :param target:      The name of the player the card will be targeted at.
    """
    output = ''
    brief = ('play [-Hh] [--target=$target] card\n\n'
             'Plays card in your hand, optionally at $target')
    valid = False
    if H:
        output += play.__doc__
    if h:
        output += brief
    else:
        cards = fyreside.search_hand(player, card)
        if len(cards) == 1:
            valid = True
            card = cards[0]
            output += 'Attempting to play the {} card...'.format(card.name)
            if target in ['me', 'self']:
                targets = [player]
            else:
                targets = fyreside.search_connected_players_by_name(target)
            if hasattr(card, 'needs_target') and len(targets) <= 0:
                output += '...needs a target, didn\'t get one... '
                valid = False
            if hasattr(card, 'needs_singular_target') and len(targets) != 1:
                output += '...needs a single target... '
                valid = False
            if valid is True and player.mana <= card.cost:
                output += ('You need {} mana to play this but only have {}'
                           ''.format(card.cost, player.mana))
                valid = False
        elif len(cards) == 0:
            output += 'Couldn\'t find that card in your hand.'
        elif len(cards) > 1:
            output += 'More than one match for that card.'
        if valid is True:
            player.mana += -card.cost
            output += ('...took {} mana, now you have {} mana... '
                       ''.format(card.cost, player.mana))
            output += ('shuffling {} back into the deck... '.format(card.name))
            player.hand.remove(card)
            fyreside.DECK.append(card)
            player.history.append(card.name)
    if output:
        qtmud.schedule('send', recipient=player, text=output)
    if valid is True:
        card.play(player=player, target=targets[0])


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





