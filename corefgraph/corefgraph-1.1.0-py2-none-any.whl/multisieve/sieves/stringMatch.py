# coding=utf-8
""" The sieves that check form similarity features.

"""
from logging import getLogger

from corefgraph.constants import FORM
from corefgraph.multisieve.features.constants import APPOSITIVE, MENTION
from corefgraph.multisieve.sieves.base import Sieve

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


class ExactStringMatch(Sieve):
    """ Two mentions are coreferent if their surfaces are equals."""
    short_name = "ESM"
    # Filter options
    ONLY_FIRST_MENTION = False
    NO_PRONOUN = True
    NO_STOP_WORDS = True
    DISCOURSE_SALIENCE = False

    def __init__(self, multi_sieve_processor, options):
        super(ExactStringMatch, self).__init__(multi_sieve_processor, options)
        self.logger = getLogger(__name__)

    def are_coreferent(self, entity, mention, candidate_entity, candidate):
        """ Candidate an primary mention have the same form

        @param candidate_entity: The candidate current entity.
        @param candidate: The candidate that may corefer the entity.
        @param mention: The selected mention to represent the entity.
        @param entity: The entity that is going to be evaluated.
        """
        if not super(self.__class__, self).are_coreferent(
                entity, mention, candidate_entity, candidate):
            return False
        if self.is_pronoun(candidate):
            self.logger.debug("FILTERED LINK mention pronoun")
            self.meta["Filtered_mention_pronoun"] += 1
            return False
        # TODO remove 's
        mention_x_form = mention[FORM].lower()
        mention_x_form_s = mention_x_form + " 's"
        candidate_form = candidate[FORM].lower()
        candidate_form_s = candidate_form + " 's"
        if ((mention_x_form == candidate_form) or
                (mention_x_form_s == candidate_form) or
                (candidate_form_s == mention_x_form)):
            self.logger.debug("Linked")
            self.meta["linked"] += 1
            return True
        self.meta["ignored"] += 1
        return False

    def context(self, mention_entity, mention, candidate_entity, candidate):
        """ Return a Human readable and sieve specific info string of the
        mention, the candidate and the link for logging proposes.

        @param mention_entity: The entity of the linked mention.
        @param mention: The mention.
        @param candidate_entity: The candidate entity
        @param candidate: The candidate of the link
        @return: A ready to read string.
        """
        return "{0} -{1}- | {2} -{3}- ".format(
            mention[FORM], self.graph_builder.get_root(mention)[FORM],
            candidate[FORM], self.graph_builder.get_root(candidate)[FORM])


class RelaxedStringMatch(Sieve):
    """ Two mentions are coreferent if their surfaces are similar."""
    short_name = "RSM"
    # Filter options
    NO_PRONOUN = True
    NO_STOP_WORDS = True

    def __init__(self, multi_sieve_processor, options):
        super(RelaxedStringMatch, self).__init__(multi_sieve_processor, options)
        self.logger = getLogger(__name__)

    def are_coreferent(self, entity, mention, candidate_entity, candidate):
        """ Candidate and any mention of the entity have the same relaxed form
         are coreferent.

        @param candidate_entity: The candidate current entity.
        @param candidate: The candidate that may corefer the entity.
        @param mention: The selected mention to represent the entity.
        @param entity: The entity that is going to be evaluated.
        """
        if not super(self.__class__, self).are_coreferent(
                entity, mention, candidate_entity, candidate):
            return False

        candidate_relaxed_form = self.relaxed_form(candidate)
        mention_relaxed_form = self.relaxed_form(mention)
        if mention[MENTION] == "pronoun":
            self.logger.debug("FILTERED LINK mention pronoun")
            self.meta["Filtered_mention_pronoun"] += 1
            return False
        if mention.get("enumeration", False) or \
                candidate.get("enumeration", False):
            self.logger.debug("FILTERED LINK Empty relaxed form")
            self.meta["Filtered_enumeration"] += 1
            return False
        if mention.get(APPOSITIVE, False) or candidate.get(APPOSITIVE, False):
            return False
        if candidate_relaxed_form == "":
            self.logger.debug("FILTERED LINK Empty relaxed form")
            self.meta["Filtered_relaxed_form_empty"] += 1
            return False
        if mention_relaxed_form == "":
            self.logger.debug("FILTERED LINK Empty relaxed form")
            self.meta["Filtered_relaxed_form_empty"] += 1
            return False
        if (mention_relaxed_form == candidate_relaxed_form) or \
                (mention_relaxed_form + " 's" == candidate_relaxed_form)or \
                (mention_relaxed_form == candidate_relaxed_form + " 's"):
            self.logger.debug("Linked")
            self.meta["linked"] += 1
            return True
        self.meta["ignored"] += 1
        return False
