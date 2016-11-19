import asyncio
from discord import Member
from discord.ext import commands
from discord.errors import Forbidden, HTTPException
from ..utils import checks

class Moderation:
    """
    Commands for moderation.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.check(lambda ctx: checks.HasPermissionsOr(ctx, ban=True))
    @commands.command(no_pm=True)
    async def ban(self, member: Member):
        """Your everyday ban command."""
        try:
            await self.bot.ban(member)
        except Forbidden:
            await self.bot.say('I\'m Missing permissions')
            return
        except HTTPException:
            await self.bot.say('But it failed.')
            return
        await self.bot.say('_poof_')


    @commands.check(lambda ctx: checks.HasPermissionsOr(ctx, ban=True))
    @commands.command(no_pm=True)
    async def softban(self, member: Member):
        """Softban - A kick & prune all in one"""
        try:
            await self.bot.ban(member)
            try:
                await self.bot.unban(member)
            except:
                await asyncio.sleep(1)
                await self.bot.unban(member)
        except Forbidden:
            await self.bot.say('I\'m Missing Permissions to softban')
            return
        except HTTPException:
            await self.bot.say('But it Failed..')
            return
        await self.bot.say('_poof_')

    @commands.check(lambda ctx: checks.HasPermissionsOr(ctx, kick=True))
    @commands.command(no_pm=True)
    async def kick(self, member: Member):
        """Your typical kick command"""
        try:
            await self.bot.kick(member)
        except Forbidden:
            await self.bot.say('I\'m missing permissions to do that.')
            return
        except HTTPException:
            await self.bot.say('But it failed')
        await self.bot.say('_poof_')
