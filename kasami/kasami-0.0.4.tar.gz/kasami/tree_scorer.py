import logging
import pickle
from collections import defaultdict
from math import log

logger = logging.getLogger(__name__)


class TreeScorer:
    """
    Scores a parsed sentence "tree" using a probabilistic context-free grammar
    (PCFG) strategy.  It's critical that the same parser used to create the
    `prod_freq` is again used to create the `tree`s provided to `score()`

    :Parameters:
        prod_freq : `dict` ( :class:`kasami.Production` --> `int` )
            A mapping between productions and frequency of their occurances
    """

    def __init__(self, prod_freq):
        self.prod_freq = prod_freq
        self.source_prods = defaultdict(set)
        self.source_freq = defaultdict(int)

        for prod, freq in self.prod_freq.items():
            self.source_prods[prod.source] = prod
            self.source_freq[prod.source] += freq

    def score(self, tree):
        """
        Scores a parsed sentence tree.  Note that it is critical that the same
        parser that trained the PCFG is used when producing the tree for
        scoring.

        :Parameters:
            tree : :class:`kasami.Node`
                The top node of a parse tree for a sentence.

        :Returns:
            `float` : A log(likelihood) of seeing the parse tree
        """
        probas = [self.prod_freq.get(prod, 0.5) /
                  self.source_freq.get(prod.source, 1)
                  for prod in tree]
        logger.debug("Scoring {0}:".format(tree))
        for prod, proba in zip(tree, probas):
            logger.debug(
                "\t- {0} {1}({2})"
                .format(prod, round(proba, 3), round(log(proba, 10), 3)))
        return sum(log(proba, 10) for proba in probas)

    @classmethod
    def from_tree_bank(cls, trees):
        """
        Constructs a PCFG from a tree bank.

        :Parameters:
            trees : `iterable`
                A collection of trees
        """
        prod_freqs = defaultdict(int)
        for tree in trees:
            for prod in tree:
                prod_freqs[prod] += 1

        return cls(prod_freqs)

    def dump(self, f):
        """
        Dumps the PCFG out to a file

        :Parameters:
            f : `file-like`
                A file-like object to serialize to
        """
        pickle.dump(self.prod_freq, f)

    @classmethod
    def load(cls, f):
        """
        Loads a PCFG from a file

        :Parameters:
            f : `file-like`
                A file-like object to deserialize from
        """
        prod_freq = pickle.load(f)
        return cls(prod_freq)
