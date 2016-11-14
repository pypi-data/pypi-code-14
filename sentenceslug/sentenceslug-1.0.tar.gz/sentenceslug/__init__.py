from .sentenceslug import SentenceSlug

def simple_slug():
    ss = SentenceSlug()
    return ss.makeslug(simple=True)

def simple_slug_digits():
    ss = SentenceSlug()
    return ss.makeslug(simple=True, digits=3)

def sentence_slug():
    ss = SentenceSlug()
    return ss.makeslug(delimiter="_")

def sentence_slug_digits():
    ss = SentenceSlug()
    return ss.makeslug(delimiter="_", digits=3)

def nsa_codeword():
    ss = SentenceSlug()
    return ss.makeslug(simple=True).upper()

def make_slug(**kwargs):
    ss= SentenceSlug()
    return ss.makeslug(**kwargs)