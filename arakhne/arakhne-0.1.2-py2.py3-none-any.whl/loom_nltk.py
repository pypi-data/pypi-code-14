from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from nltk.util import ngrams, bigrams, trigrams, skipgrams

from .loom import Loom


class LoomNLTK(Loom):

    def tokenize(self, mode='word'):
        if mode == 'sentence':
            return (
                sent_tokenize(self.text)
            )
        elif mode == 'wordpunct':
            return wordpunct_tokenize(self.data)
        else:
            return word_tokenize(self.text)

    def filter_stopwords(self, stoplist):
        filtered_words = []
        tokenizer = PunktLanguageVars()
        tokens = tokenizer.word_tokenize(str(self.data).lower())
        for word in tokens:
            if word not in stoplist:
                filtered_words.append(word)
        return self.__class__(" ".join(filtered_words))

    def ngram(self, gram_size=3):
            tokens = self.tokenize()
            if gram_size < 2:
                gram_size = 2
            if gram_size == 2:
                return bigrams(tokens)
            if gram_size == 3:
                return trigrams(tokens)
            else:
                return ngrams(tokens)

    def skipgram(self, gram_size, skip_size):
        tokens = self.tokenize()
        return skipgrams(tokens, gram_size, skip_size)
