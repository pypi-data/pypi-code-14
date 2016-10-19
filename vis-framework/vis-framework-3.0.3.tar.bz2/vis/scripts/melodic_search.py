from vis.models.indexed_piece import Importer
import pandas
import pdb
import time
import os
import vis
from numpy import nan, isnan
VIS_PATH = vis.__path__[0]

piece_path = os.path.join(VIS_PATH, 'scripts', 'pange_lingua.xml')

# v_setts = {'quality': True, 'simple or compound': 'simple', 'directed': True}
h_setts = {'quality': True, 'horiz_attach_later': True, 'simple or compound': 'compound', 'directed': True, 'mp': False}
n_setts = {'n': 4, 'continuer': 'P1', 'vertical': 'all',
           'terminator': [], 'open-ended': False, 'brackets': False}


ip = Importer(piece_path)
nr = ip.get_data('noterest')

def run_query1(melody):
	t0 = time.time()
	melodic_ngrams = ip.get_data('ngram', data=(nr,), settings=n_setts)
	results = melodic_ngrams[melodic_ngrams == melody].dropna(how='all')
	t1 = time.time()
	print('********** The query is for: ' + melody + '***********')
	print(t1-t0)
	print(results)

# without octave information:
def truncate_octaves(event):
	if isinstance(event, float):
		return event
	else:
		return(event[:-1])

def run_query2(melody):
	t0 = time.time()
	nr_no_octaves = nr.applymap(truncate_octaves)
	# query = 'A A B A'
	melodic_ngrams = ip.get_data('ngram', data=(nr_no_octaves,), settings=n_setts)
	results = melodic_ngrams[melodic_ngrams == melody].dropna(how='all')
	t1 = time.time()
	print('********** The query is for: ' + melody + ' ***********')
	print(t1-t0)
	print(results)

pdb.set_trace()

run_query1('A3 A3 B3 A3')
run_query2('A A B A')
