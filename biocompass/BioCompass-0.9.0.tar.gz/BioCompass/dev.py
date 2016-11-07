# -*- coding: utf-8 -*-


import re

import pandas as pd
from Bio import SeqIO

from BioCompass.BioCompass import cds_from_gbk


gb_file = '/Users/castelao/work/projects/others/BioCompass/antiSMASH_input/PAL/c00001_Moorea_...cluster001.gbk'
cds = cds_from_gbk(gb_file)

strain_id = 'PAL_001'

if strain_id is not None:
    cds['BGC'] = strain_id

# Replacing category_gen

subcluster = json.load(open('subcluster_dictionary.json'))

def get_category(product):
    for s in subcluster:
        if re.search(s, product):
            return subcluster[s]
    return 'hypothetical'


cds['category'] = cds.loc[cds['product'].notnull(), 'product'].apply(get_category)
cds['category'].fillna('hypothetical', inplace=True)





#table1_handle = open('%s_table1.csv' % strain_name, "w")
table1_handle = open('teste.csv', "w")
cds.to_csv(table1_handle, sep='\t', index=False)
table1_handle.close()


