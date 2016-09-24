import re
from . import settings


class BaseRuleProc(object):
    ''' Base class for processing commit messages.
    '''
    # Based on pattern from https://bitbucket.org/sntran/trello-broker
    re_pattern = re.compile(r'''
        (               # start capturing the verb
        fix             # contains 'fix'
        | close         # or 'close'
        |               # or just to reference
        )               # end capturing the verb
        e?              # maybe followed by 'e'
        (?:s|d)?        # or 's' or 'd', not capturing
        \s              # then a white space
        [#]             # and '#' to indicate the card
        ([0-9]+)        # with the card's short id.
        ''',
        re.VERBOSE | re.IGNORECASE,
    )
    continue_processing = True

    def __init__(self, repo):
        self.repo = repo
        self._re_groups = None
        self._proc_cards = []

    def update(self):
        raise NotImplementedError

    def move(self):
        raise NotImplementedError

    def archive(self):
        raise NotImplementedError


class DefaultRuleProc(BaseRuleProc):
    pass
