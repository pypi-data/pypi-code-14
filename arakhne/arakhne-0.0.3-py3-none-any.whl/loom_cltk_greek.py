from cltk.corpus.utils.formatter import cltk_normalize
from cltk.tag.pos import POSTag

from .loom_cltk import LoomCLTK


class LoomCLTKGreek(LoomCLTK):

    def __init__(self, text):
        super().__init__(text, language='greek')

    def normalize(self):
        return self.__class__(cltk_normalize(self.data), self.language)

    def tag(self, **kwargs):
        tagger = POSTag(self.language)
        if 'mode' in kwargs:
            mode = kwargs['mode'].lower()
        else:
            mode = '123'
        if mode != '123' and mode != 'tnt' and mode != 'crf':
            print('Error: invalid part of speech tagging mode specified.')
            return False
        elif mode == '123':
            return tagger.tag_ngram_123_backoff(self.data)
        elif mode == 'tnt':
            return tagger.tag_tnt(self.data)
        else:
            return tagger.tag_crf(self.data)
