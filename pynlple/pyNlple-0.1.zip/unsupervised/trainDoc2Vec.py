# -*- coding: utf-8 -*-
import logging

from gensim import models
from gensim import utils
from gensim.utils import RULE_DISCARD, RULE_KEEP, RULE_DEFAULT

from datasource.corpus import DFTaggedDocumentSource
from module import get_abs_path as path


class Filter(object):

    def __init__(self, check_func):
        self.check_function = check_func
        super(Filter, self).__init__()

    def filtering_rule(self, word, count, min_count):
        if self.check_function(word):
            return RULE_KEEP
        else:
            return RULE_DISCARD
        return RULE_DEFAULT

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

theme_ids = [55950, 50488, 63941, 46681, 31355, 46770, 46771, 39969, 41734, 46773, 46777]
sorted_theme_ids = sorted(theme_ids)
key = ','.join([str(theme_id) for theme_id in sorted_theme_ids])
date = '01.04.2016'
in_file = path('data\\' + key + '_' + date + '_dump_filtered.tsv')

mention_documents = DFTaggedDocumentSource(in_file, '\t', 1, skip_first_line=True)

dimensions = 500

# check_function = Stopwords(False).is_not_a_stopword
# filter = Filter(check_function)

model_name = 'gensim_doc2vec_' + key + '_d' + str(dimensions) + '.tst'
model_path = path('unsupervised\model\\' + model_name)
# model = models.Doc2Vec(mention_documents, dm=0, size=dimensions, seed=13, window=8, min_count=3, workers=3)
# model.save(model_path)
#
model = models.Doc2Vec.load(model_path)

tokens = [u'колесо']

if all(token in model.vocab for token in tokens):
    similars = model.most_similar(tokens, topn=15)
    similar_words = [utils.any2unicode(similar_word) for similar_word, similarity in similars]
    print (', '.join(tokens) + ': ' + ', '.join(similar_words)).encode('utf8')
else:
    print ('Tokens not found.')


doc_vector = model.infer_vector(tokens)
similar_vectors = model.docvecs.most_similar([doc_vector], topn=20)

tags = [str(tag) for tag, similarity in similar_vectors]
print (', '.join(tokens) + ': ' + ', '.join(tags)).encode('utf8')
# with codecs.open(path('data\\' + str(id_) + '_' + date + '_doc2vec.tsv'), 'w', 'utf8') as out_file:
#     d = 0
#     header = ['i' + str(d) for d in range(0, dimensions)]
#     out_file.write('\t'.join(header))
#     out_file.write('\r\n')
#
#     d2 = 0
#     for doc in mention_documents:
#         doc_vector = model.docvecs[d2]
#         out_file.write('\t'.join([str(num) for num in doc_vector]))
#         out_file.write('\r\n')
#         d2 += 1
