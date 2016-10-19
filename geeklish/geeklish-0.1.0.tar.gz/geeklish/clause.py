from __future__ import print_function
from __future__ import absolute_import

class Clause(object):
	def __init__(self, c_type='statement'):
		self.c_type = c_type
		self.subject = None
		self.verb = None
		self.adjective_clause = None
		self.adverbs = []
		self.conjunction = None

	def take_subject(self, subject):
		assert isinstance(subject, Determiner) and subject.independent or \
			   isinstance(subject, Pronoun) and subject.mode == 'n' or \
			   isinstance(subject, Noun), 'Not a valid subject'
		self.subject = subject

	def take_verb(self, verb):
		self.verb = verb

	def take_modifier(self, mod):
		if isinstance(mod, AdjectiveClause):
			self.adjective_clause = mod
		elif isinstance(mod, Adverb) and mod.can_modify_clause:
			self.adverbs.append(mod)
		else:
			print('Not a valid modifier.')

	def take_conjunction(self, conj):
		assert isinstance(conj, Conjunction) and conj.type == 'subordinating', \
			'Not a subordinating conjunction'
		self.conjunction = conj

	def get_verb_for_question(self, v):
		"""Except Be"""
		s = self.subject
		negative = 'not' if v.negative else ''

		if v.modal:
			head = repr(v.modal)
			if v.perfect:
				if v.passive:
					rest = [negative, 'have', 'been', v.word['passive']]
				else:
					if v.continuous:
						rest = [negative, 'have', 'been', v.word['gerund']]
					else:
						rest = [negative, 'have', v.word['passive']]
			else:
				if v.passive:
					rest = [negative, 'be', v.word['passive']]
				else:
					if v.continuous:
						rest = [negative, 'be', v.word['gerund']]
					else:
						rest = [negative, v.word['base']]
		else:
			if v.perfect:
				if v.mode == 'past':
					head = 'had'
				else:
					head = 'has' if s.is_3s() else 'have'
				if v.passive:
					rest = [negative, 'been', v.word['passive']]
				else:
					if v.continuous:
						rest = [negative, 'been', v.word['gerund']]
					else:
						rest = [negative, v.word['passive']]
			else:
				if v.passive:
					head = s.get_be(v.mode)
					if v.continuous:
						rest = [negative, 'being', v.word['passive']]
					else:
						rest = [negative, v.word['passive']]
				else:
					if v.continuous:
						head = s.get_be(v.mode)
						rest = [negative, v.word['gerund']]
					else:
						if v.mode == 'past':
							head = 'did'
						else:
							head = 'does' if s.is_3s() else 'do'
						rest = [negative, v.word['base']]

		return (head, rest)

	def get_verb(self, v):
		if v.perfect or v.continuous or v.modal or v.negative or v.passive:
			head, rest = self.get_verb_for_question(v)
			return [head] + rest
		if v.mode == 'past':
			return [v.word['past']]
		return [v.word['3s']] if self.subject.is_3s() else [v.word['base']]

	def get_be_verb(self, v):
		s = self.subject
		negative = 'not' if v.negative else ''

		if v.modal:
			head = repr(v.modal)
			if v.perfect:
				rest = [negative, 'have', 'been']
			else:
				rest = [negative, 'be']
		else:
			if v.perfect:
				if v.mode == 'past':
					head = 'had'
				else:
					head = 'has' if s.is_3s() else 'have'
				rest = [negative, 'been']
			else:
				head = s.get_be(v.mode)
				if v.continuous:
					rest = [negative, 'being']
				else:
					rest = [negative]
		return ([head], rest)

	def reorder_wh(self, clause):
		wh = None
		new_clause = []
		for i, p in enumerate(clause):
			if type(p) in [Adjective,Adverb,Preposition,Noun,Pronoun,Determiner]:
				# Search for Wh
				wh_, is_wh = p.get_wh()
				if wh_:
					wh = wh_
				if not is_wh:
					new_clause.append(p)
			else:
				new_clause.append(p)
		s = [p if type(p) == str else repr(p) for p in new_clause]
		return [repr(wh)] + s if wh else s

	def should_use_an(self, word):
		a_specials = ['us','uni','one','once','eu']
		an_specials = ['hour','honor','honest']
		for s in a_specials:
			if word.startswith(s):
				return False
		for s in an_specials:
			if word.startswith(s):
				return True
		return word[0] in 'aioeu'

	def check_article(self, clause):
		return ['an'
				if c == 'a' and self.should_use_an(clause[i+1])
				else c
				for i, c in enumerate(clause)]

	def get_clause(self):
		s = self.subject
		v = self.verb

		if self.c_type == 'command':
			negative = ['do not '] if v.negative else []
			return negative + v.get_list([v.word['base']])

		if not (s and v):
			print("You need a subject and a verb")
			return "error"
		c = s.get_list()
		if type(v) == Be:
			head, rest = self.get_be_verb(v)
			if self.c_type == 'question' and s.is_wh == False:
				return head + c + v.get_list(rest)
			else:
				return c + v.get_list(head + rest)
		if type(v) == Verb:
			if self.c_type == 'question' and s.is_wh == False:
				head, rest = self.get_verb_for_question(v)
				return [head] + c + v.get_list(rest)
			else:
				return c + v.get_list(self.get_verb(v))
		if type(v) == VerbContainer:
			last = len(v.verbs) - 1
			if self.c_type == 'question' and s.is_wh == False:
				v_type = {type(verb) for verb in v.verbs}
				assert len(v_type) == 1,"We do not support be verb and non-be verb in a question"
				assert list(v_type)[0] != Be, "We do not support multiple be verbs in a question"
				heads = []
				for i, verb in enumerate(v.verbs):
					head, rest = self.get_verb_for_question(verb)
					heads.append(head)
					c += verb.get_list(rest)
					if i != last:
						c += [v.conjunction]
				assert len(set(heads)) == 1, \
						"We do not support multiple types of verbs in a question"
				return [head] + c
			else:
				print(v.verbs)
				for i, verb in enumerate(v.verbs):
					if type(verb) == Be:
						head, rest = self.get_be_verb(verb)
						verb = verb.get_list(head + rest)
					else:
						verb = verb.get_list(self.get_verb(verb))
					c += verb
					if i != last:
						c += [v.conjunction]
				return c

	def __repr__(self):
		c = self.get_clause()
		beginnings = [adv for adv in self.verb.adverbs if adv and adv.position == 'beginning']
		c = beginnings + c

		print(c)
		c = self.reorder_wh(c)
		c = self.check_article(c)
		print(c)
		c = ' '.join([p for p in c if p])
		if self.adjective_clause:
			c = '%s, %s' % (c, self.adjective_clause)
		if self.adverbs:
			adverbs = ', '.join(str(adv) for adv in self.adverbs)
			c = '%s, %s' % (adverbs, c)
		return c


class ClauseContainer(object):
	def __init__(self):
		self.clauses = []
		self.conjunction = None
		self.c_type = self.determine_c_type()

	def take_clauses(self, clauses):
		self.clauses += clauses

	def take_conjunction(self, conjunction):
		self.conjunction = conjunction

	def determine_c_type(self):
		for c in self.clauses:
			if c.c_type == 'question':
				return 'question'
		return 'statement'

	def __repr__(self):
		if str(self.conjunction) in ['and', 'or']:
			return (' '+str(self.conjunction)+' ').join([str(s) for s in self.clauses])
		if self.conjunction:
			assert len(clauses) == 2, \
					"You cannot use %s to link more than 2 clauses." % conjunction
			return '%s %s %s' % (self.clauses[0], self.conjunction, self.clauses[1])
		# subordinating
		if self.clauses[0].conjunction:
			dependent, independent = self.clauses
			return '%s %s, %s' % (dependent.conjunction, dependent, independent)
		elif self.clauses[1].conjunction:
			independent, dependent = self.clauses
			return '%s %s, %s' % (independent, dependent.conjunction, dependent)
		else:
			assert False, 'You need a subordinating clause.'



from .adverb import Adverb
from .adjective import Adjective, AdjectiveClause
from .preposition import Preposition
from .conjunction import Conjunction
from .noun import Noun, Pronoun, Determiner
from .verb import Verb, Be, VerbContainer

