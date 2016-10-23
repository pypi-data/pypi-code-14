from .corpus import Corpus
from .io import IO
from .doc import Doc


class Arakhne:
    language = None
    stopwords = None

    def __init__(
        self, language=None, title=None, stopwords=[], corpus=None
    ):
        self.filepath = None
        self.corpus = None
        self.language = language
        self.title = title
        self.stopwords = stopwords
        if corpus:
            self.corpus = corpus
        else:
            self.corpus = Corpus(
                language=self.language, title=self.title,
                stopwords=self.stopwords
            )

    def load_csv(
        self, filepath, text_col='text', stopwords=None, encoding='utf-8',
        pathtype='relative'
    ):
        documents = []
        file = None
        self.filepath = filepath
        self.encoding = encoding
        self.pathtype = pathtype
        # Loading stopwords, if specified
        if stopwords:
            self.stopwords = IO(
                filepath=stopwords,
                encoding=self.encoding,
                pathtype=self.pathtype,
                mode='load'
            ).stopwords()
        # Load the main data file
        file = IO(
            self.filepath,
            encoding=self.encoding,
            pathtype=self.pathtype,
            mode='load'
        ).csv(text_col=text_col)
        # Create doc object from each record and append to the list
        for record in file:
            documents.append(
                Doc(record['text'], record['metadata']).make(self.language)
            )
        # Load Doc objects into .corpus
        self.corpus = self.corpus.make(documents)
        return self

    def save_csv(self, filepath, overwrite=False):
        return IO(
            filepath=filepath,
            encoding=self.encoding,
            pathtype=self.pathtype,
            mode='save',
            overwrite=overwrite
        ).csv()

    def folder(self, stopwords=None, encoding='utf-8'):
        pass

    def document(self, stopwords=None, encoding='utf-8'):
        pass

    def plain_text(self, text, stopwords=None):
        pass
