from cltk.prosody.latin.clausulae_analysis import Clausulae
from cltk.prosody.latin.macronizer import Macronizer
from cltk.stem.latin.j_v import JVReplacer
from cltk.stem.latin.stem import Stemmer

from .loom_cltk import LoomCLTK


class LoomCLTKLatin(LoomCLTK):
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
        super().__init__(text, language='latin')

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
