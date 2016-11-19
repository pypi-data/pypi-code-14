from discord.ext.commands import Bot
from .Core import Core
from .fun import Fun
from .Moderator import Moderation

def setup(bot: Bot):
    bot.add_cog(Core(bot))
    bot.add_cog(Fun(bot))
    bot.add_cog(Moderation(bot))
