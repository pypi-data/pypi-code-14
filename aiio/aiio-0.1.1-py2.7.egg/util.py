import random

phrases = {
	"rephrase": [
		"so you're saying that",
		"in other words,",
		"so,"
	],
	"inquire": [
		"please elaborate on",
		"tell me more regarding",
		"i'd like to know more about"
	],
	"noted": [
		"noted",
		"thanks for the info",
		"cool",
		"ok, great"
	],
	"what": [
		"what?",
		"i'm not sure what you mean",
		"i don't get it"
	],
	"unsure": [
		"i'm not sure",
		"it's hard to say",
		"ummm.."
	],
	"exhausted": [
		"i don't know anymore :(",
		"you tell me"
	],
	"agree": [
		"exactly!",
		"i completely agree.",
		"you're preaching to the choir :)",
		"you've got my vote!"
	],
	"disagree": [
		"i don't think you're right.",
		"you're wrong!",
		"not exactly..."
	]
}

def randphrase(ptype):
	return random.choice(phrases[ptype])