from digExtractor.extractor import Extractor
import re
import copy 
import types

class RegexExtractor(Extractor):

    def __init__(self):
        super(RegexExtractor, self).__init__()
        self.renamed_input_fields = 'text'

    def get_regex(self):
        self.regex

    def set_regex(self, regex):
        if not (isinstance(regex, type(re.compile(''))) or
                isinstance(regex, types.ListType)):
            raise ValueError("regex must be a Regex or a list of Regexes")
        self.regex = regex
        return self

    def apply_regex(self, text, regex):
        extracts = list()
        for m in re.finditer(regex, text):
            if self.get_include_context():
                extracts.append(self.wrap_value_with_context(m.group(1),
                                                             'text',
                                                             m.start(),
                                                             m.end()))
            else:
                extracts.append(m.group(1))
        return extracts

    def extract(self, doc):
        try:
            if isinstance(self.regex, type(re.compile(''))):
                extracts = self.apply_regex(doc['text'], self.regex)
            elif isinstance(self.regex, types.ListType):
                extracts = list()
                for r in self.regex:
                    extracts.extend(self.apply_regex(doc['text'], r))
            if self.get_include_context():
                return (extracts)
            else:
                return list(frozenset(extracts))
        except:
            return list()

    def get_metadata(self):
        return copy.copy(self.metadata)

    def set_metadata(self, metadata):
        self.metadata = metadata
        return self

    def get_renamed_input_fields(self):
        return self.renamed_input_fields
