from arakhne.corpus import Corpus
from arakhne.io import IO
from arakhne.doc import Doc


class Arakhne:
    language = None
    stopwords = None

    def __init__(self, language=None, title=None, stopwords=None, corpus=None):
        self.path = None
        self.corpus = None
        self.language = language
        self.title = title
        self.stopwords = IO(path=stopwords).stopwords()
        if corpus:
            self.corpus = corpus
        else:
            self.corpus = Corpus(
                language=self.language, title=self.title,
                stopwords=self.stopwords
            )

    def csv(self, path, text_col='Text', encoding='utf-8', stopwords=None):
        documents = []
        file = None
        self.path = path
        self.encoding = encoding
        if stopwords:
            self.stopwords = IO(path=stopwords).stopwords()
        file = IO(self.path).csv(text_col=text_col)
        for record in file:
            doc = Doc(record['text'], record['metadata']).make(self.language)
            documents.append(doc)
        self.corpus = self.corpus.make(documents)
        return self

    def folder(self, stopwords=None, encoding='utf-8'):
        pass

    def document(self, stopwords=None, encoding='utf-8'):
        pass

    def plain_text(self, text, stopwords=None):
        pass
