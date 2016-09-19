from collections import UserString

from nltk.text import Text
from cltk.corpus.utils.importer import CorpusImporter
from cltk.tokenize.word import nltk_tokenize_words
from cltk.tokenize.sentence import TokenizeSentence
from cltk.stem.lemma import LemmaReplacer
from cltk.stem.latin.stem import Stemmer
from nltk.util import ngrams, bigrams, trigrams, skipgrams
from cltk.tag.pos import POSTag
from cltk.stop.greek.stops import STOPS_LIST as GREEK_STOPS_LIST
from cltk.stop.latin.stops import STOPS_LIST as LATIN_STOPS_LIST
from cltk.corpus.utils.formatter import cltk_normalize
from cltk.corpus.utils.formatter import tlg_plaintext_cleanup
from cltk.stem.latin.j_v import JVReplacer
from cltk.prosody.greek.scanner import Scansion as GreekScansion
from cltk.prosody.latin.scanner import Scansion as LatinScansion
from cltk.prosody.latin.clausulae_analysis import Clausulae
from cltk.prosody.latin.macronizer import Macronizer
from cltk.text_reuse.levenshtein import Levenshtein
from cltk.text_reuse.comparison import long_substring, minhash
from cltk.tag import ner
from cltk.utils.frequency import Frequency

from .stopper import Stopper
from .scrubber import Scrubber


class CLTKLoom(UserString):
    """ Provides wrapper functions for CLTK tools

    [description]

    Methods:
        tokenize
        lemmatize
        scrub
        tlgu_cleanup
        stop_words
        scansion
        entities
        ngram
        skipgram
        compare_levenshtein
        compare_longest_common_substring
        compare_min_hash
        import_corpora

    Extends:
        UserString
    """

    def __init__(self, text, language):
        # Calling base class init
        super().__init__(str)
        # Copying passed properties
        self.data = text
        self.language = language

    def tokenize(self, mode='word'):
        """ Tokenizes text and returns list of sentences

        [description]

        Returns:
            list -- Filled with strings, each a sentence from the text
        """
        if mode == 'sentence':
            return (
                TokenizeSentence(self.language).tokenize_sentences(self.text)
            )
        else:
            return nltk_tokenize_words(self.data)

    def lemmatize(self, return_string=True):
        # Returns a CLTK lemmatized form of the text
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

    def scrub(self):
        scrubbed_text = Scrubber(self.data).scrub(self.language)
        return self.__class__(scrubbed_text)

    def tlgu_cleanup(self, **kwargs):
        # Performs cltk-included cleanup for TLG and other corpora
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

    def stop_words(self, **kwargs):
        """ Removes stopwords from text, loads file or list

        Uses the Stopper object to filter out Stopwords. If a path argument
        was specified in kwargs, attempts to open the file.

        Arguments:
            **kwargs {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        stopper = None
        path = ''
        default = True
        # Using pre-existing stopper if passed, otherwise creating
        if 'stopper' in kwargs:
            stopper = kwargs['stopper']
        if 'path' in kwargs:
                path = kwargs['path']
        if 'default' in kwargs:
                default = kwargs['default']
        if not stopper:
            stopper = Stopper(path=path)
        if default:
            if self.language == 'greek':
                stopper = stopper.add(GREEK_STOPS_LIST)
            if self.language == 'latin':
                stopper = stopper.add(LATIN_STOPS_LIST)
        return self.__class__(stopper.filter(self.data))

    def scansion(self):
        """ Scans the text into list with by line and feet

        [description]

        Returns:
            list -- List of lists, each with series of strings for each foot
        """
        if self.language == 'greek':
            return GreekScansion().scan_text(self.data)
        if self.language == 'latin':
            return LatinScansion().scan_text(self.data)

    def entities(self):
        """ Searches and returns list of entities

        [description]
        """
        return ner.tag_ner(self.language, self.data)

    def ngram(self, gram_size=3):
        # Converting text to tokens
        tokens = self.tokenize()
        # If an invalid size is sent, return False
        if gram_size < 2:
            return False
        # Using bi/trigrams for 2/3, using ngrams for larger
        if gram_size == 2:
            return bigrams(tokens)
        if gram_size == 3:
            return trigrams(tokens)
        else:
            return ngrams(tokens)

    def skipgram(self, gram_size, skip_size):
        # Converting text to tokens
        tokens = self.tokenize()
        return skipgrams(tokens, gram_size, skip_size)

    def compare_levenshtein(self, other_text):
        # Gives levenshtein distancy ratio
        return Levenshtein().ratio(self.data, other_text)

    def compare_longest_common_substring(self, other_text):
        return long_substring(self.data, other_text)

    def compare_minhash(self, other_text):
        return minhash(self.data, other_text)

    def word_count(self, style='cltk'):
        # Using NLTK Text.vocab method if specified
        if style == 'nltk':
            return Text(self.tokenize()).vocab()
        else:
            return Frequency().counter_from_str(self.data)

    def import_corpora(self):
        """
        Auto-import cltk-language related corpora
        """
        try:
            corpus_importer = CorpusImporter(self.language)
            corpora_list = corpus_importer.list_corpora
            # If no corpora were found for download
            if len(corpora_list) == 0:
                print('Error: No corpora available for download.')
            else:
                # Looping through the list and downloading each corpus
                for corpus in corpora_list:
                    try:
                        corpus_importer.import_corpus(corpus)
                        print(corpus, 'imported sucessfully.')
                    # If there is a problem getting the individual corpus
                    except:
                        print(
                            'Error: Problem importing',
                            corpus,
                            ': It may be unavailable for download'
                        )
        # If there is any problem creating the importer or listing corpora
        except:
            print('Error: Unknown error importing corpora.')


class GreekLoom(CLTKLoom):
    """[summary]

    [description]

    Methods:
        normalize
        tag

    Extends:
        CLTKLoom
    """

    def __init__(self, text):
        super().__init__(text, 'greek')

    def normalize(self):
        # Normalizes polytonic Greek, eliminated problematic character dups
        return self.__class__(cltk_normalize(self.data), self.language)

    def tag(self, **kwargs):
        """ Performs part-of-speech tagging

        Conducts one of several types of part-of-speech tagging (either
        1-2-3 gram backoff, TnT, or CRF). User specifies which by passing
        mode as '123', 'tnt', or 'crf'

        Arguments:
            **kwargs {[type]} -- [description]

        Returns:
            list -- List of tuples, each a string pair (word/pos)
        """
        # Instantiating the CLTK tagger object
        tagger = POSTag(self.language)
        # Checking if POS tagging mode was set, defaults to 123-gram pos tag
        if 'mode' in kwargs:
            mode = kwargs['mode'].lower()
        else:
            mode = '123'
        # Ensure mode set is valid
        if mode != '123' and mode != 'tnt' and mode != 'crf':
            print('Error: invalid part of speech tagging mode specified.')
            return False
        # Return respective mode tag functions
        elif mode == '123':
            return tagger.tag_ngram_123_backoff(self.data)
        elif mode == 'tnt':
            return tagger.tag_tnt(self.data)
        else:
            return tagger.tag_crf(self.data)


class LatinLoom(CLTKLoom):
    """[summary]

    [description]

    Methods:
        macronize
        clausulae
        jv_replace
        stemmify

    Extends:
        CLTKLoom
    """

    def __init__(self, text):
        super().__init__(text, 'latin')

    def macronize(self):
        return self.__class__(
            Macronizer().macronize_text(self.data),
            self.language
        )

    def clausulae(self):
        return self.__class__(
            Clausulae().clausulae_analysis(self.data),
            self.language
        )

    def jv_replace(self):
        return self.__class__(JVReplacer().replace(self.data), self.language)

    def stemmify(self):
        return self.__class__(Stemmer().stem(self.data.lower()), self.language)

#    def tag(self) # :TODO
#        pass
