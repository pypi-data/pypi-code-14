# coding=utf-8
""" Annotation of the mention multiwords.
"""


from corefgraph.constants import FORM
import corefgraph.properties

from corefgraph.multisieve.features.baseannotator import FeatureAnnotator
from corefgraph.constants import MULTIWORD
from pynaf import NAFDocument
from socket import socket, error

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


class MultiWordAnnotator(FeatureAnnotator):
    """Annotate the type of a mention(nominal, pronominal, pronoun) also search
    some relevant features of the mention(Mention subtype)"""

    name = "multiword"
    server_ip = "127.0.0.1"
    server_port = 1337
    features = [MULTIWORD]
    retry = 3

    def __init__(self, graph_builder):
        FeatureAnnotator.__init__(self, graph_builder)

        self.server = socket()
        try:
            self.server.connect((self.server_ip, self.server_port))
            self.error = False
        except error as ex:
            self.logger.error("Error in IXA POS server: %s", ex.strerror)
            self.error = True

    def extract_and_mark(self, mention):
        """ Determine the type of the mention. Also check some mention related
        features.

        :param mention: The mention to be classified.
        """
        if self.error:
            return
        form = mention[FORM]
        if "_" in form and len(form) > 1:
            if len(self.graph_builder.get_words(mention)) == 1:
                mention[MULTIWORD] = self.expand_words(form)

    def expand_words(self, form):
        form = form.replace("_", " ")
        # TODO form += " es así."
        doc = NAFDocument(language=corefgraph.properties.lang)
        offset = 0
        for index, token in enumerate(form.split(" ")):
            doc.add_word(token.decode(corefgraph.properties.encoding), "w{0}".format(index),
                         offset=str(offset), length=str(len(token)), sent="1")
            offset += len(token) + 1
        retry = self.retry
        while retry:
            try:
                self.server.sendall(str(doc))
                retry = 0
            except error as ex:
                from time import sleep
                sleep(0.5)
                retry -= 1
                if not retry:
                    self.logger.error("Error in IXA POS server (retry exhausted): %s", ex.strerror)
        full_response = ""
        while True:
            response = self.server.recv(1024)
            full_response += response
            if not response:
                break
        naf_pos = NAFDocument(input_stream=full_response)
        return naf_pos.get_words()
