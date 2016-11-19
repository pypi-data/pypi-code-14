import discord
import asyncio
import aiohttp
from datetime import datetime
from discord.ext import commands
from ..utils.checks import IsOwner, SelfBot
from ..utils.utils import create_permissions

class Core:
    """Core Commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def on_message(self, message):
        if not SelfBot():
            return
        if message.author.id != self.bot.Config.OwnerID:
            return
        if message.content in ['afk', 'brb']:
            await self.bot.change_precense(afk=True,
                                           game=message.author.game)
            return
        if message.content == 'bk':
            await self.bot.change_precense(afk=False,
                                           game=message.author.game)
            return


    @commands.command(alias='about', pass_context=True)
    async def info(self, ctx):
        message = ['Flora 2.0a0 By Fuzen.py', 'Git: <https://github.com/Fuzen-py/Flora>']
        if not SelfBot():
            x = self.bot.user.id
            permissions = 268823638
            t = 'https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions={}'
            t = t.format(x, permissions)
            message.append(t)
        await self.bot.say('\n'.join(message))

    @commands.check(IsOwner)
    @commands.command(pass_context=True)
    async def ping(self, ctx):
        s = ctx.message.timestamp
        await self.bot.say('Pong {}'.format(datetime.utcnow() - s))

    @commands.group(pass_context=True)
    async def guilds(self, ctx):
        if ctx.invoked_subcommand is None and not IsOwner(ctx):
            await self.bot.say('Invalid criteria passed "{ctx.subcommand_passed}"'.format(ctx=ctx))
            return
        text = ['{0.name}({0.id}) | {0.owner.name}'.format(server) for server in self.bot.servers]
        text.sort()
        msg = ''
        for t in text:
            if len(msg + t) >=2000:
                try:
                    await self.bot.whisper(msg)
                    await asyncio.sleep(1)
                except discord.HTTPException:
                    pass
            msg += t + '\n'
        await self.bot.say(msg)

    @commands.check(IsOwner)
    @guilds.command(name='leave')
    async def guilds_leave(self, ctx, *servers: str):
         for server in self.bot.servers:
             if (server.id in servers) or (server.name in servers):
                 try:
                     if server.owner != self.bot.user:
                         await self.bot.leave_server(server)
                     else:
                        await self.bot.delete_server(server)
                 except discord.HTTPException:
                     pass

    @commands.check(SelfBot)
    @guilds.command(name='create')
    async def create_guild(self, name: str, region=None, icon=None):
        if icon:
            icon = None # Place Holder, Download the image link
        try:
            await self.bot.create_server(name, region=region, icon=icon)
            await self.bot.say('Server Created')
        except discord.HTTPException:
            await self.bot.say('Server Create Failed')
        except discord.InvalidArgument:
            await self.bot.say('Invallid Icon, Must Be a PNG/JPG')

    @commands.check(IsOwner)
    @commands.group(name='edit', pass_context=True)
    async def edit_bot(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid criteria passed "{ctx.subcommand_passed}"'.format(ctx=ctx))

    @edit_bot.group(name='status', pass_context=True)
    async def edit_bot_status(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid criteria passed "{ctx.subcommand_passed}"'.format(ctx=ctx))

    @edit_bot_status.command(name='game')
    async def edit_bot_status_game(self, game: str):
        presence = self.bot.user.status
        game = Game(name=game)
        await self.bot.change_presence(game=game, status=presence)

    @edit_bot_status.command(name='presence')
    async def edit_bot_status_presence(self, presence: str):
        presence = presence.lower().replace(' ', '_')
        x = ['online', 'offline', 'idle', 'dnd', 'do_not_disturb', 'invisible']
        if presence not in x:
            await self.bot.say('Status must be: {}'.format(', '.join(x)))
        status = discord.Status.__getattr__(presence)
        game = self.bot.user.game
        await self.bot.change_precense(game=game, status=status)

    @commands.has_permissions(manage_nick=True)
    @edit_bot.command('nickname', alias='nick')
    async def edit_bot_nick(self, *, nick):
        await self.bot.change_nickname(nick)

    @edit_bot.group(name='profile', pass_context=True)
    async def edit_bot_profile(self, ctx):
        if ctx.invoked_subcommand:
            return
        await self.bot.say('Invallid Subcommand Passed {}'.format(ctx.subcommand_passed))

    @edit_bot_profile.command(name='username')
    async def edit_bot_profile_username(self, *, username):
        C = self.bot.Config
        password = C.Password if C.SelfBot else None
        try:
            await self.bot.edit_profile(username=username,
                                  password=password)
        except discord.HTTPException:
            await self.bot.say('Editing Profile Failed')
            return
        except discord.ClientException:
            await self.bot.say('Invalid Password In Config\n'
                               'Edit the config and use reload')
            return
        await self.bot.say('Updated')

    @edit_bot_profile.command(name='avatar', pass_context=True)
    async def edit_profile_avatar(self,ctx, *, avatar=None):
        embeds = ctx.message.embeds
        C = self.bot.Config
        password = C.Password if C.SelfBot else None
        if avatar is None and not len(embeds):
            await self.bot.say('Umm.... what am I supposed to upload?')
            return
        if len(embeds):
            avatar = embeds[0]['url']
        with aiohttp.Clinet() as session:
            async with session.get(avatar) as re:
                try:
                    await self.bot.edit_profile(avatar=await re.read(), password=password)
                except discord.InvalidArgument:
                    await self.bot.say('Avatar was not a PNG/JPG.')
                except discord.HTTPException:
                    await self.bot.say('Failed to edit profile.')
                except discord.ClientException:
                    await self.bot.say('Invallid Password in Config'
                                       '\nedit config and use reload'
                                       'then try again')


    @commands.command(pass_context=True, no_pm=True)
    @commands.check(IsOwner)
    async def purge(self, ctx):
        message = ctx.message.content
        await self.bot.say('Are you sure you wish to do this?')
        m = await self.bot.wait_for_message(channel=message.channel, author=message.author)
        if 'yes' in m.content.lower():
            return
        counter = 0
        while True:
            try:
                x = await self.bot.purge_from(ctx.message.channel, before=ctx.message.timestamp)
            except discord.errors.Forbidden:
                await self.bot.say('I don\'t have permission to do that')
                return
            if len(x) == 0:
                break
            counter += len(x)
            await asyncio.sleep(3)
        await self.bot.reply('{} Messages Deleted'.format(counter))
