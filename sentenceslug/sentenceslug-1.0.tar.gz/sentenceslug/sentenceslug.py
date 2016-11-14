import random

from wordlists import WordLists as WL

class SentenceSlug:

    @classmethod
    def makeslug(cls, digits=0, simple=False, delimiter=""):

        adjective = WL.randomAdjective().title()
        noun = WL.randomNoun().title()

        if not simple:
            verb = WL.randomVerb().title()
            determiner = WL.randomDeterminer().title()
            if determiner == 'A' and adjective[0] in ['A', 'E', 'I', 'O', 'U', 'H']:
                determiner = 'An'
            slug_list = [verb, determiner, adjective, noun]
        else:
            slug_list = [adjective, noun]
        if digits:
            slug_list.append(str(random.randint(1, 10 ** digits - 1)).zfill(digits))
        return delimiter.join(slug_list)

if __name__ ==  '__main__':

    combos = len(WL.verbs) * len(WL.determiners) * len(WL.adjectives) * len(WL.nouns)
    print "Examples of sentence slugs without integer postfix: (%s combos)" % combos
    for i in range(10):
        ss = SentenceSlug()
        print ss.makeslug()

    print ""

    combos = combos * 999
    print "Examples of sentence slugs with integer postfix: (%s combos)" % combos
    for i in range(10):
        ss = SentenceSlug()
        print ss.makeslug(digits=3)

    print ""

    combos = len(WL.adjectives) * len(WL.nouns)
    print "Examples of simple slugs without integer postfix: (%s combos)" % combos
    for i in range(10):
        ss = SentenceSlug()
        print ss.makeslug(simple=True)

    print ""

    combos = combos * 999
    print "Examples of simple slugs with integer postfix: (%s combos)" % combos
    for i in range(10):
        ss = SentenceSlug()
        print ss.makeslug(simple=True, digits=3)