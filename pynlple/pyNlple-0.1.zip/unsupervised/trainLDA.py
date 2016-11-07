# -*- coding: utf-8 -*-
import codecs
import itertools
import logging

from gensim import models

from datasource.corpus import GensimFilteringTextCorpus
from module import get_abs_path as path

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# id_ = 31355
id_ = 50488

in_file = path('data\\' + str(id_) + '_17.02.2016_dump_preprocessed_filtered_noheader.txt')
# in_file = path('data\glued_dump.txt')

mention_corpus = GensimFilteringTextCorpus(in_file)
topics = 2
model_name = 'gensim_lda_' + str(id_) + '_t' + str(topics) + '.tst'
model_path = path('unsupervised\model\\' + model_name)

# model = models.LdaModel(mention_corpus, num_topics=topics, iterations=50)
# model.save(model_path)

model = models.LdaModel.load(model_path)

id2token = {y: x for x, y in mention_corpus.dictionary.token2id.iteritems()}
for topic in model.show_topics(topics, 15, False, False):
    print 'Theme #' + str(topic[0])
    for topic_keyword in topic[1]:
        string = id2token[int(topic_keyword[0])] + '*' + str(topic_keyword[1])
        print string.encode('utf8')

with codecs.open(path(in_file), 'r', 'utf8') as in_file:
    with codecs.open(path(model_name + '_tagged_documents.tsv'), 'w', 'utf8') as out_file:
        out_file.write('mention_text')
        i = 0
        while i < topics:
            out_file.write('\t')
            out_file.write(str(i))
            i += 1
        out_file.write('\r\n')
        for text_vector, text in itertools.izip(mention_corpus, in_file):
            doc_topics = model.get_document_topics(text_vector)

            topic_dict = {topic_id: prob for topic_id, prob in doc_topics}

            out_file.write(text.strip())
            t = 0
            while t < topics:
                out_file.write('\t')
                if t in topic_dict:
                    out_file.write(str(topic_dict[t]))
                else:
                    out_file.write(str(0.0))
                t += 1
            out_file.write('\r\n')
