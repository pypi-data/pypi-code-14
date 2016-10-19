from __future__ import print_function
from __future__ import absolute_import
import json, os
from collections import OrderedDict

script_dir = os.path.dirname(__file__)

class Verb(object):
	with open(os.path.join(script_dir, 'dictionary/verbs/verbs.json')) as json_data:
		dictionary = json.load(json_data, object_pairs_hook=OrderedDict)

	def __init__(self, word, mode='base', negative=False, continuous=False,
					perfect=False, passive=False):
		if type(word) == str and word in Verb.dictionary:
			word = Verb.dictionary[word]

		self.word = {}
		self.word['base'] = word['base']
		self.word['3s'] = word['3s']
		self.word['past'] = word['past']
		self.word['passive'] = word['passive'] if 'passive' in word else self.word['past']
		self.word['gerund'] = word['gerund']
		self.valid_complements = word['complements']
		
		self.mode = mode # base, past, gerund
		self.negative = negative
		self.continuous = continuous
		self.perfect = perfect
		self.passive = passive
		self.modal = None

		self.complements = []
		self.predicate = None
		self.adverbs = []
		self.prepositions = []

	def take_complement(self, complement):
		"""Used for action verb"""		
		if type(complement) == Pronoun:
			complement.mode = 'a'
		self.complements.append(complement)

	def take_adverb(self, adverb):
		assert adverb.can_modify_verb, '%s cannot modify a verb' % adverb
		self.adverbs.append(adverb)

	def take_predicate(self, predicate):
		"""Used for linking verb"""
		assert type(predicate) in [Noun, Pronoun, Adjective], \
				'%s cannot be a predicate' % predicate
		self.predicate = predicate

	def take_preposition(self, preposition):
		"""Used for both action and linking verb"""
		assert type(preposition) == Preposition, \
				'%s is not a preposition' % preposition
		self.prepositions.append(preposition)

	def take_modal(self, modal):
		"""Used for both action and linking verb"""
		assert type(modal) == Modal, '%s is not a modal' % modal
		self.modal = modal

	def __repr__(self):
		verb = self.get_list([self.word[self.mode]])
		return ' '.join([p if type(p) == str else repr(p) for p in verb])

	def verb_after_to(self):
		# to talk
		return self.get_list(self.make_verb())

	def make_verb(self):
		negative = ['not'] if self.negative else []
		if self.perfect:
			return negative + ['have', self.word['passive']] 
		if self.passive:
			return negative + ['be', self.word['passive']] 
		if self.continuous:
			return negative + ['be', self.word['gerund']]
		return negative + [self.word['base']]

	def get_list(self, verb):
		assert self.has_valid_complements(), \
				"The complements of the verb '%s' is not valid." % (self.word['base'])
		verb = verb + self.complements
		verb = verb + [self.predicate] if self.predicate else verb
		verb = self.str_adverbs(verb, self.adverbs)
		verb = verb + self.prepositions
		return verb

	def str_adverbs(self, verb, adverbs):
		if not adverbs:
			return verb
		before = []
		after = []
		for adv in adverbs:
			if adv.position == 'before_verb':
				before.append(adv)
			elif adv.position == 'after_verb':
				after.append(adv)
		return before + verb + after

	def change_mode(self, mode):
		self.mode = mode

	def has_valid_complements(self):
		if self.valid_complements == [] and self.complements == []:
			return True
		if self.passive:
			return True
		for p in self.valid_complements:
			if same_complements(p, self.complements):
				return True
		return False


class Be(Verb):
	def __init__(self, mode='base'):
		self.word = {}
		self.word['base'] = 'be'
		self.word['1s'] = 'am'
		self.word['3s'] = 'is'
		self.word['plural'] = 'are'
		self.word['past_s'] = 'was'
		self.word['past_p'] = 'were'
		self.word['past'] = None
		self.word['passive'] = None
		self.word['gerund'] = 'being'
		self.valid_complements = []

		self.mode = mode
		self.negative = False
		self.modal = None
		self.perfect = False
		self.continuous = False

		# never be used
		self.passive = False

		self.complements = []
		self.adverbs = []
		self.predicate = None
		self.prepositions = []



class Modal(object):
	with open(os.path.join(script_dir, 'dictionary/verbs/modals.json')) as json_data:
		dictionary = json.load(json_data, object_pairs_hook=OrderedDict)

	def __init__(self, word):
		if type(word) == str and word in Modal.dictionary:
			word = Modal.dictionary[word]

		self.word = word['word']

	def __repr__(self):
		return self.word


class VerbContainer(Verb):
	def __init__(self):
		self.verbs = []
		self.conjunction = None

		self.valid_complements = None
		
		self.mode = None # Is this needed?
		self.negative = False
		self.continuous = False
		self.perfect = False
		self.passive = False
		self.modal = None

		self.complements = []
		self.adverbs = []
		self.predicate = None
		self.prepositions = []

	def take_verbs(self, verbs):
		self.verbs += verbs

	def take_conjunction(self, conjunction):
		self.conjunction = conjunction

	def __repr__(self):
		verb = self.get_list(' %s ' % (self.conjunction).join(str(v) for v in self.verbs))		
		return ' '.join([p if type(p) == str else repr(p) for p in verb])

	# def get_list(self):
	# 	return


from .adverb import Adverb
from .adjective import Adjective
from .preposition import Preposition
from .conjunction import Conjunction
from .noun import Noun, Pronoun, Determiner
from .others import same_complements