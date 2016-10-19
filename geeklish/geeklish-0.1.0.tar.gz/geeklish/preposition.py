from __future__ import print_function
from __future__ import absolute_import
import json, os
from collections import OrderedDict

class Preposition(object):
	with open(os.path.join(os.path.dirname(__file__), 'dictionary/prepositions.json')) as json_data:
		dictionary = json.load(json_data, object_pairs_hook=OrderedDict)

	def __init__(self, word, complement=None, is_wh=False):
		if type(word) == str and word in Preposition.dictionary:
			word = Preposition.dictionary[word]

		self.word = word['word']
		self.complement = complement
		self.is_wh = is_wh

	def __repr__(self):
		return '%s %s' % (self.word, self.complement) if self.complement else self.word

	def take_complement(self, complement):
		assert isinstance(complement, (Noun, Pronoun, Determiner)), \
				'%s is not a noun' % complement
		if isinstance(complement, Pronoun):
			complement.mode = 'a'
		self.complement = complement

	def get_wh(self):
		if self.is_wh:
			return (self, True)
		if self.complement:
			wh, is_wh = self.complement.get_wh()
			if is_wh:			
				self.complement = None
			if wh:
				return (wh, False)
		return (None, False)

from .noun import Noun, Pronoun, Determiner
