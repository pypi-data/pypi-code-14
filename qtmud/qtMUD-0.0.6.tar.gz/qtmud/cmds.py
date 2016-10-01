import qtmud

def finger(fingerer, line):
    """ Command for fingering a client. """
    qtmud.schedule('finger',
                   fingerer=fingerer,
                   fingeree=line)
    return True


def commands(commander, line):
    output = ('Your commands are: {}'
              ''.format(', '.join([c for c in commander.commands.keys()])))
    qtmud.schedule('send',
                   recipient=commander,
                   text=output)
    return True

def foo(client, line):
    mudsocket = qtmud.active_services['mudsocket']
    output = mudsocket.connections
    qtmud.schedule('send', recipient=client, text='{}'.format(output))
    return True


def help(client, query=''):
    """ Sends the docstring for a command to helpee.

        in-game syntax: help [domain] <command|subscriber|service>

        :param client: the client who is asking for help
        :param query: the topic being queried for help.


     """
    output = ''
    domain = None
    matches = []
    if not query:
        output = ('syntax: help [domain] <command|subscriber|service>. '
                  '"commands" to see all your commands.')
    #####
    #
    #
    #
    #####
    if len(query.split(' ')) > 1:
        domain = query.split(' ')[0]
        query = ' '.join(query.split(' ')[1:])
        if domain in ['commands', 'command', 'cmds']:
            domain = 'cmds'
        if domain in ['subscriptions', 'subscription', 'subscribers']:
            domain = 'subscribers'
        if domain in ['services', 'service']:
            domain = 'active_services'
        else:
            output = ('{} is not a valid domain.'.format(domain))
    #####
    #
    #
    #
    #####
    if domain == 'cmds' or not domain:
        if query in client.commands:
            matches.append(client.commands[query])
        elif domain:
            output = 'Can\'t find help for {} in commands'.format(query)
    if domain == 'subscribers' or not domain:
        if query in qtmud.subscribers:
            for subscriber in qtmud.subscribers[query]:
                matches.append(subscriber)
        elif domain:
            output = 'Can\'t find help for {} in subscribers'.format(query)
    if domain == 'active_services' or not domain:
        if query in qtmud.active_services:
            matches.append(qtmud.active_services[query])
        elif domain:
            output = 'Can\'t find help for {} in active_services'.format(query)
    #####
    #
    #
    #
    #####
    if matches:
        if len(matches) == 1:
            output = matches[0].__doc__
        elif len(matches) > 1:
            output = ('Multiple matches found; try "help [domain] {}" where '
                      'domain is one of: {}'
                      ''.format(query,
                                ', '.join([m.__module__.split('.')[-1]
                                                for m in
                                           matches])))
        elif len(matches) == 0:
            output = ('Couldn\'t find help on that topic.')
    if not output:
        output = 'Couldn\'t find help for {}'.format(query)
    qtmud.schedule('send', recipient=client, text=output)
    return True


def whoami(client, line):
    """ Says your name back at you """
    qtmud.schedule('send', recipient=client,
                   text='You are {}'.format(client.name))
    return True




def talker(client, line):
    output = ''
    if not line:
        output = 'you\'re listening to {}'.format([c for c in client.channels])
    else:
        line = line.split(' ')
        if line[0] in ['history']:
            channel = ' '.join(line[1:])
            if not channel:
                output = 'syntax: talker history <channel>'
            if channel in client.channels:
                output = '{}'.format('\n'.join(m for m in
                                               qtmud.active_services[
                                                   'talker'].history[
                                                   channel]))
    if not output:
        output = ('Invalid syntax, check "help talker" for more.')
    qtmud.schedule('send', recipient=client, text=output)


def quit(client, line):
    qtmud.schedule('send', recipient=client, text='you quit goodbye')
    qtmud.schedule('client_disconnect', client=client)


def who(client, line):
    qtmud.schedule('send',
                   recipient=client,
                   text='The following clients are currently connected:\n'
                        '{}'.format('\n'.join([c.name
                                               for c in
                                    qtmud.connected_clients])))
    return True