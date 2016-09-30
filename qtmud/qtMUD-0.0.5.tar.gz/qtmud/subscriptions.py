""" Subscriptions are methods which handle the interaction and manipulation
of :class:`things <qtmud.Thing>`.

Every method in this module is added to :attr:`qtmud.subscribers` when
:func:`qtmud.start`. Calls to these methods which have been :func:`scheduled
<qtmud.schedule>` as :attr:`events qtmud.events>` will be called when
:func:`qtmud.tick` is called.
"""

import qtmud


def broadcast(channel, speaker, message):
    # TODO: emotes
    if not message:
        qtmud.schedule('send', recipient=speaker,
                       text='syntax: {} <message>'.format(channel))
    else:
        for listener in qtmud.active_services['talker'].channels[channel]:
            qtmud.schedule('send',
                           recipient=listener,
                           text='({}) {}: {}'.format(channel,
                                                     speaker.name,
                                                     message))
            qtmud.active_services['talker'].history[
                channel].append('{}: {}'.format(speaker.name, message))
    return True


def client_disconnect(client):
    mudsocket = qtmud.active_services['mudsocket']
    qtmud.log.debug('disconnecting {} from qtmud.'.format(client.name))
    for other in qtmud.connected_clients:
        qtmud.schedule('send',
                       recipient=other,
                       text='{} disconnected.'.format(client.name))
    try:
        qtmud.connected_clients.remove(client)
    except ValueError:
        pass
    socket = mudsocket.get_socket_by_thing(client)
    if socket:
        mudsocket.clients.pop(mudsocket)
    return True


def client_login_parser(client, line):
    """ Handle log-in for arriving players - right now, just a basic check
    against qtmud.client_accounts to see if the client is there already.
    """
    output = ''
    #####
    #
    # start login process
    #
    #####
    if not hasattr(client, 'login_stage'):
        client.login_stage = 0
        output = 'Input [desired] client name and press <enter>.'
    #####
    #
    # check if client exits
    #
    #####
    elif client.login_stage == 0:
        if line in qtmud.client_accounts.keys():
            output = ('There\'s a client named {}, if you\'re them, type your '
                      'password and press <enter>'.format(line))
            client.login_stage = 2
        elif line:
            output = ('No client named {}, going to make an account with that '
                      'name. Type your desired password and press <enter>.'
                      ''.format(line))
            client.login_stage = 1
        else:
            output = ('Your client name can\'t be blank. Input what name '
                      'you\'d like to use and press <enter>.')
        client.name = line
    #####
    #
    # register new client
    #
    #####
    elif client.login_stage == 1:
        qtmud.client_accounts[client.name] = {'password': line}
        qtmud.save_client_accounts()
        client.login_stage = 9
        output = ('Client account registered with name {}, press '
                  '<enter> to finish logging in.'.format(client.name))
    #####
    #
    # login existing account
    #
    #####
    elif client.login_stage == 2:
        if line == qtmud.client_accounts[client.name]['password']:
            client.login_stage = 9
            output = ('That\'s the correct password, press <enter> to finish '
                      'logging in.')
        else:
            client.login_stage = 0
            output = ('That\'s not the right password for that account - '
                      'type your [desired] client name and press <enter>.')
    elif client.login_stage == 9:
        client.input_parser = 'client_command_parser'
        qtmud.active_services['talker'].tune_in(channel='one', client=client)
    if output:
        qtmud.schedule('send', recipient=client, text=output)
    return True


def shutdown():
    qtmud.log.debug('shutdown() occurring')
    for client in qtmud.connected_clients:
        qtmud.schedule('client_disconnect', client=client)
    for service in qtmud.active_services:
        try:
            service.shutdown()
        except:
            pass
    while True:
        if qtmud.events:
            qtmud.log.debug('processing final events: {}'.format(qtmud.events))
            qtmud.tick()
        else:
            exit()


def client_input_parser(client, line):
    """ Pushes a client's input to their designated parser subscription.
    """
    qtmud.schedule('{}'.format(client.input_parser), client=client, line=line)
    return True


def client_command_parser(client, line):
    """ The default qtmud command parser, what client input is run through
    once they've logged in.
    """
    if line:
        command = line.split(' ')[0]
        if command in client.commands:
            client.commands[command](' '.join(line.split(' ')[1:]))
        elif command in client.channels:
            message = ' '.join(line.split(' ')[1:])
            qtmud.schedule('broadcast', channel=command,
                           speaker=client,
                           message=message)
        else:
            qtmud.schedule('send',
                           recipient=client,
                           text=('{} is not a valid command; check '
                                 '"commands" for your commands.'.format(
                                   command)))
    return True

def send(recipient, text):
    """ Prepares text to be sent to the recipient

    :param recipient: expected to be a :class:`thing <qtmud.Thing>,
                      specifically one with a send_buffer. (In qtmud, this
                      is only clients, though mudlibs may have more things
                      with send_buffers.
    :param text: the text to be appended to the recipient's send_buffer
    :return: True if text is added to recipient's send_buffer, otherwise False.
    """
    if hasattr(recipient, 'send_buffer'):
        recipient.send_buffer += '{}\n'.format(text)
        return True
    return False


