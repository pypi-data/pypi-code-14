from discord.ext.commands import command
from random import choice

class Fun:

    def __init__(self, bot):
        self.bot = bot

    @command(name='8ball')
    async def eight_ball(self, text):
        x = ['Probably not', 'Maybe', 'HEH', ':smirk:', 'Not a chance', '... Did you really just ask that?'
             'Sorry, I can\'t hear you over the sound of no one caring!', 'oboi',
             'Yes', 'Defiantly', 'Please Insert Coin', 'Ask me again later', 'Go away', 'Without a doubt',
             'Maybe...']
        await self.bot.reply(':8ball: | {}'.format(choice(x)))

