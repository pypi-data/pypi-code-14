from pocketsphinx import LiveSpeech

def listen(cb):
	for phrase in LiveSpeech():
		p = str(phrase)
		print p
		p and cb(p)
