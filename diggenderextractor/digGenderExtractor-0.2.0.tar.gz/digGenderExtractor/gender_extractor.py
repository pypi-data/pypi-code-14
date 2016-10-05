# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-06-21 12:36:47
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-10-02 15:41:27

import copy 
import types
from digExtractor.extractor import Extractor
from digGenderExtractor.digge import DIGGE

class GenderExtractor(Extractor):

    def __init__(self):
        self.renamed_input_fields = ['text']

    def extract(self, doc):
        if 'text' in doc: 
            return DIGGE.extract(doc['text'])
        return None
        
    def get_metadata(self):
        return copy.copy(self.metadata)

    def set_metadata(self, metadata):
        self.metadata = metadata
        return self

    def get_renamed_input_fields(self):
        return self.renamed_input_fields
