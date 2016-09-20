import json
import pygtrie as trie
from digExtractor.curry import curry
from digExtractor.extractor import extract
from digDictionaryExtractor.populate_trie import populate_trie
from itertools import ifilter

@curry
def dictionary_extractor(input, t, preProcess = lambda x:x, preFilter = lambda x:x, postFilter = lambda x: isinstance(x,basestring)):
	extracts = list()
	tokens = input['tokens']

	extracts.extend(ifilter(postFilter, 
		map(lambda x: t.get(x), 
			ifilter(preFilter, 
				map(preProcess, iter(tokens))))))
	return frozenset(extracts)

