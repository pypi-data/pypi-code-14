import random
from model import *
from think import learn, phrase, meaning, question, identify, tag, nextNoun, retorts
from util import randphrase
from hear import listen
from speak import say
"""
[('who', 'WP'), ('are', 'VBP'), ('you', 'PRP'), ('?', '.')]
[('who', 'WP'), ('is', 'VBZ'), ('john', 'NN'), ('?', '.')]
[('who', 'WP'), ('eats', 'VBZ'), ('cheerios', 'NNS'), ('?', '.')]
[('who', 'WP'), ('am', 'VBP'), ('i', 'RB'), ('?', '.')]
[('i', 'NN'), ('am', 'VBP'), ('mario', 'NN')]
"""

class Brain(object):
	def __init__(self, name, ear=False, retorts=True):
		self.name = name
		self.identity = identify(name)
		self.examiner = None
		say("who are you?")
		self.retorts = retorts
		if ear:
			self.ear = listen(self)

	def __call__(self, sentence):
		tagged = tag(sentence)
		if tagged[0][1] == "WP":
			return say(self.answer(sentence))
		elif sentence.startswith("tell me"):
			subject = sentence.split(" about ")[1]
			if "you" in subject:
				person = self.identity
			elif subject == "me":
				person = self.examiner
			else:
				person = identify(subject)
			content = person.content()
			if content == person.name:
				content = learn(subject, True).meaning()
			if content:
				return say(content)
			else:
				return say(randphrase("exhausted"))
		else:
			self.ingest(sentence)
			if self.retorts:
				return say(self.retort(sentence))

	def ingest(self, sentence):
		# glean information, populate topics{} and history[]
		tagged = tag(sentence)
		if len(tagged) > 1:
			if tagged[0][0] == "i" and tagged[1][0] == "am":
				desc = sentence[5:]
				if not self.examiner:
					self.examiner = identify(nextNoun(tagged[2:]))
				elif not self.examiner.summary:
					self.examiner.summary = desc
				else:
					self.examiner.description = "%s %s"%(self.examiner.description, desc)
				self.examiner.qualifiers.append(phrase(desc).key)
				self.examiner.put()
				q = question("who am i?")
				q.answers.append(self.examiner.key)
				q.put()
				say("hello %s"%(self.examiner.name,))
				# what's going on here? no qualifiers???
				if self.examiner.qualifiers: # should ALWAYS be qualifiers :-\
					qual = random.choice(self.examiner.qualifiers).get().content()
					qper = []
					for (qword, qpos) in tag(qual):
						if qpos == "PRP":
							qword = "you"
						elif qpos == "PRP$":
							qword = "your"
						qper.append(qword)
					say(" ".join(qper))
			elif "because" in sentence:
				event, reason = sentence.split(" because ")
				Reason(person=self.examiner and self.examiner.key, name=event, reason=phrase(reason)).put()
				say("ok, so %s because %s?"%(event, reason))
			elif tagged[0][1].startswith("NN"):
				if tagged[1][0] in ["is", "are"]: # learn it!
					meaning(tagged[0][0], " ".join([w for (w, p) in tagged[2:]]))
					say(randphrase("noted"))
				else:
					pass # handle other verbs!!

	def clarify(self, sentence):
		return randphrase("what")

	def answer(self, sentence):
		q = question(sentence)
		if not q.answers:
			tagged = tag(sentence)
			if tagged[0][0] == "who":
				if tagged[1][0] in ["is", "are"]:
					if tagged[2][0] == "you":
						q.answers.append(self.identity.key)
					else:
						q.answers.append(identify(nextNoun(tagged[2:])).key)
				elif tagged[1][0] == "am":
					return "i don't know. who are you?"
				else:
					return randphrase("what")
			elif tagged[0][0] == "what":
				if tagged[1][0] in ["is", "are"]:
					obj = learn(nextNoun(tagged[2:]), True)
					meanings = obj.meanings()
					if not meanings:
						return "%s. what does %s mean to you?"%(randphrase("unsure"), obj.word)
					q.answers.append(meanings[0].key)
				else:
					return randphrase("what")
			elif tagged[0][0] == "why":
				return "nevermind the whys and wherefores!"# placeholder
				# TODO: first check reason. then... something?
			else: # when/why: yahoo answers api. where: google maps api?
				return randphrase("what")
			q.put()
		return random.choice(q.answers).get().content()

	def retort(self, sentence):
		retz = retorts.keys()
		random.shuffle(retz)
		for r in retz:
			v = retorts[r](sentence)
			if v:
				v = v.replace(self.identity.name, "i")
				return self.examiner and v.replace(self.examiner.name, "you") or v