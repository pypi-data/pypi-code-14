from __future__ import print_function
from __future__ import absolute_import
import json, os
from collections import OrderedDict

class Adverb(object):
	with open(os.path.join(os.path.dirname(__file__), 'dictionary/adverbs.json')) as json_data:
		dictionary = json.load(json_data, object_pairs_hook=OrderedDict)

	def __init__(self, word, position='before_verb', is_wh=False):
		if type(word) == str and word in Adverb.dictionary:
			word = Adverb.dictionary[word]

		self.word = word['word']
		self.can_modify_verb = "verb" in word['can_modify']
		self.can_modify_adj = "adj" in word['can_modify']
		self.can_modify_adv = "adv" in word['can_modify']
		self.can_modify_det = "det" in word['can_modify']
		self.can_modify_clause = "clause" in word['can_modify']
		self.position = position
		self.adverb = None
		self.is_wh = is_wh

	def __repr__(self):
		adv = self.word
		adv = self.str_adverb(adv, self.adverb)
		return adv

	def change_position(self, position):
		"""
		change position of adverb that modifies verb
		[beginning, before_verb, after_verb]
		"""
		self.position = position

	def str_adverb(self, adv1, adv2):
		return '%s %s' % (adv2, adv1) if adv2 else adv1

	def take_adverb(self, adverb):
		assert adverb.can_modify_adv, '%s cannot modify adverb' % adverb
		self.adverb = adverb

	def get_wh(self):
		if self.is_wh:
			return (self, True)
		if self.adverb:
			wh, is_wh = self.adverb.get_wh()
			if is_wh:			
				self.adverb = None
			if wh:
				return (wh, False)
		return (None, False)
