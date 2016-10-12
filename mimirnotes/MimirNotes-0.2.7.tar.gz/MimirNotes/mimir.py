import click
from enum import Enum

from MimirNotes.mimir_handler import MimirHandler


class Actions(Enum):
    init = 1
    delete = 2
    new = 3
    status = 4
    edit = 5


@click.command()
@click.argument('action', nargs=-1)
@click.option('-s', nargs=1, type=int)
def cli(s=None, action=None):
    actions = Actions
    handler = MimirHandler()

    # Check if the 'show' option was provided. If so, show that many notes, and return
    if s is not None and s >= 0:
        handler.handle('show', num=s)
        return

    if len(action) == 1:
        action = action[0]
        try:
            if action in actions.__members__:
                if action == 'delete':
                    if click.confirm('Are you sure you wish to delete any mimirs found?'):
                        handler.handle(action)
                else:
                    handler.handle(action)
            else:
                raise KeyError('Action not defined!')
        except KeyError as ex:
            # Assume here that user wants a one word note, and record it
            handler.handle('new', note=action)
    elif len(action) > 0:
        # If multiple arguments were passed in, but no specific actions were called, assume no specific action,
        # and create a note instead.
        handler.handle('new', note=action)
    else:
        # If we made it here, then mimir is confused as to how to handle the users input. Alert them to this.
        if len(action) is 0 and s is None:
            handler.handle('editor_new')
        else:
            invalid_action()


def invalid_action():
    """
    Let the user know that they have done something invalid that mimir does not know how to handle
    :return:
    """
    actions = Actions

    print 'Invalid action supplied'

    valid = ''
    for action in actions:
        valid += action.name + ' '

    print 'Valid actions: {}'.format(valid)
    print 'Run \'mimir --help\' for more information'

