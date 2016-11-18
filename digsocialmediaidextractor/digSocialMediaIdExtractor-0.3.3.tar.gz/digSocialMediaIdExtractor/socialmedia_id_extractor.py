import copy

from digExtractor.extractor import Extractor
import social_extractor

class SocialMediaIdExtractor(Extractor):

    def __init__(self, list_words_en, list_words_fr):
        self.renamed_input_fields = 'tokens'
        self.metadata = {"extractor": "SocialMediaIdExtractor"}
        self.extractor = social_extractor.SocialExtractor(list_words_en, list_words_fr, high_recall=True)

    def extract(self, doc):
        try:
            handles = None
            if 'tokens' in doc:
                tokens = doc["tokens"]
                handles = self.extractor.extract(tokens)
            return handles
        except:
            return None

    def get_metadata(self):
        """Returns a copy of the metadata that characterizes this extractor"""
        return copy.copy(self.metadata)

    def set_metadata(self, metadata):
        """Overwrite the metadata that characterizes this extractor"""
        self.metadata = metadata
        return self

    def get_renamed_input_fields(self):
        """Return a scalar or ordered list of fields to rename to"""
        return self.renamed_input_fields
