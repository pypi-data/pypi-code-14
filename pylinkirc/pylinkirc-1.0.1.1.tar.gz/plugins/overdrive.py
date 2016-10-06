from pylinkirc.log import log
from pylinkirc import utils

@utils.add_cmd
def strangle(irc, source, args):
    """strangles whatever"""
    args = ' '.join(args)
    irc.reply('\x01ACTION strangles %s\x01' % args)

@utils.add_cmd
def pls(irc, source, args):
    """<action>

    Makes the bot do something (CTCP action)."""
    args = ' '.join(args)
    irc.reply('\x01ACTION %s\x01' % args)

def lolprivmsghandler(irc, sender, command, args):
    target = args['target']
    opered = irc.isOper(sender, allowOper=False)
    chobj = irc.channels.get(target)

    if irc.name == 'ovd' and target.lower() in ('#chat', '#endlessvoid'):
        if opered and args['text'] == '!float':
            log.info('(%s) floating %s because of %s', irc.name, target, irc.getHostmask(sender))

            modes = []
            if chobj:
                pm = chobj.prefixmodes
                for uid in pm['op']:
                    modes += [('-o', uid)]
                for uid in pm['halfop']:
                    modes += [('-h', uid)]
                if modes:
                    irc.proto.mode(irc.pseudoclient.uid, target, modes)
        elif args['text'] == '!sanic':
            irc.msg(target, 'gotta go fast')
        elif opered and args['text'] in ('!clear assholes', '!clear fags'):
            for user in chobj.users:
                if irc.users[user].ident == 'nathan':
                    irc.proto.kick(irc.pseudoclient.uid, target, user, '%s used by %s' % (args['text'], irc.getHostmask(sender)))

utils.add_hook(lolprivmsghandler, 'PRIVMSG')

def loltopic(irc, source, command, args):
    target = args['channel']
    topic = args['text']
    if irc.name == 'ovd' and target.lower() in ('#chat', '#endlessvoid'):
        newtopic = topic.replace('central time is', 'pacific time is')
        newtopic = newtopic.replace('Central time is', 'Pacific time is')
        newtopic = newtopic.replace('Central Time is', 'Pacific Time is')
        newtopic = newtopic.replace('CST is', 'PST is')
        newtopic = newtopic.replace('aranzia', 'aranzia province')
        newtopic = newtopic.replace('Republic of Aranzia', 'Aranzia Province')
        if newtopic != topic:
            irc.proto.topic(irc.pseudoclient.uid, target, newtopic)
            if source in irc.users:
                irc.proto.kick(irc.sid, target, source, 'Timezone and topic integrity enforcement')

utils.add_hook(loltopic, 'TOPIC')
