from digExtractor.extractor import Extractor
import re
import copy 
import types

class RegexExtractor(Extractor):

    def __init__(self):
        self.renamed_input_fields = 'text'

    def get_regex(self):
        self.regex

    def set_regex(self, regex):
        if not (isinstance(regex, type(re.compile(''))) or isinstance(regex, types.ListType)):
            raise ValueError("regex must be a Regex or a list of Regexes")
        self.regex = regex
        return self

    def extract(self, doc):
        try:
            if isinstance(self.regex, type(re.compile(''))):
                extracts = self.regex.findall(doc['text'])        
            elif isinstance(self.regex, types.ListType):
                extracts = list()
                for r in self.regex:
                    extracts.extend(r.findall(doc['text']))
            return list(frozenset(extracts))
        except:
            return list()

    def get_metadata(self):
        return copy.copy(self.metadata)

    def set_metadata(self, metadata):
        self.metadata = metadata
        return self

    def get_renamed_input_fields(self):
        return self.renamed_input_fields;

