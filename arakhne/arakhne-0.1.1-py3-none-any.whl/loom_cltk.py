from nltk.text import Text
from cltk.corpus.utils.importer import CorpusImporter
from cltk.tokenize.word import nltk_tokenize_words
from cltk.tokenize.sentence import TokenizeSentence
from cltk.stem.lemma import LemmaReplacer
from cltk.corpus.utils.formatter import tlg_plaintext_cleanup
from cltk.prosody.greek.scanner import Scansion as GreekScansion
from cltk.prosody.latin.scanner import Scansion as LatinScansion
from cltk.text_reuse.levenshtein import Levenshtein
from cltk.text_reuse.comparison import long_substring, minhash
from cltk.tag import ner
from cltk.utils.frequency import Frequency

from .loom_nltk import LoomNLTK


class LoomCLTK(LoomNLTK):

    def tokenize(self, mode='word'):
        if mode == 'sentence':
            return (
                TokenizeSentence(self.language).tokenize_sentences(self.text)
            )
        else:
            return nltk_tokenize_words(self.data)

    def lemmatize(self, return_string=True):
        if len(self.data) == 0 or not self.data:
            return (
                self.__class__('')
            )
        return (
            self.__class__(
                LemmaReplacer(self.language)
                .lemmatize(self.data, return_string=return_string)
            )
        )

    def tlgu_cleanup(self, **kwargs):
        rm_punctuation = True
        rm_periods = False
        if 'rm_punctuation' in kwargs:
            rm_punctuation = kwargs['rm_punctuation']
        if 'rm_periods' in kwargs:
            rm_periods = kwargs['rm_periods']
        return self.__class__(
            tlg_plaintext_cleanup(
                self.data, rm_punctuation=rm_punctuation, rm_periods=rm_periods
            )
        )

    def scansion(self):
        if self.language == 'greek':
            return GreekScansion().scan_text(self.data)
        if self.language == 'latin':
            return LatinScansion().scan_text(self.data)

    def entities(self):
        return ner.tag_ner(self.language, self.data)

    def compare_levenshtein(self, other_text):
        return Levenshtein().ratio(self.data, other_text)

    def compare_longest_common_substring(self, other_text):
        return long_substring(self.data, other_text)

    def compare_minhash(self, other_text):
        return minhash(self.data, other_text)

    def word_count(self, style='cltk'):
        if style == 'nltk':
            return Text(self.tokenize()).vocab()
        else:
            return Frequency().counter_from_str(self.data)

    def import_corpora(self):
        try:
            corpus_importer = CorpusImporter(self.language)
            corpora_list = corpus_importer.list_corpora
            if len(corpora_list) == 0:
                print('Error: No corpora available for download.')
            else:
                for corpus in corpora_list:
                    try:
                        corpus_importer.import_corpus(corpus)
                        print(corpus, 'imported sucessfully.')
                    except:
                        print(
                            'Error: Problem importing',
                            corpus,
                            ': It may be unavailable for download'
                        )
        # If there is any problem creating the importer or listing corpora
        except:
            print('Error: Unknown error importing corpora.')
