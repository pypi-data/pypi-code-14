from ..utils import errors
from ..utils.checks import ServerOwner, SelfBot
if not SelfBot():
    raise errors.SelfBot('Not Supported by Greet Plugin')
import sqlite3
import sys
from os import path
from discord.ext import commands
from ..utils.values import DB
class Greeter:
    def __init__(self, bot):
        self.conn = sqlite3.connect(DB)
        self.c = self.conn.cursor()
        self.bot = bot
        try:
            self.c.execute('SELECT * FROM Greetings')
        except (sqlite3.OperationalError):
            self.c.execute('''CREATE TABLE Greetings
                              (server_id text, join_message text, leave_message text, joinenabled real, leave_enabled real)''')
            self.conn.commit()
    def __del__(self):
        self.conn.commit()
        self.conn.close()

    async def on_member_join(member):
        server = member.server
        # Check if join message is enabled and Use it
        return

        await self.bot.send_message(member,)




if __name__ == '__main__':
    Greeter(None)
