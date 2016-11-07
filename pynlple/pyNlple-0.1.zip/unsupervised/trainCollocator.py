# -*- coding: utf-8 -*-
import codecs
import logging

from gensim.models import Phrases

from datasource.corpus import ColumnSentence
from module import get_abs_path as path

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

date = '01.04.2016'
theme_ids = [55950, 50488, 63941, 46681, 31355, 46770, 46771, 39969, 41734, 46773, 46777]
sorted_theme_ids = sorted(theme_ids)
key = ','.join([str(theme_id) for theme_id in sorted_theme_ids])
in_file = path('data\\' + key + '_01.04.2016_dump_filtered.tsv')
sentences = ColumnSentence(in_file, 1, '\t', True)

min_count = 5
threshold = 20.0

model_name = 'gensim_collocations_' + key + '_mc' + str(min_count) + '_t' + str(threshold) + '.col'
model_path = path('unsupervised\model\\' + model_name)

model = Phrases(sentences, min_count=min_count, threshold=threshold, max_vocab_size=90000000, delimiter='_')
model.save(model_path)

# model = Phrases.load(model_path)

# print (utils.any2unicode('итак'))
#

out_file = path('collocations.txt')
with codecs.open(out_file, mode='w', encoding='utf8', ) as out:
    for sent in sentences:
        out.write(' '.join(model[sent]))
        out.write('\n')


