# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-21 09:45:34
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-10-02 15:01:52

import re

######################################################################
#   Constant
######################################################################

GE_NAME = 'gender extractor'

GE_GENDER_NAME_TRANSGENDER = 'transgender'
GE_GENDER_NAME_MALE = 'male'
GE_GENDER_NAME_FEMALE = 'female'


GE_GENDER_TRANSGENDER = [
    'ts',
    'trans',
    'transgender'
]

GE_GENDER_MALE = [
    'male'
]

GE_GENDER_FEMALE = [
    'female'
]

GE_GENDER_NAMES = GE_GENDER_TRANSGENDER + GE_GENDER_MALE + GE_GENDER_FEMALE

######################################################################
#   Regular Expression
######################################################################

reg_gender_name = r'\b(?:'+r'|'.join(GE_GENDER_NAMES)+r')\b'
re_gender_name = re.compile(reg_gender_name, re.IGNORECASE)
re_tokenize = re.compile(r'[\s!\"#\$%&\'\(\)\*\+,\-\./:;<=>\?@\[\\\]\^_`{|}~]')

######################################################################
#   Main Class
######################################################################

class DIGGE(object):
    # level(hight->low): transgender, male, female

    @staticmethod
    def extract(text):
        pap = {}

        # tokenize
        text = ' '.join([_.strip() for _ in re_tokenize.split(text) if _.strip() != ''])

        # extract
        extractions = re_gender_name.findall(text)

        # normalize
        for extraction in extractions:
            if extraction in GE_GENDER_TRANSGENDER:
                pap.setdefault(GE_GENDER_NAME_TRANSGENDER, 0)
                pap[GE_GENDER_NAME_TRANSGENDER] += 1
            elif extraction in GE_GENDER_MALE:
                pap.setdefault(GE_GENDER_NAME_MALE, 0)
                pap[GE_GENDER_NAME_MALE] += 1
            elif extraction in GE_GENDER_FEMALE:
                pap.setdefault(GE_GENDER_NAME_FEMALE, 0)
                pap[GE_GENDER_NAME_FEMALE] += 1
            else:
                continue
                raise Exception(GE_NAME, 'never happen')

        # level judement
        
        if GE_GENDER_NAME_TRANSGENDER in pap.keys():
            return GE_GENDER_NAME_TRANSGENDER
        elif GE_GENDER_NAME_MALE in pap.keys():
            return GE_GENDER_NAME_MALE
        else:
            return GE_GENDER_NAME_FEMALE

