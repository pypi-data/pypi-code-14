# coding=utf-8
from logging import getLogger

from corefgraph.resources.tagset import constituent_tags, ner_tags, pos_tag_set
from corefgraph.resources.dictionaries import temporals, verbs, stopwords, pronouns
from corefgraph.resources.tagset import pos_tags
from corefgraph.constants import TAG, FORM, NER, POS, ID, LEMMA, SPAN, CONSTITUENT, HEADWORD

logger = getLogger(__name__)


# TODO Check
def get_head_word_form(graph_builder,  element):
    """ Get the head of a chunk

    @param element: A syntactic element
    @return: String, the form of the word.
    """
    try:
        return element["head_word_form"]
    except KeyError:
        head = graph_builder.get_head_word(element)
        if ner_tags.mention_ner(element.get(NER)):
            # If element is a Named entity get the last word of the set
            # begin-word headword (both included) that isn't a common known
            # ne suffix
            words = graph_builder.get_words(element)
            words = words[:words.index(head) + 1]
            for word in reversed(words):
                word_form = word[FORM].replace(".", "")
                if not stopwords.common_NE_subfixes(word_form.lower()):
                    head = word
                    break
        element["head_word_form"] = head[FORM]
        return head[FORM]


# TODO Check
def is_role_appositive(graph_builder,  first_constituent, second_constituent):
    """Check if are in a role appositive construction.

    @param first_constituent:
    @param second_constituent:
    @return: True or False
    """
    if not graph_builder.same_sentence(
            second_constituent, first_constituent):
        return False
    if not (graph_builder.is_inside(
            first_constituent[SPAN], second_constituent[SPAN]) or
                graph_builder.is_inside(
                    second_constituent[SPAN], first_constituent[SPAN])):
        return False
    # If candidate or mention are NE use their constituent
    if first_constituent[graph_builder.node_type] == graph_builder.named_entity_node_type:
        first_constituent = first_constituent[CONSTITUENT]
    if second_constituent[graph_builder.node_type] == graph_builder.named_entity_node_type:
        second_constituent = second_constituent[CONSTITUENT]

    # The Candidate is headed by a noun.
    candidate_head = graph_builder.get_head_word(first_constituent)
    if not candidate_head or not pos_tags.all_nouns(candidate_head[POS]):
        return False
        # The Candidate appears as a modifier of a NP
    candidate_syntactic_father = graph_builder.get_syntactic_parent(
        first_constituent)
    if not constituent_tags.noun_phrases(candidate_syntactic_father[TAG]):
        return False
        # The NP whose head is the mention
    return second_constituent[ID] == graph_builder.get_head(
        candidate_syntactic_father)[ID]


# TODO Check
def is_relative_pronoun(graph_builder, first_constituent, second_constituent):
    """ Check if tho constituents are in relative pronoun construction.
    Also mark they.

    @param first_constituent:
    @param second_constituent:
    @return: Boolean
    """
    # NP < (NP=m1 $.. (SBAR < (WHNP < WP|WDT=m2)))
    if not graph_builder.same_sentence(
            first_constituent, second_constituent):
        return False
    if not pronouns.relative(second_constituent[FORM].lower()):
        return False
    if first_constituent[SPAN] > second_constituent[SPAN]:
        return False
    enclosing_np = graph_builder.get_syntactic_parent(
        first_constituent)

    upper = graph_builder.get_syntactic_parent(second_constituent)
    while upper and (upper[graph_builder.node_type] != graph_builder.root_type):
        if graph_builder.is_inside(
                upper[SPAN], enclosing_np[SPAN]):
            upper = graph_builder.get_syntactic_parent(upper)
        elif upper[ID] == enclosing_np[ID]:
            # TODO check path element
            return True
        else:
            return False

    return False


# TODO Check
def is_enumeration(graph_builder,  constituent):
    """ Check if the constituent is a enumeration.
    @param constituent: The constituent to check
    @return: True or False
    """
    coordination = False
    np_pre_coordination = False
    for child in graph_builder.get_syntactic_children(constituent):
        child_tag = child.get(TAG)
        if constituent_tags.noun_phrases(child_tag):
            if coordination:
                return True
            else:
                np_pre_coordination = True
        else:
            child_pos = child.get(POS)
            if pos_tags.conjunctions(child_pos) and np_pre_coordination:
                coordination = True
    return False


# TODO Check
def is_predicative_nominative(graph_builder, constituent):
    """ Check if the constituent is a predicate in a predicative nominative
    mention.

    Stanford check for the relation:
    # "S < (NP=m1 $.. (VP < ((/VB/ <
                    /^(am|are|is|was|were|'m|'re|'s|be)$/) $.. NP=m2)))";
    # "S < (NP=m1 $.. (VP < (VP < ((/VB/ <
                    /^(be|been|being)$/) $.. NP=m2))))";

    @param constituent: The mention to check
    """
    constituent = constituent.get(CONSTITUENT, constituent)
    # The constituent is in a VP that start with a copulative verb
    parent = graph_builder.get_syntactic_parent(constituent)
    if constituent_tags.verb_phrases(parent.get(TAG)):
        # Check if previous sibling is a copulative verb
        for child in graph_builder.get_syntactic_children(parent):
            if child[SPAN] < constituent[SPAN]:
                if pos_tags.verbs(child.get(POS)):
                    if verbs.copulative(child[FORM]):
                        return True
    return False


# TODO Check
def is_attributive(graph_builder, constituent):
    """ Check if the constituent is a known attributive construction

            @param constituent: The mention to check
    """
    # The constituent is in a VP that start with a copulative verb
    constituent = constituent.get(CONSTITUENT, constituent)
    root = graph_builder.get_root(constituent)
    sentence_words = graph_builder.get_words(root)
    first_word = constituent[SPAN][0] - root[SPAN][0]
    if first_word == 0:
        return False
    return sentence_words[first_word - 1][FORM] in ("of",)


# TODO Check
def is_appositive_construction_child(graph_builder, constituent):
    """ Check if the mention is in a appositive construction.

    "NP=m1 < (NP=m2 $.. (/,/ $.. NP=m3))";
    "NP=m1 < (NP=m2 $.. (/,/ $.. (SBAR < (WHNP < WP|WDT=m3))))";
    "/^NP(?:-TMP|-ADV)?$/=m1 < (NP=m2 $- /^,$/ $-- NP=m3 !$ CC|CONJP)";
    "/^NP(?:-TMP|-ADV)?$/=m1 <
                  (PRN=m2 < (NP < /^NNS?|CD$/ $-- /^-LRB-$/ $+ /^-RRB-$/))";

    @param graph_builder: The graphBuilder
    @param constituent: The mention to check
    """
    constituent = constituent.get("constituent", constituent)

    # mention is inside a NP
    # TODO Improve the precision
  
    # parent is NP
    plausible_parent = constituent
    constituent_parent = None
    while constituent_parent is None:
        plausible_parent = graph_builder.get_syntactic_parent(
            plausible_parent)
        if plausible_parent is None:
                return False
        if constituent_tags.noun_phrases(
                plausible_parent.get(TAG)):
            constituent_parent = plausible_parent

    if ner_tags.mention_ner(constituent_parent.get(NER)):
        return False
    # Search if the next brother is usable
    siblings = graph_builder.get_syntactic_sibling(
        constituent)
    position = siblings.index(constituent)
    # Search for a coma or a conjunction between mention and the end
    if position+1 < len(siblings):
        brother = siblings[position+1]
        if constituent_tags.noun_phrases(brother.get(TAG)):
            # Check if next to conjunction (or comma) exist a
            # enumerable sibling
            if graph_builder.get_words(brother)[0][FORM] == ",":

                logger.info(
                    "Mention is apposition(First Element): %s",
                    constituent[FORM])
                return True
    # Check comma or conjunction before mention and previous sibling is usable
    if position > 0:
        brother = siblings[position-1]
        if constituent_tags.noun_phrases(brother.get(TAG)):
            # Check if next to conjunction (or comma) exist a
            # enumerable sibling
            if graph_builder.get_words(constituent)[-1][FORM] == ",":
                logger.info(
                    "Mention is apposition(First Element): %s",
                    constituent[FORM])
    return False


def is_bare_np(graph_builder, constituent):
    head_word = graph_builder.get_head_word(constituent)
    head_form = head_word[FORM].lower()
    head_word_pos = head_word[POS]
    words = graph_builder.get_words(constituent)
    if pos_tags.singular_common_nouns(head_word_pos) and \
            not temporals.temporals(head_form) and (
            len(words) == 1 or pos_tags.adjective(words[0][POS])):
        logger.debug(
            "Mention is bare NP: %s(%s)", constituent[FORM], constituent[ID])
        return True
    return False


# TODO check
def is_bare_plural(graph_builder, constituent):
    """ Check if the constituent is Bare plural.
    @param constituent: The constituent to check
    @return: Boolean
    """
    span = constituent[SPAN]
    return (span[0] - span[1] == 0) and \
        pos_tags.bare_plurals(
            graph_builder.get_constituent_words(constituent)[0][POS])


# TODO CHECK
def is_pleonastic(graph_builder, constituent):
    """ Determine if the mention is pleonastic.
    @param graph_builder: The graph builder
    @param constituent: The constituent to check if is pleonastic



    """
    # NP < (PRP=m1) $..
    # Is a "it" pronoun
    if constituent_tags.noun_phrases(constituent.get(TAG)):
        pleonastic_np = constituent
    else:
        father = graph_builder.get_syntactic_parent(constituent)
        # Is a child of a NP
        if constituent_tags.noun_phrases(father[TAG]):
            pleonastic_np = father
        else:
            return False

    if pleonastic_np is None:
        return False
    siblings = graph_builder.get_syntactic_sibling(pleonastic_np)
    index = siblings.index(pleonastic_np)
    if index + 1 < len(siblings):
        if constituent_tags.adverbial_phrase(siblings[index+1].get(TAG, None)):
            return True
        if pos_tags.interrogative_pronoun(graph_builder.get_head_word(siblings[index+1]).get(POS, None)):
            return True
        if verbs.pleonastic_verbs(siblings[index+1].get(LEMMA, None)):
            return True
    if index > 0:
        if constituent_tags.preposition(siblings[index-1].get(TAG, None)):
            return True
    # Y eso que
    if index > 0 and index + 1 < len(siblings):
        prev_head = graph_builder.get_head_word(siblings[index - 1])
        next_head = graph_builder.get_head_word(siblings[index + 1])
        if prev_head["form"].lower() == 'y' and next_head['form'] == 'que':
            return True

    return False
