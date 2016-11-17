# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-06-21 12:36:47
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-10-02 16:27:12

import copy
from digExtractor.extractor import Extractor
from dig_email_extractor import DIGEmailExtractor


class EmailExtractor(Extractor):

    def __init__(self):
        self.renamed_input_fields = ['text']
        self.dee = DIGEmailExtractor()

    def extract(self, doc):
        if 'text' in doc:
            if self.get_include_context():
                return self.dee.extract_email_with_context(doc['text'])
            else:
                return self.dee.extract_email(doc['text'])
        return None

    def get_metadata(self):
        return copy.copy(self.metadata)

    def set_metadata(self, metadata):
        self.metadata = metadata
        return self

    def get_renamed_input_fields(self):
        return self.renamed_input_fields
