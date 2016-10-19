from __future__ import absolute_import
import json, os
from collections import OrderedDict

class Conjunction(object):
	with open(os.path.join(os.path.dirname(__file__), 'dictionary/conjunctions.json')) as json_data:
		dictionary = json.load(json_data, object_pairs_hook=OrderedDict)	
	
	def __init__(self, word):
		if type(word) == str and word in Conjunction.dictionary:
			word = Conjunction.dictionary[word]

		self.word = word['word']
		self.type = word['type']

	def __repr__(self):
		return self.word