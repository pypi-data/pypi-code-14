from __future__ import print_function
from __future__ import absolute_import
import json, os
from collections import OrderedDict

class Adjective(object):
	with open(os.path.join(os.path.dirname(__file__), 'dictionary/adjectives.json')) as json_data:
		dictionary = json.load(json_data, object_pairs_hook=OrderedDict)
	
	def __init__(self, word, mode='base', is_wh=False):
		if type(word) == str and word in Adjective.dictionary:
			word = Adjective.dictionary[word]

		self.word = {}
		self.word['base'] = word['base']
		self.word['comparative'] = word['comparative'] \
			if 'comparative' in word else "more "+ word['base']
		self.word['superlaive'] = word['superlaive'] \
			if 'superlaive' in word else "most "+ word['base']
		self.mode = mode
		self.adverbs = []
		self.prepositions = []
		self.is_wh = is_wh

	def __repr__(self):
		adj = self.word[self.mode]
		adj = self.str_adverb(adj, self.adverbs)
		adj = self.str_preposition(adj, self.prepositions)
		return adj

	def str_adverb(self, adj, advs):
		if advs == []:
			return adj
		return ' '.join([repr(a) for a in advs]) +' '+ adj

	def take_adverb(self, adverb):
		assert adverb.can_modify_adj, '%s cannot modify a verb' % adverb
		self.adverbs.append(adverb)

	def str_preposition(self, adj, preps):
		if preps == []:
			return adj
		return adj +' '+ ' '.join([repr(a) for a in preps])

	def take_preposition(self, preps):
		self.prepositions.append(preps)

	def get_wh(self):
		if self.is_wh:
			return (self, True)
		if self.adverbs:
			for i, adv in enumerate(self.adverbs):
				wh, is_wh = adv.get_wh()
				if is_wh:			
					self.adverbs.pop(i)
				if wh:
					return (wh, False)
		if self.prepositions:
			for i, prep in enumerate(self.prepositions):
				wh, is_wh = prep.get_wh()
				if is_wh:
					self.prepositions.pop(i)
				if wh:
					return (wh, False)
		return (None, False)

class AdjectiveClause(Adjective):
	def __init__(self):
		self.clause = clause
		self.is_wh = False

	def take_clause(self, clause):
		self.clause = clause

	def __repr__(self):
		return str(self.clause)

from .preposition import Preposition
from .conjunction import Conjunction
from .noun import Noun, Pronoun, Determiner
from .clause import Clause