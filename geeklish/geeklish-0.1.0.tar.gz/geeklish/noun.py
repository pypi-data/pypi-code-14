from __future__ import print_function
from __future__ import absolute_import
import json, os
from collections import OrderedDict

script_dir = os.path.dirname(__file__)

class Pronoun(object):
	with open(os.path.join(script_dir, 'dictionary/nouns/pronouns.json')) as json_data:
		dictionary = json.load(json_data, object_pairs_hook=OrderedDict)

	def __init__(self, word, mode='n', is_wh=False):
		if type(word) == str and word in Pronoun.dictionary:
			word = Pronoun.dictionary[word]

		self.word = {}
		self.word['n'] = word['n']
		self.word['a'] = word['a'] if 'a' in word else self.word['n']
		self.word['p'] = word['p'] if 'p' in word else None
		self.word['pp'] = word['pp'] if 'pp' in word else self.word['p']
		self.word['r'] = word['r'] if 'r' in word else None
		self.person = word['person'] if 'person' in word else None
		self.number = word['number'] if 'number' in word else 'singular'
		self.mode = mode
		self.is_wh = is_wh

	def __repr__(self):
		return self.word[self.mode]

	def get_list(self):
		return [self]

	def get_be(self, mode):
		if mode == 'past':
			if self.number == 'plural' or self.person == 2:
				return 'were'
			return 'was'
		else:
			if self.number == 'plural' or self.person == 2:
				return 'are'
			if self.person == 1:
				return 'am'
			return 'is'

	def is_3s(self):
		return True if self.number == 'singular' and self.person not in [1, 2] else False

	def get_wh(self):
		return (self, True) if self.is_wh else (None, False)

class Noun(object):
	with open(os.path.join(script_dir, 'dictionary/nouns/nouns.json')) as json_data:
		dictionary = json.load(json_data)

	def __init__(self, word, number='singular', mode=None, is_wh=False):
		if type(word) == str and word in Noun.dictionary:
			word = Noun.dictionary[word]

		self.word = {}
		self.type = word['type']
		self.word['singular'] = word['singular']
		self.word['plural'] = word['plural'] if 'plural' in word else word['singular']
		self.person = None

		self.word['p'] = None
		self.number = None
		self.mode = mode
		self.change_number(number)

		self.adjectives = []
		self.adjectives_after = []
		self.determiners = []
		self.prepositions = []
		self.nouns = []
		self.is_wh = is_wh

	def __repr__(self):
		return ' '.join([p if type(p) == str else repr(p) for p in self.get_list()])

	def get_list(self):
		noun = [self.word[self.mode]]
		return self.get_rest(noun)
		# if self.mode == 'p':
		# 	noun.append(self.make_possesive_form2(noun[-1]))

	def get_rest(self, noun):
		noun = self.adjectives + self.nouns + noun + self.adjectives_after + self.prepositions
		noun = self.str_determiner(noun, self.determiners)
		return noun

	def str_determiner(self, noun, determiners):
		return determiners + noun

	def take_noun(self, noun):
		assert isinstance(noun, Noun), '%s is not a noun' % noun
		assert noun.mode != 'p', \
			"The possessive noun is a determiner. Use 'take_determiner' instead."
		self.nouns.append(noun)

	def take_determiner(self, det):
		if isinstance(det, (Noun, Pronoun)):
			assert det.mode == 'p', '%s is not a possessive'
		else:
			assert det.number in [self.number, 'both'], "Determiner-Noun agreement faild."
		self.determiners.append(det)

	def take_adjective(self, adj):
		if isinstance(adj, AdjectiveClause):
			self.adjectives_after.append(adj)
		elif isinstance(adj, Adjective):
			self.adjectives.append(adj)
		elif isinstance(adj, Verb): # Participle
			assert adj['mode'] == 'gerund' or adj.passive, \
					'%s is not a participle' % adj
			if adj.complements or adj.adverb or adj.preposition:
				self.adjectives_after.append(adj)
			else:
				self.adjectives.append(adj)
		else:
			assert False, '%s is not an adjective' % adj

	def take_preposition(self, preposition):
		assert type(preposition) == Preposition, '%s is not a preposition' % preposition
		self.prepositions.append(preposition)

	def get_be(self, mode):
		if mode == 'past':
			return 'were' if self.number == 'plural' or self.person == 2 else 'was'
		return 'are' if self.number == 'plural' or self.person == 2 else 'is'

	def is_3s(self):
		return True if self.number == 'singular' and self.person not in [1, 2] else False

	def make_possesive_form(self):
		if self.number == 'singular':
			return self.word['singular'] + "'s"
		end = "'" if self.word['plural'][-1] == 's' else "'s" 
		return self.word['plural'] + end

	def change_number(self, number):
		self.number = number
		self.word['p'] = self.make_possesive_form()
		if self.mode != 'p':
			self.mode = number

	def change_mode(self, mode):
		self.mode = mode

	# def make_possesive_form2(self, word):
	# 	print([ word])
	# 	return "'s"

	def get_wh(self):
		if self.is_wh:
			return (self, True)
		if self.adjectives:
			for i, adj in enumerate(self.adjectives):
				wh, is_wh = adj.get_wh()
				if is_wh:			
					self.adjectives.pop(i)
				if wh:
					return (wh, False)
		if self.adjectives_after:
			for i, adj in enumerate(self.adjectives_after):
				wh, is_wh = adj.get_wh()
				if is_wh:
					self.adjectives_after.pop(i)
				if wh:
					return (wh, False)
		if self.determiners:
			for i, det in enumerate(self.determiners):
				wh, is_wh = det.get_wh()
				if is_wh:
					self.determiners.pop(i)
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


class Determiner(object):
	with open(os.path.join(script_dir, 'dictionary/nouns/determiners.json')) as json_data:
		dictionary = json.load(json_data)

	def __init__(self, word, is_wh=False):
		if type(word) == str and word in Determiner.dictionary:
			word = Determiner.dictionary[word]

		self.word = word['word']
		self.number = word['number']
		self.independent = word['independent']
		self.is_wh = is_wh

	def __repr__(self):
		return self.word

	def get_be(self, mode):
		if mode == 'past':
			return 'were' if self.number == 'plural' else 'was'
		return 'are' if self.number == 'plural' else 'is'

	def is_3s(self):
		return True if self.number == 'singular' else False

	def get_wh(self):
		return (self, True) if self.is_wh else (None, False)

class Number(Determiner):

	def __init__(self, number, mode='cardinal', string='symbol', is_wh=False):
		assert isinstance(number, (int, float)), '%s is not a number.' % number

		self.row_number = number
		self.mode = mode
		self.string = string

		self.word = {}
		self.word['cardinal_symbol'] = str(number)
		self.word['cardinal_word'] = self.cardinal_word(number)
		self.word['ordinal_symbol'] = self.ordinal_symbol(number)
		self.word['ordinal_word'] = self.ordinal_word(number)

		self.number = 'singular' if number == 1 or mode == 'ordinal' else 'plural'
		self.independent = True
		self.is_wh = is_wh

	def __repr__(self):
		return self.word[self.mode+'_'+self.string]

	def cardinal_word(self, number):
		pass

	def ordinal_symbol(self, number):
		if type(number) == float or number == 0:
			return None
		if number in [11, 12, 13]:
			return '%sth' % number
		number = str(number)
		if number[-1] == '1':
			return '%sst' % number
		if number[-1] == '2':
			return '%snd' % number
		if number[-1] == '3':
			return '%srd' % number
		return '%sth' % number

	def ordinal_word(self, number):
		pass


class NounContainer(Noun):
	def __init__(self, is_wh=False):
		self.person = None
		self.number = 'plural'

		self.nouns = []
		self.adjectives = []
		self.adjectives_after = []
		self.determiners = []
		self.preposition = []
		
		self.conjunction = None
		self.nouns = []
		self.is_wh = is_wh

	def take_nouns(self, nouns):
		self.nouns += nouns

	def take_conjunction(self, conjunction):
		self.conjunction = conjunction

	def get_list(self):
		return self.get_rest([repr(self.conjunction).join([repr(n) for n in self.nouns])])

	def get_be(self, mode):
		return 'were' if mode == 'past' else 'are'

	def is_3s(self):
		return False

class NounClause(Noun):
	def __init__(self, is_wh=False):
		self.clause = None
		self.person = None
		self.number = 'singular'

		self.nouns = []
		self.adjectives = []
		self.adjectives_after = []
		self.determiners = []
		self.prepositions = []
		
		self.is_wh = is_wh

	def take_clause(self, clause):
		self.clause = clause

	def get_list(self):
		return self.get_rest([self.clause])

	def get_be(self, mode):
		return 'was' if mode == 'past' else 'is'

	def is_3s(self):
		return True

from .preposition import Preposition
from .adjective import Adjective, AdjectiveClause
from .verb import Verb