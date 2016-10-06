import collections

from markio.utils import unindent


class AnswerKey(collections.Mapping):
    """
    Represents all answer keys as a dictionary.
    """

    def __init__(self, sections):
        self._sections = sections

    def __getitem__(self, key):
        section = self._sections['answer key', key]
        return unindent(section.data)

    def __iter__(self):
        for section in self._sections:
            if section.title.casefold() == 'answer key':
                yield section.tags[0]

    def __len__(self):
        return sum(1 for _ in self)

    def __repr__(self):
        return repr(dict(self))
