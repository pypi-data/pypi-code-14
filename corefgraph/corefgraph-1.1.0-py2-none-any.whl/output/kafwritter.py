# coding=utf-8
""" Store the document in a KAF format(2.1).
"""
from corefgraph.constants import FORM, LEMMA, POS, ID
from corefgraph.output.basewriter import BaseDocument
from pynaf import KAFDocument
import os
import time

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


class KafDocument(BaseDocument):
    """ Store the document in a KAF format(2.1).
    """
    short_name = "KAF"
    time_format = "%Y-%m-%dT%H:%M:%S"

    def store(self, graph, encoding, language,
              version="1.2",
              linguistic_parsers_name="corefgraph",
              linguistic_parsers_version="1.0",
              linguistic_parsers_layer="coreference",
              start_time=None,
              end_time=None,
              hostname=os.uname()[1],
              **kwargs):
        """ Store the graph in a string and return it.
        @param graph: the graph to be stored.
        @param language: The language code inserted into the kaf file
        @param version: The version of corefgraph set on kaf
        @param encoding: Encoding set on kaf document
        @param linguistic_parsers_name: The linguistic parser name added to kaf header.
        @param linguistic_parsers_layer: The linguistic parser layer added to kaf header.
        @param linguistic_parsers_version: The linguistic parser version added to kaf header.
        @param start_time: Add a mocked start time.
        @param end_time: Add a mocked end time.
        @param hostname: Set a mocked hostname.
        @param kwargs: Unused
        """
        if not start_time:
            start_time = time.strftime(self.time_format, time.time()),
        if not end_time:
            end_time = time.strftime(self.time_format, time.time()),

        graph_builder = graph.graph["graph_builder"]

        # Check if graph contains a pre generated kaf
        try:
            previous_kaf = graph.graph["kaf"]
        except KeyError:
            previous_kaf = None

        if previous_kaf:
            kaf_document = previous_kaf
            kaf_document.add_linguistic_processors(
                layer=linguistic_parsers_layer,
                name=linguistic_parsers_name,
                version=linguistic_parsers_version,
                begin_timestamp=start_time,
                end_timestamp=end_time,
                hostname=hostname)
            for coref_index, entity \
                    in enumerate(graph_builder.get_all_coref_entities(graph), 1):
                references = [
                    [
                        word[ID].split("#")[0]
                        for word
                        in graph_builder.get_words(mention)]
                    for mention
                    in graph_builder.get_all_entity_mentions(entity)]
                kaf_document.add_coreference(
                    "co{0}".format(coref_index), references)

        else:
            kaf_document = KAFDocument(language=language, version=version)

            words_graphs = graph_builder.get_word_graph(graph)
            kaf_document.add_linguistic_processors(
                layer=linguistic_parsers_layer,
                name=linguistic_parsers_name,
                version=linguistic_parsers_version,
                begin_timestamp=start_time,
                end_timestamp=end_time,
                hostname=hostname)

            word_index = 1
            terms_ids = dict()

            for (term_index, graph_word) \
                    in enumerate(words_graphs.vertices(), 1):
                kaf_words = graph_word[FORM].split(" ")
                words_ids = []
                for word in kaf_words:
                    word_id = "w{0}".format(word_index)
                    kaf_document.add_word(word, word_id, lemma=word[LEMMA])
                    words_ids.append(word_id)
                    word_index += 1
                term_id = "t{0}".format(term_index)
                terms_ids[graph_word] = term_id
                kaf_document.add_term(
                    tid=term_id, pos=graph_word[POS], words=words_ids)

            for coref_index, entity \
                    in enumerate(graph_builder.get_all_coref_entities(graph), 1):
                references = [
                    ([
                        terms_ids[word]
                        for word
                        in graph_builder.get_words(mention)], mention[FORM])
                    for mention
                    in graph_builder.get_all_entity_mentions(entity)]
                kaf_document.add_coreference(
                    "co{0}".format(coref_index), references)

        kaf_document.write(self.file, encoding=encoding)
        return kaf_document
