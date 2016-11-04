def drug_use_build_phrase(x):
    return r'(?:\b' + x + r's?\b)'


drug_use_words = [
    r"meth\s*head",
    r"meth-head",
    r"crack\s*head",
    r"crack-head",
    r"meth\s*monster",
    r"meth-monster",
    r"druggie",
    r"junkie",
    r"adict",
    r"dope\s*head",
    r"dope-head",
    r"acid\s*freak",
    r"acid-freak",
    r"acid\s*head",
    r"acid-head",
    r"bag\s*bitch",
    r"bag-bitch",
    r"coke\s*whore",
    r"coke-whore",
    r"dope\s*whore",
    r"dope-whore",
    r"crank\s*whore",
    r"crank-whore",
    r"pill\s*popper",
    r"pill-popper"
]

# If any of the following match, assume it is a negative statement
negative_regex_list = [
    r"don't\s+do\s+drugs?",
    r'do\s+not\s+do\s+drugs?',
    r'\bno\s+drugs\b',
    r'adrenaline'
]

# Common drug user slang
phrase_re_list = []
for x in drug_use_words:
    phrase_re_list.append(drug_use_build_phrase(x))


# Typical sentence fragments to refer to drug users
regex_list = [
    "|".join(phrase_re_list),
    r'\bon\s+.{,15}?drugs?',
    r'\bshe\s+.{,4}?drugs',
    r'\btrak\s+.{,15}?arms',
    r'\buses\s+drugs',
    r'\buses\s+and.{,8}?drugs',
    r'\bsmells?\s+.{,8}?drugs',
    r'\bdoes\s.{,15}?drugs',
    r'\bshe\s+in.{,7}?drugs',
]
