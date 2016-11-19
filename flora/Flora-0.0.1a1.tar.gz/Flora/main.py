import asyncio
import datetime
import sys
import traceback

from discord import User
from discord.ext import commands

from .utils import setupstuff; del setupstuff  #  Run Then deletes it
from .commands import setup
from .utils.checks import SelfBot
from .utils.color_print import prRed
from .utils.config import Config
from .utils.values import PLUGIN_DIR, PATH

sys.path.insert(0, PATH)

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


Flora = commands.Bot(command_prefix=Config.Prefix,
                     pm_help=not Config.SelfBot,
                     self_bot=Config.SelfBot)
if Config.SelfBot:
    Flora.whisper = Flora.reply
Flora.Config = Config
Flora.Owner = User(id=Config.OwnerID)
Flora.first_ready = False
Flora.pm_owner = lambda message: Flora.send_message(Flora.Owner, message)



@Flora.event
async def on_ready():
    if Flora.first_ready:
        return
    Flora.first_ready = True
    Flora.Config.reload()
    print('[+] Online\n[!] Logged in as', Flora.user.name)
    if not SelfBot():
        await Flora.pm_owner('Hi Master\nMy Current prefix(s) are: {}\nAttempting to load other plugins.'
                             .format(Flora.Config.Prefix))
    load_fail = []
    for plugin in Flora.Config.Plugins:
        try:
            Flora.load_extension(plugin)
        except ImportError:
            load_fail.append(plugin)
    if SelfBot():
        return
    if not len(load_fail):
        return
    await Flora.pm_owner('Failed to load:\n```\n{}```\n'.format('\n'.join(load_fail)))

@Flora.event
async def on_message(message):
    if message.author.bot:
        return
    if SelfBot() and message.author.id != Flora.user.id:
        return
    if message.author.id in Flora.Config.get('Blacklist', []):
        return
    await Flora.process_commands(message)

@Flora.event
async def on_error(event,*args,**kwargs):
    Current_Time = datetime.datetime.utcnow().strftime("%b/%d/%Y %H:%M:%S UTC")
    prRed(Current_Time)
    prRed("[!][{}] Error:\n{}".format(Current_Time, traceback.format_exc()))
    error =  '```py\n{}\n```'.format(traceback.format_exc())
    if SelfBot():
        return
    await Flora.pm_owner("```py\n{}```\n{}".format(Current_Time + "\n"+ "ERROR!" + "\n", error))

@Flora.event
async def on_command_error(error, ctx):

    if isinstance(error, commands.NoPrivateMessage):
        await Flora.send_message(ctx.message.author, 'This command cannot be used in private messages.')
        return
    if isinstance(error, commands.DisabledCommand):
        await Flora.send_message(ctx.message.author, 'This Command is disabled and cannot be used')
        return
    if isinstance(error, commands.CommandOnCooldown):
        return
    if isinstance(error, commands.CommandNotFound):
        return
    Current_Time = datetime.datetime.utcnow().strftime("%b/%d/%Y %H:%M:%S UTC")
    errors = '\n'.join(traceback.format_exception(type(error), error, error.__traceback__))
    prRed("[!][{}] Error:\n{}".format(Current_Time, errors))
    if SelfBot():
        return
    errors = '```py\n{}```'.format(errors)
    await Flora.pm_owner("```py\n{}```\n{}".format(Current_Time + "\n" + "ERROR!", errors))


@commands.check(lambda ctx: ctx.message.author.id == Flora.Config.OwnerID)
@Flora.group()
async def plugin():
    pass


@plugin.command(name='load')
async def plugin_load(_plugin):
    try:
        Flora.load_extension(plugin)
    except Exception as e:
        try:
            await Flora.whisper('Error:```py\n{}\n```'.format(e))
        except:
            pass
        await Flora.say('Failed to load {}.'.format(_plugin))


@plugin.command()
async def plugin_unload(_plugin):
    try:
        await Flora.unload_extention(_plugin)
    except Exception as e:
        try:
            await Flora.whisper('Error:```py\n{}\n```'.format(e))
        except:
            pass
        await Flora.say('Failed to unload {}.'.format(_plugin))


@plugin.command()
async def reload(_plugin):
    try:
        await Flora.unload_extension(_plugin)
        await Flora.load_extention(_plugin)
    except Exception as e:
        try:
            await Flora.whisper('Error:```py\n{}\n```'.format(e))
        except:
            pass
        await Flora.say('Failed to reload {},'.format(_plugin))


@commands.check(lambda ctx: ctx.message.author.id == Flora.Config.OwnerID)
@Flora.command(name='reload')
async def reload_config():
    Flora.Config.reload()
    await Flora.say('Configuration successfully reloaded.')


@commands.check(lambda ctx: ctx.message.author.id == Flora.Config.OwnerID)
@Flora.command()
async def logout():
    await Flora.say('It\'s not like I wanted to spend time with you anyways!')
    await Flora.logout()


def run():
    setup(Flora)
    Flora.run(Config.Token, bot=not Config.SelfBot)

if __name__ == '__main__':
    run()
