"""Functions that read and write student and group files.

A student file contains one student name on each line.

A groups file contains a student name on each line with a blank line
between groups.
"""
from itertools import chain

from .models import Group
from .models import GroupConfig
from .models import Students


def read_students(students_file):
    r"""Read student file and return a sorted list of the students.

    >>> read_students(['A\n', 'B\n', '\n'])
    Students('A', 'B')
    """
    names = [name.strip() for name in students_file if name.strip() != '']
    return Students(*names)


def read_group_configs(group_config_file_paths):
    """Yield all historical group configs from a list of group config file
    paths.
    """
    for group_config_file_path in group_config_file_paths:
        with open(group_config_file_path) as group_config_file:
            yield read_group_config(group_config_file)


def _read_yield_group_config(group_config_file):
    r"""Yield groups from a group config file.

    >>> list(_read_yield_group_config(['A\n', 'B\n', '\n', 'C\n']))
    [Group('A', 'B'), Group('C')]
    """
    working_names = set()
    for name in map(str.strip, chain(group_config_file, [''])):
        if name != '':
            working_names.add(name)
        elif len(working_names) > 0:
            yield Group(*working_names)
            working_names = set()


def read_group_config(group_config_file):
    r"""Read a group config file.

    >>> read_group_config(['A\n', 'B\n', '\n', 'C\n'])
    GroupConfig(Group('A', 'B'), Group('C'))
    """
    return GroupConfig(*_read_yield_group_config(group_config_file))


def write_group_config(group_config, file=None):
    """Write out a group config file.

    Writes to std out by default.

    >>> write_group_config(GroupConfig(Group('A', 'B'), Group('C')))
    A
    B
    <BLANKLINE>
    C
    """
    print(
        '\n\n'.join('\n'.join(name for name in group.names)
                    for group in group_config.groups),
        file=file)
