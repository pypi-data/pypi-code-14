# -*- coding: utf-8 -*-

import logging
from os import path as p

from gensim import models

from datasource.corpus import DFTaggedDocumentSource, SentenceFilteringSource
from datasource.filesource import FileDataSource
from module import get_abs_path as path
from processing.preprocessor import *

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

replacers_stack = DefaultPreprocessorStack()

root_folder = 'E:\Data'
mentions_key = '2016.11.01'
mentions = 'mentions_preprocessed'
out_mentions = 'mentions_evaluated'
fill_na_map = {'text': ''}
data = FileDataSource.read_dataframe_from_folder(p.join(root_folder, mentions, mentions_key), '.tsv', fill_na_map=fill_na_map, encoding='utf8')
train_data = data[data['deleted'] == False]
train_data = train_data[train_data['text'] != fill_na_map['text']]
sentences = DFTaggedDocumentSource(data, 'text', text_preprocessor=None)


# root_folder = 'F:/corpora/Opensubtitles'
# file = 'OpenSubtitles2016.raw.ru'

# dash_at_start_remover = RegexReplacerAdapter(r'-\s', '', False, False, True)
# sentences = OpensubtitlesSentenceSource(FileLineSource(p.join(root_folder, file), encoding='utf8', text_preprocessor=replacers_stack), text_preprocessor=dash_at_start_remover)
n = 3
not_shorter_than_n_sentences = SentenceFilteringSource(sentences, lambda s: len(s) >= n)
key = 'mentions' + '_n' + str(n)
dimensions = 300
hs = 1
neg = 0
w_cnt_threshold = 10

params = '_d' + str(dimensions) + '_thres' + str(w_cnt_threshold) + '_hs' + str(hs) + '_neg' + str(neg)
model_name = 'gensim_word2vec_' + key + params + '.tst'
model_path = path('unsupervised\model\\' + model_name)

model = models.Word2Vec(None, size=dimensions, hs=hs, negative=neg, sg=0, cbow_mean=1, seed=13, window=5, min_count=w_cnt_threshold, iter=10, workers=3)
model.build_vocab(sentences)
model.train(sentences)
print ('First training step finished.')

model.save(model_path)
# model.save_word2vec_format(path('data\\' + str(id_) + '_word2vec.tsv'))

# model = models.Word2Vec.load(model_path)
# print ('Model ' + model_name + ' was successfully loaded.')


def normalize_a_b(num, min, max, range_a, range_b):
    return range_a + (((num - min) * (range_b - range_a)) / (max - min))


def normalize(num, min, max):
    return (num - min) / (max - min)

# score_data = data
# score_data = FileDataSource.read_dataframe_from_folder(p.join(root_folder, mentions, mentions_key), '.tsv', fill_na_map=fill_na_map, encoding='utf8')
# score_data = FileDataSource.read_dataframe(p.join(root_folder, out_mentions, mentions_key, 'all.tsv'), fill_na_map=fill_na_map, encoding='utf8')
# chars = u'йцукенгшщзхъэждлорпавыфячсмитьбюЙЦУКЕНГШЩЗХЪЭЖДЛОРПАВЫФЯЧСМИТЬБЮ'
# score_data = score_data[score_data['deleted'] == True]
# score_data = score_data[score_data['text'] != fill_na_map['text']]
# score_data = score_data[score_data['text'].apply(lambda t: any([char in t for char in chars]) and len(t) > 10)]
# score_data['log_likelihood'] = model.score(score_data.loc[:,'text'], total_sentences=len(score_data.loc[:,'text']))
# max_log = numpy.max(score_data.loc[:,'log_likelihood'])
# min_log = numpy.min(score_data.loc[:,'log_likelihood'])
# score_data['text_len'] = score_data['text'].apply(lambda t: len(t.split()))
# max_length = numpy.max(score_data.loc[:,'text_len'])
# score_data['norm_log_lh'] = (score_data.loc[:,'log_likelihood'] - max_log)
# score_data['norm_likelihood'] = numpy.exp(score_data.loc[:,'norm_log_lh']) / score_data.loc[:, 'text_len']
# score_data['log_lh_length'] = score_data.loc[:,'log_likelihood'] / score_data.loc[:,'text_len']
# max_norm_log = numpy.max(score_data.loc[:,'log_lh_length'])
# min_norm_log = numpy.min(score_data.loc[:,'log_lh_length'])
# score_data.loc[:,'norm_log_lh'] = score_data.loc[:,'norm_log_lh'] - max_norm_log
# score_data.loc[:,'norm_log_lh'] = normalize_a_b(score_data.loc[:,'log_lh_length'], min_norm_log, max_norm_log, 0, 1)
# score_data['likelihood'] = numpy.exp(score_data.loc[:,'log_lh_length'])
# min_likelihood = numpy.min(score_data.loc[:,'likelihood'])
# max_likelihood = numpy.max(score_data.loc[:,'likelihood'])
# score_data['norm_likelihood'] = normalize_a_b(score_data.loc[:,'likelihood'],
#                                               min_likelihood,
#                                               max_likelihood,
#                                               -1,
#                                               1)
# score_data['probability'] = score_data.loc[:,'likelihood'] / (1 + score_data.loc[:,'likelihood'])
# outpath = p.join(root_folder, out_mentions, mentions_key, 'all.tsv')
# score_data.to_csv(outpath, sep='\t', encoding='utf8')
#
# new_sents = [
#     [u'теперь', u'на', u'некоторых', u'станциях', u'метро', u'пассажиры', u'имеющие', u'koobeton', u'или', u'мобильный', u'телефон', u'с', u'поддержкой', u'wi', u'-', u'fi', u',', u'могут', u'войти', u'во', u'всемирную', u'паутину', u'на', u'приличной', u'скорости', u'.'],
#     [u'давно', u'ещё', u'фантазировал', u'на', u'эту', u'тему', u'-', u'мобильная', u'команда', u'с', u'koobeton', u'десантируется', u'в', u'любом', u'кафе', u'или', u'прямо', u'на', u'лавочках', u',', u'раскидывает', u'сеть', u'на', u'wi', u'-', u'fi', u'с', u'доступом', u'в', u'интернет', u'через', u'gprs', u'с', u'bluetooth', u'-', u'и', u'продолжает', u'плодотворно', u'трудиться', u'.'],
#     [u'DQTS', u'чиновники', u'россвязьохранкультуры', u'заявили', u',', u'что', u'для', u'использования', u'технологии', u'wi', u'-', u'fi', u',', u'которая', u'сейчас', u'внедрена', u'практически', u'во', u'все', u'продаваемые', u'koobeton', u',', u'коммуникаторы', u',', u'карманные', u'компьютеры', u'и', u'даже', u'многие', u'мобильные', u'телефоны', u',', u'нужно', u'специальное', u'разрешение', u'на', u'использование', u'радиочастот', u'и', u'регистрация', u'в', u'надзорной', u'службе', u'.'],
# ]
#
# model.min_count = 1
# model.iter = 100
# model.build_vocab(new_sents, update=True)
# model.train(new_sents)
# print ('Second training step finished.')

# print ('Post-training step')
# word = u'кресло'
# if word in model.vocab:
#     similars = model.most_similar([word], topn=15)
#     print (word + ': ' + ', '.join([similar[0] + '>' + str(similar[1]) for similar in similars])).encode('utf8')
# else:
#     print ('Word not found.')

# phrases = list()
# file_path = 'E:\Projects\YouScan\sentiscan\java\dict\sentiment.neg.norm'
# with codecs.open(file_path, encoding='utf-8', mode='r') as file_lines:
#     for line in file_lines:
#         phrases.append(line.strip().lower().split(' '))

# search_entities = u'coca кола,coca kola,coca cola,coca сола,koka кола,koka kola,koka cola,koka сола,koca кола,koca kola,koca cola,koca сола,coka кола,coka kola,coka cola,coka сола,кока кола,кока kola,кока cola,кока сола,соса кола,соса kola,соса cola,соса сола,"кола","колу","колой","колла","cola","colla",кокакола,кокуколу,кокукола,какакола,cocacola,kokakola,моякокакола,сосасола,cocacolarus,"@cocacolarus",#cocacolarus'
# phrases = [phrase.replace('"', '').lower().split(' ') for phrase in search_entities.split(',')]
# words = [u'nokian']

# print ('Distinct words:')
# distinct_words = set(itertools.chain(*phrases))
# for distinct_word in distinct_words:
#     if distinct_word in model.vocab:
#         similars = model.most_similar([distinct_word], topn=15)
#         similar_words = [utils.any2unicode(similar_word) for similar_word, similarity in similars]
#         filtered_similar_words = filter(lambda w: all(w not in p for p in phrases), similar_words)
#         print (distinct_word + ': ' + ', '.join(filtered_similar_words)).encode('utf8')
#     else:
#         print (distinct_word + ' - nothing found').encode('utf8')
# print ('--------------')
# print ('Phrases:')
# for phrase in phrases:
#     filtered_phrase = filter(lambda word: word in model.vocab, phrase)
#     if filtered_phrase is not None and len(filtered_phrase) > 0:
#         similars = model.most_similar(filtered_phrase, topn=15)
#         similar_words = [utils.any2unicode(similar_word) for similar_word, similarity in similars]
#         filtered_similar_words = filter(lambda w: all(w not in p for p in phrases), similar_words)
#         print (' '.join(phrase) + ': ' + ', '.join(filtered_similar_words)).encode('utf8')
#     else:
#         print (' '.join(phrase) + ' - nothing found').encode('utf8')
