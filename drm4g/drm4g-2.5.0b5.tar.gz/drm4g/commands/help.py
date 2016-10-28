from __future__ import absolute_import

#from pip.basecommand import Command
from difflib import get_close_matches

'''
This was done to add the suggestions to drm4g.
At the end it was done in another branch taken from the master -> DRM4G_suggestions
and it was implemented in bin/drm4g if i'm not mistaken
'''
class HelpCommand():
    """Show help for commands"""
    name = 'help'
    usage = """
      %prog <command>"""
    summary = 'Show help for commands.'

    commands_list = [
        'start',
        'host',
        'id',
        'job',
        'resource',
        'restart',
        'status',
        'stop',
        'clear',
        'conf'
    ]
    SUCCESS = 0

    def run(self, options, args):
        try:
            # 'pip help' with no args is handled by pip.__init__.parseopt()
            cmd_name = args[0]  # the command we need help for
        except IndexError:
            return SUCCESS

        if cmd_name not in commands_dict:
            guess = get_similar_commands(cmd_name)

            msg = ['unknown command "%s"' % cmd_name]
            if guess:
                msg.append('maybe you meant "%s"' % guess)

            raise CommandError(msg)

        return SUCCESS


    def get_similar_commands(name):
        """Command name auto-correct."""

        name = name.lower()

        close_commands = get_close_matches(name, commands_list)

        if close_commands:
            return close_commands[0]
        else:
            return False


class CommandError(Exception):
    """Raised when there is an error in command-line arguments"""
    pass
