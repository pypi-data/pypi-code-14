# Command Line Achievements
# Copyright 2016 Louis Paternault
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Wrap binaries to enable achievements."""

import os
import re

from multidict import MultiDict

LONG_RE = re.compile("--(?P<option>[^=]*)(=(?P<arg>.*))?")

class Command:
    """Parse command line call, for easy access to parameters.

    .. warning::

        This class does not work, on purpose. Correctly parsing command
        line depends on each command, and implementing it correctly would
        mean re-implementing the parsing process used by every binary that
        is to be wrapped with CLAchievements. This is not going to happen.
        What is done is:

        - Any argument *not* starting with ``-`` is a positional argument.
        - Any argument starting with a single ``-`` is a list of short
          options (``-foo`` is equivalent to ``-f -o -o``). Those options
          *do not have* any arguments.
        - Any argument starting with double ``--`` is a long option. If it
          contains a ``=``, it is intepreted as an option with its
          argument; otherwise, it does not have any arguments.

    The available attributes are:

    .. attribute:: bin

        Base name of the wrapped binary (more or less equivalent to
        ``os.path.basename(sys.argv[0])``).

    .. attribute:: short

        :class:`multidict.MultiDict` of short command line arguments (that
        is, arguments starting with a single ``-``). Keys are the
        arguments, and values are the options to the arguments. See the
        warning at the beginning of the documentation of this class.

    .. attribute:: long

        :class:`multidict.MultiDict` of long command line arguments (that
        is, arguments starting with a double ``-``). Keys are the
        arguments, and values are the options to the arguments. See the
        warning at the beginning of the documentation of this class.

    .. attribute:: positional

        List of positional arguments (that is, arguments not starting with `-`).

    .. attribute:: argv

        Complete list of arguments (as one would expect from :data:`sys.argv`).

    The following doctest serves as an example.

    >>> command = Command("/usr/bin/foo tagada -bar --baz --baz=plop tsoin tsoin".split())
    >>> command.bin
    'foo'
    >>> command.short
    <MultiDict('b': None, 'a': None, 'r': None)>
    >>> command.long
    <MultiDict('baz': None, 'baz': 'plop')>
    >>> command.argv
    ['/usr/bin/foo', 'tagada', '-bar', '--baz', '--baz=plop', 'tsoin', 'tsoin']
    >>> command.positional
    ['tagada', 'tsoin', 'tsoin']
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, argv):
        self.bin = os.path.basename(argv[0])
        self.short = MultiDict()
        self.long = MultiDict()
        self.positional = []
        self.argv = argv

        for argument in argv[1:]:
            if argument.startswith("--"):
                match = LONG_RE.match(argument)
                self.long.add(
                    match.groupdict()['option'],
                    match.groupdict().get('arg', None),
                    )
            elif argument.startswith("-"):
                for option in argument[1:]:
                    self.short.add(option, None)
            else:
                self.positional.append(argument)
