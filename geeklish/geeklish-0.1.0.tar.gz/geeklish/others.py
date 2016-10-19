from __future__ import print_function
from __future__ import absolute_import

class To(object):
	def __init__(self):
		self.verb = None

	def take_verb(self, verb):
		assert isinstance(verb, Verb), '%s is not a verb' % verb
		self.verb = verb

	def __repr__(self):
		phrase = self.verb.verb_after_to()
		return ' '.join(['to'] + [p if type(p) == str else repr(p) for p in phrase])

def sentence(clause):
	def punctuation(c):
		return '?' if c.c_type == 'question' else '.'

	def capitalize(sentence):
		return sentence[0].upper() + sentence[1:]

	return capitalize(str(clause) + punctuation(clause))

def pritty_str(pos, word):
	dic = pos.dictionary[word]
	pretty_dic = '\n'.join(['%s => %s' % (key, val) for key, val in dic.items()])
	return '%s\n%s' % (str(pos).split(".")[-1][:-2], pretty_dic)

def search_dic(word, pos=None):
	if pos:
		if word in pos.dictionary:
			print(pritty_str(pos, word))
		else:
			print("%s is not in the dictionary." % word)
	else:
		pos_list = [Verb,Adverb,Adjective,Preposition,Conjunction,Noun,Pronoun,Determiner]
		results = [pritty_str(pos, word) for pos in pos_list if word in pos.dictionary]
		if results == []:
			print("%s is not in the dictionary." % word)
		else:
			print('\n\n'.join(results))

def same_complements(p_complements, complements):
	if len(p_complements) != len(complements):
		return False
	for p, c in zip(p_complements, complements):
		if not same_comlement(p, c):
			return False
	return True

def same_comlement(p, c):
	if p == 'N':
		if isinstance(c, Noun):
			return True
		if type(c) == Pronoun:
			return True if c.mode != 'p' else False
		if type(c) == Determiner:
			return True if c.independent else False
		if type(c) == VerbContainer:
			lyst = [c.mode == 'gerund' for v in c.verbs]
			return True if all(lyst) and len(lyst) > 0 else False
		if isinstance(c, Verb):
			return True if c.mode == 'gerund' else False
		return False
	if p == 'P':
		return True if type(c) == Preposition else False
	if p == 'To':
		return True if type(c) == To else False


from .verb import Verb, Modal, VerbContainer
from .adverb import Adverb
from .adjective import Adjective
from .preposition import Preposition
from .conjunction import Conjunction
from .noun import Noun, Pronoun, Determiner
from .others import To