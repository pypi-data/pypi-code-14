import wikipedia, nltk, random
from commands import getoutput
from cantools.util import log, error
from model import *
from util import randphrase

def load_corpora():
	for item in ["maxent_ne_chunker", "words", "averaged_perceptron_tagger", "punkt"]:
		nltk.download(item)

load_corpora()

def learn(word, deep=False):
	w = Word.query(Word.word == word).get()
	if w:
		log("found %s"%(word,))
	else:
		log("learning %s"%(word,))
		w = Word(word=word)
		w.put() # for recursion...
	puts = []
	if deep and not w.meanings(True):
		o = getoutput('dict -d wn "%s"'%(word,))
		if not o.startswith("No"):
			padded = "\n\n  %s\n      "%(word,)
			if padded in o:
				o = o.split(padded)[1]
			else:
				o = o.split("\n\n  %s\n      "%(word.title(),))[1]
			dz = o.replace("\n%s"%(" " * 13,), " ").replace("\n%s"%(" " * 11,),
				" ").replace("\n%s"%(" " * 9,), " ").split("\n      ")
			for d in dz:
				if not d[0].isdigit(): # new part
					part, d = d.split(" ", 1)
				m = Meaning(part=part)
				d = d.split(": ", 1)[1]
				if " [ant: {" in d:
					d, aline = d.split(" [ant: {")
					antz = aline[:-2].split("}, {")
					m.antonyms = [wordorphrase(aword).key for aword in antz]
				if " [syn: {" in d:
					d, sline = d.split(" [syn: {")
					synz = sline[:-2].split("}, {")
					m.synonyms = [wordorphrase(sword).key for sword in synz]
				m.definition = d
				puts.append(m)
		if not w.meanings(True):
			puts.append(Meaning(definition=wsum(w.word), synonyms=[w.key]))
	puts and db.put_multi(puts)
	return w

def phrase(p):
	pent = Phrase.query(Phrase.phrase == p).get()
	if not pent:
		stripped = [c for c in p if c.isalpha() or c.isspace()]
		pent = Phrase(phrase=p, words=[learn(w).key for w in "".join(stripped).split(" ")])
		pent.put()
	return pent

def wordorphrase(s):
	return " " in s and phrase(s) or learn(s)

def meaning(q, a):
	m = Meaning(synonyms=[wordorphrase(q).key], definition=a)
	m.put()
	return m

def question(q):
	p = phrase(q)
	return Question.query(Question.phrase == p.key).get() or Question(phrase=p.key)

def wsum(name):
	try:
		return wikipedia.summary(name)
	except wikipedia.DisambiguationError, e:
		return wikipedia.summary(str(e).split("\n")[1])
	except Exception, e:
		return None

def research(person):
	summary = wsum(person.name)
	if summary:
		person.description = summary
		person.summary = person.description.split("\n")[0]
		person.qualifiers = [phrase(p).key for p in person.summary.split(". ")]

def identify(name):
	person = Person.query(Person.name == name).get()
	if not person:
		person = Person(name=name)
		research(person)
		person.put()
	return person

def tag(sentence):
	return nltk.pos_tag(nltk.word_tokenize(sentence.replace("n't", " not")))

def nextNoun(tagged):
	noun = []
	for t in tagged:
		if t[1].startswith("NN"):
			noun.append(t[0])
		elif noun:
			break
	return " ".join(noun)

def inquire(sentence): # only return if word is unknown
	for (word, pos) in tag(sentence):
		deep = len(word) > 3
		w = learn(word, deep)
		if deep and not w.meanings(True):
			return "%s %s"%(randphrase("inquire"), word)

# also support identity assignment ("I" instead of "Joe Whatever")
def _invert(sentence): # reverse/retag 1st/2nd person
	orig = tag(sentence)
	log("orig: %s"%(orig,))
	tagged = []
	lastword = None
	lastpart = None
	for (word, part) in orig:
		if part == "VB" or part == "VBP":
			part = part == "VBP" and "VB" or "VBP"
			if word == "am":
				word = "are"
			elif word == "are":
				word = "am"
			else:
				word = learn(word).conjugate(part)
		elif word == "i":
			word = "you"
		elif part == "NN" and word == "you":
			word = "i"
		elif part == "PRP":
			if word == "me":
				word = "you"
			elif word == "you":
				word = (lastpart == "IN" and lastword != "that") and "me" or "i"
		lastword = word
		lastpart = part
		tagged.append((word, part))
	log("tagged: %s"%(tagged,))
	return tagged

def invert(sentence):
	return " ".join([a for (a, b) in _invert(sentence)])

def _getalt(word, tpos, opposite=False):
	vmeanz = [m for m in learn(word, len(word) > 3).meanings() if m.part == POS.get(tpos)]
	if vmeanz:
		random.shuffle(vmeanz)
		for mng in vmeanz:
			altz = None
			if opposite and mng.antonyms:
				altz = [a for a in db.get_multi(mng.antonyms) if a.modeltype() == "word" and a.word != word]
			elif not opposite and mng.synonyms:
				altz = [s for s in db.get_multi(mng.synonyms) if s.modeltype() == "word" and s.word != word]
			if altz:
				alt = random.choice(altz)
				log("swapped '%s' for '%s'"%(alt.content(), word))
				return alt.content()

def _rephrase(sentence, tpos, opposite=False):
	# tokenize, replace words w/ synonyms/antonyms
	swapped = False
	new = []
	for (word, pos) in tag(sentence):
		if pos.startswith(tpos):
			new.append(_getalt(word, tpos, opposite) or word)
		else:
			new.append(word)
	return " ".join(new)

def rephrase(sentence):
	return "%s %s"%(randphrase("rephrase"), invert(_rephrase(_rephrase(sentence, "VB"), "NN")))

def support(sentence):
	# tokenize, replace adjective/verb w/ synonym
	return "%s %s"%(randphrase("agree"), invert(_rephrase(_rephrase(sentence, "JJ"), "VB")))

negz = {
	" no ": "",
	" not ": "",
	" isn't ": " is ",
	" aren't ": " are ",
	" weren't ": " were ",
	" don't ": " do ",
	" doesn't ": " does "
}
posz = {
	" is ": " isn't ",
	" are ": " aren't ",
	" were ": " weren't ",
	" do ": " don't ",
	" does ": " doesn't "
}

def negate(sentence):
	for neg in negz:
		if neg in sentence:
			log("negating on %s"%(neg,))
			return sentence.replace(neg, negz[neg])
	for pos in posz:
		if pos in sentence:
			log("negating on %s"%(pos,))
			return sentence.replace(pos, posz[pos])
	negated = False
	words = []
	for (word, pos) in tag(sentence):
		if not negated and pos.startswith("VB"):
			log("negating %s"%(word,))
			word = learn(word).negate(pos)
			log("with %s"%(word,))
			negated = True
		words.append(word)
	return " ".join(words)

def refute(sentence):
	# tokenize, replace adjective w/ antonym, noun w/ synonym
	negation = _rephrase(sentence, "JJ", True)
	if negation == sentence:
		negation = negate(sentence)
	return "%s %s"%(randphrase("disagree"), invert(_rephrase(negation, "NN")))

retorts = {
	"inquire": inquire,
	"rephrase": rephrase,
	"support": support,
	"refute": refute
}