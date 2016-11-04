# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-10-03 23:46:09
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-10-03 23:47:15

import copy
import re
from digExtractor.extractor import Extractor
import extract_drug_use


class DrugUseExtractor(Extractor):

    def __init__(self):
        self.renamed_input_fields = ['text']

    def extract(self, doc):
        if 'text' in doc:
            drug_use = self.extract_drug_use(doc['text'])

            if self.get_include_context():
                result = drug_use
            else:
                result = list()
                result.append(drug_use)
            return result

        return None

    def get_metadata(self):
        return copy.copy(self.metadata)

    def set_metadata(self, metadata):
        self.metadata = metadata
        return self

    def get_renamed_input_fields(self):
        return self.renamed_input_fields

    def extract_drug_use(self, text):
        """Returns an array of all mentions of drug use.
        Example mentions from ads:
        - she is a drug user
        - uses this money he uses it to buy drugs
        - SHE IS ON SOME HEAVY DRUGS
        - she's on drugs
        - TRAK MARKS ON ARMS
        - uses drugs during her sessions
        - provider also uses drugs
        - uses and sells drugs
        - smell like some drug she uses
        - does drugs -- negative is I don't smoke or do drugs
        - negative: I am not looking for someone who uses drugs
        - negative: no drugs
        - Shes In To Drugs
        - negative: who isn't on drugs
        - negative: I do not do drugs
        - meth head
        - crack head
        - crackhead/meth monster
        - druggie
        - junkie
        - adict
        - dopehead
        - acid freak
        - acid head
        - bag bitch
        - coke whore
        - dope whore
        - crank whore
        - pill popper

        """

        for negative in extract_drug_use.negative_regex_list:
            if re.findall(negative, text, re.I):
                return []

        result = []
        for r in extract_drug_use.regex_list:
            for m in re.finditer(r, text, re.I):
                if self.get_include_context():
                    result.append(self.wrap_value_with_context(m.group(0),
                                                               'text',
                                                               m.start(),
                                                               m.end()))
                else:
                    result.append(m.group(0))
            #result += re.findall(r, text, re.I)

        return result
