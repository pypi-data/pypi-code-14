# -*- coding: UTF-8 -*-
#!/usr/bin/python
import re
import os
import json

try:
    import hfst_lookup
    CHFST = True
except:
    from .shared import Header, Alphabet
    from .transducer import Transducer
    from .transducer import TransducerW
    CHFST = False

import pymorphy2
from pymorphy2.units.by_analogy import KnownSuffixAnalyzer, UnknownPrefixAnalyzer, DictionaryAnalyzer

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_MORPHAN_FILE = os.path.join(BASE_DIR, 'files/tatar_last.hfstol')
WORDS_FILE = os.path.join(BASE_DIR, 'files/words.csv')
EXCEPTIONS_FILE = os.path.join(BASE_DIR, 'files/exceptions.txt')
DISAM_RULES_FILES = os.path.join(BASE_DIR, 'files/disam_rules.json')

def is_that_chain(chain, pattern):
    """
        Checks if chain fits the pattern
        :chain string
        :pattern string
    """
    chain_set = set(chain.split('+')) | set([''])
    pattern_set = set(pattern.split('+'))
    if not len(pattern_set - chain_set):
        return True

def is_that_amtype(chains, amtype_pattern):
    """
        Checks if amtype fits the amtype_pattern
        :chains string (delimeter ';')
        :amtype_pattern string (delimeter '|')
    """
    chains = chains.strip(';').split(';')
    patterns = amtype_pattern.split('|')
    found = False
    for chain in chains:
        for pattern in patterns:
            if is_that_chain(chain, pattern):
                found = True
                patterns.remove(pattern)
                break
        if found:
            # change to False and check next chain
            found = False
        else:
            return False
    return True

def is_amtype_pattern(amtype_pattern, errors=[]):
    """
        Checks if amtype is formed in proper way
    """
    err = []
    morphemes = [u"POSS_1SG(Ым)", u"NUM_COLL(АУ)", u"PROF(чЫ)", u"LOC(ДА)", u"1SG(мЫн)", 
                 u"ATTR_LOC(ДАгЫ)", u"PREC_2(сАнА)", u"ATTR_GEN(нЫкЫ)", u"PST_DEF(ДЫ)", 
                 u"PART", u"ATTR_MUN(лЫ)", u"IMP_PL(ЫгЫз)", u"RAR_2(ЫштЫр)", u"3PL(ЛАр)", 
                 u"SIM_2(сыман)", u"POST", u"1PL(к)", u"HOR_SG(Йм)", u"FUT_DEF(АчАк)", 
                 u"EQU(чА)", u"OBL(ЙсЫ)", u"PROB(ДЫр)", u"PCP_FUT(Ыр)", u"RAR_1(ГАлА)", 
                 u"NUM_APPR(лАп)", u"INF_1(ЫргА)", u"ATTR_ABES(сЫз)", u"N", u"INTRJ", 
                 u"POSS_2SG(Ың)", u"VN_1(у/ү/в)", u"POSS_2PL(ЫгЫз)", u"PST_INDF(ГАн)", 
                 u"IMP_SG()", u"ABL(ДАн)", u"1PL(бЫз)", u"Num", u"PCP_PR(чЫ)", u"MOD", 
                 u"NMLZ(лЫк)", u"ADVV_NEG(ЙчА)", u"ADVV_ACC(Ып)", u"DIR_LIM(ГАчА)", u"Adj", 
                 u"PASS(Ыл)", u"DIM(чЫк)", u"ADVV_SUCC(ГАнчЫ)", u"JUS_PL(сЫннАр)", u"DIR(ГА)", 
                 u"HOR_PL(Йк)", u"RECP(Ыш)", u"PCP_PS(ГАн)", u"ACC(нЫ)", u"CNJ", 
                 u"FUT_INDF_NEG(мАс)", u"MSRE(лАтА)", u"NEG(мА)", u"REFL(Ын)", u"2SG(сЫң)", 
                 u"NUM_DISR(шАр)", u"COMP(рАк)", u"2PL(гЫз)", u"USIT(чАн)", u"SIM_1(ДАй)", 
                 u"GEN(нЫң)", u"DESID(мАкчЫ)", u"CAUS(ДЫр)", u"PRES(Й)", u"1SG(м)", u"AFC(кАй)", 
                 u"3SG(ДЫр)", u"Sg", u"V", u"2PL(сЫз)", u"PCP_FUT(АчАк)", u"Nom", u"INT(мЫ)", 
                 u"VN_2(Ыш)", u"ADVV_ANT(ГАч)", u"SIM_3(сымак)", u"POSS_1PL(ЫбЫз)", 
                 u"INT_MIR(мЫни)", u"PL(ЛАр)", u"POSS_3(СЫ)", u"IMIT", u"PREM(мАгАй)", 
                 u"INF_2(мАк)", u"PN", u"DISTR(лАп)", u"Adv", u"2SG(ң)", u"CAUS(т)", 
                 u"PREC_1(чЫ)", u"INF_1(скА)", u"NUM_ORD(ЫнчЫ)", u"PSBL(лЫк)", u"JUS_SG(сЫн)", 
                 u"PCP_FUT(мАс)", u"PROP", u"COND(сА)",
                 u"POSS_1SG", u"NUM_COLL", u"PROF", u"LOC", u"1SG", u"ATTR_LOC", u"PREC_2", 
                 u"ATTR_GEN", u"PST_DEF", u"PART", u"ATTR_MUN", u"IMP_PL", u"RAR_2", u"3PL", 
                 u"SIM_2", u"POST", u"1PL", u"HOR_SG", u"FUT_DEF", u"EQU", u"OBL", u"PROB", 
                 u"PCP_FUT", u"RAR_1", u"NUM_APPR", u"INF_1", u"ATTR_ABES", u"N", u"INTRJ", 
                 u"POSS_2SG", u"VN_1", u"POSS_2PL", u"PST_INDF", u"IMP_SG", u"ABL", u"1PL", 
                 u"Num", u"PCP_PR", u"MOD", u"NMLZ", u"ADVV_NEG", u"ADVV_ACC", u"DIR_LIM", 
                 u"Adj", u"PASS", u"DIM", u"ADVV_SUCC", u"JUS_PL", u"DIR", u"HOR_PL", u"RECP", 
                 u"PCP_PS", u"ACC", u"CNJ", u"FUT_INDF_NEG", u"MSRE", u"NEG", u"REFL", u"2SG", 
                 u"NUM_DISR", u"COMP", u"2PL", u"USIT", u"SIM_1", u"GEN", u"DESID", u"CAUS", 
                 u"PRES", u"1SG", u"AFC", u"3SG", u"Sg", u"V", u"2PL", u"PCP_FUT", u"Nom", u"INT", 
                 u"VN_2", u"ADVV_ANT", u"SIM_3", u"POSS_1PL", u"INT_MIR", u"PL", u"POSS_3", u"IMIT", 
                 u"PREM", u"INF_2", u"PN", u"DISTR", u"Adv", u"2SG", u"CAUS", u"PREC_1", u"INF_1", 
                 u"NUM_ORD", u"PSBL", u"JUS_SG", u"PCP_FUT", u"PROP", u"COND", u""]
    if len(amtype_pattern.split('|')) < 2:
        err.append((1, 'There must be ambiguity. To separate use "|" sign.'))
    for chain in amtype_pattern.split('|'):
        for morpheme in chain.split('+'):
            if morpheme not in morphemes:
                err.append((2, 'There is no such morpheme: "%s"' % morpheme))
    if len(err) > 0:
        errors += err[:]
        return False
    return True

def get_chain_by_pattern(chains, pattern):
    """
        From chains set choose that fits the pattern
        :chains
    """
    chains = chains.strip(';').split(';')
    for chain in chains:
        if is_that_chain(chain, pattern):
            return chain

def apply_simple_rule(sentence, index, rule_type, searched):
    """
        Checks if this word (sentence[index]) fits the rule
    """    
    if index < 0 or index > len(sentence)-1:
        # checks for sentence's borders
        return rule_type == 4
    elif rule_type == 1:
        # checks for exact word
        if sentence[index][0] == searched:
            return True
    elif rule_type == 2:
        # checks for exact chain
        chains = sentence[index][1].strip(';').split(';')
        for chain in chains:
            if chain[-len(searched):] == searched.strip(';'):
                return True
    elif rule_type == 3:
        # checks for exact morpheme
        # print('\tWord=%s, searched=%s' % (sentence[index][1], searched))
        chains = sentence[index][1].strip(';').split(';')
        for chain in chains:
            if searched in chain.split('+'):
                return True
    elif rule_type == 5:
        # checks if first letter is upper case
        if sentence[index][0][0].isupper():
            return True
    return False

def disambiguate_word(sentence, index, rules):
    """
        word disambiguation
        :sentence list of words
        :index number of word needed to disambiguate
        :rules list of rules needed to check with
    """
    if not rules:
        return None
    for (pattern, context_rules, exceptions) in rules:
        if is_that_amtype(sentence[index][1], pattern):
            # print('%s - %s' % (sentence[index][1], pattern))
            # if it is an exception, disambiguate using exceptions
            result = disambiguate_word(sentence, index, exceptions)
            if result:
                return result
            # it is not exception, so apply rules
            for (rule, result_pattern) in context_rules:
                expression = True
                for (rule_type, searched, first_index, last_index, operand) in rule:
                    result = False
                    for i in range(first_index, last_index+1):
                        result = apply_simple_rule(sentence, index+i, rule_type, searched)
                        # print('simple rule(%s): rule_type=%s, searched=%s, index=%s' % (result, rule_type, searched, index+i))
                        if result:
                            break
                    if operand == 'and':
                        expression = expression and result
                    elif operand == 'or':
                        expression = expression or result
                    elif operand == 'and not':
                        expression = expression and not result
                    elif operand == 'or not':
                        expression = expression or not result
                    else:
                        expression = False
                # if all rules fits
                if expression:
                    return get_chain_by_pattern(sentence[index][1], result_pattern)


class Morphan:
    def __init__(self, 
                 transducerfile=None, 
                 wordsfile=None, 
                 exceptionsfile=None, 
                 disamrulesfile=None,
                 params={}):
        '''
            Read a transducer from filename
        '''
        self.params = {'sdelimiter': u'\n',
                       'fdelimiter': u'\n'
                      }
        if not transducerfile:
            transducerfile = DEFAULT_MORPHAN_FILE
        if not wordsfile:
            wordsfile = WORDS_FILE
        if not exceptionsfile:
            exceptionsfile = EXCEPTIONS_FILE
        if not disamrulesfile:
            disamrulesfile = DISAM_RULES_FILES
        self.params.update(params)
            
        # if C hfst_lookup package installed
        if CHFST:
            self.ctransducer = hfst_lookup.Transducer(transducerfile)
            self.transducer = None
        else:
            # else loads the simple transducer
            self.ctransducer = None
            handle = open(transducerfile, "rb")
            self.header = Header(handle)
            self.alphabet = Alphabet(handle, self.header.number_of_symbols)
            if self.header.weighted:
                self.transducer = TransducerW(handle, self.header, self.alphabet)
            else:
                self.transducer = Transducer(handle, self.header, self.alphabet)
            handle.close()

        # loads words and exceptions for better performance
        self.words = {}
        if not self.ctransducer:
            with open(wordsfile, 'rb') as stream:
                lines = stream.read().decode('UTF-8').split('\n')
            for line in lines:
                splits = line.split('\t')
                if len(splits) == 2:
                    self.words[splits[0]] = splits[1]
        with open(exceptionsfile, 'rb') as stream:
            lines = stream.read().decode('UTF-8').split('\n')
        for line in lines:
            splits = line.split('\t')
            if len(splits) == 2:
                self.words[splits[0]] = splits[1]

        self.rusmorphan = pymorphy2.MorphAnalyzer()
        self.disam_rules = None
        with open(disamrulesfile, 'r') as stream:
            self.disam_rules = json.loads(stream.read())

    def load_disam_rules(filename):
        """
            Loads rules from json file
        """
        if os.path.isfile(filename):
            with open(filename, 'r') as stream:
                disam_rules = json.loads(stream.read())
                return disam_rules

    def analyse(self, string):
        '''
            Take string to analyse, return a vector of (string, weight) pairs.
        '''
        if not isinstance(string, unicode):
            string = string.decode('UTF-8')
        if string.lower() in self.words:
            return self.words[string.lower()]

        if self.ctransducer:
            result = self.ctransducer.lookup(string.encode('UTF-8'))
            if not result:
                return None
            # delete '+' sign in the end of analysis
            result = [row[0].decode('UTF-8') if row[0][-1] != '+' else row[0][:-1] for row in result]
            # delete duplicates and sort, then join with ';' delimiter
            return ';'.join(sorted(list(set(result)))) + ';'
        else:
            if self.transducer.analyze(string):
                result = self.transducer.displayVector
                if not result:
                    return None
                # delete '+' sign in the end of analysis
                result = [row[0] if row[0][-1] != u'+' else row[0][:-1] for row in result]
                # delete duplicates and sort, then join with ';' delimiter
                return ';'.join(sorted(list(set(result)))) + ';'
        return None

    def lemma(self, string):
        """
            Returns the lemma of the word
        """
        analysed = self.analyse(string).strip(';')
        if analysed:
            return sorted(list(set([res.split(u'+')[0] for res in analysed.split(';')])))

    def pos(self, string):
        """
            Returns the part-of-speech of the word
            !TODO
        """
        analysed = self.analyse(string).strip(';')
        if analysed:
            return sorted(list(set([res.split(u'+')[1] for res in analysed.split(';')])))

    def process_text(self, text):
        """
            Parses text and analyses each lexical unit
        """
        sdelim = self.params.get('sdelimiter', u'\n')
        fdelim = self.params.get('fdelimiter', u'\n')
        sentences = self.analyse_text(text)
        result = u''
        for sentence in sentences:
            for (word, chains) in sentence:
                result += '%s%s%s%s' % (word, sdelim, chains, fdelim)
        return result

    def is_russian_word(self, word):
        """
            Parses word and check if word is russian
        """
        parses = self.rusmorphan.parse(word)
        for parse in parses:
            if 'UNKN' not in parse.tag and \
                not isinstance(parse.methods_stack[0][0], KnownSuffixAnalyzer.FakeDictionary) and\
                not isinstance(parse.methods_stack[1][0] if len(parse.methods_stack) > 1 else None,\
                                UnknownPrefixAnalyzer) and\
                isinstance(parse.methods_stack[0][0], DictionaryAnalyzer):
                return True
        return False

    def analyse_text(self, text):
        """
            Process text and return as list of words
        """
        if not isinstance(text, unicode):
            text = text.decode('utf8')

        letters = {u'ђ':u'ә', u'њ':u'ү', u'ќ':u'җ', u'љ':u'ө', u'ћ':u'ң',
                   u'џ':u'һ', u'Ә':u'ә', u'Ү':u'ү', u'Ө':u'ө', u'Җ':u'җ',
                   u'Һ':u'һ', u'Ң':u'ң', u'c':u'с', u'a':u'а'}
        # some texts contains words with not right letters, need to replace to right
        for letter in letters:
            text = text.replace(letter, letters[letter])

        # replace some errors
        text = text.replace(u'-\r\n', u'').replace(u'-\n\r', u'')\
                   .replace(u'-\n', u'').replace(u'-\r', u'')\
                   .replace(u'¬', u'').replace(u'...', u'…')\
                   .replace(u'!..', u'!').replace(u'?..', u'?')\
                   .replace(u' -', u' - ').replace(u'- ', u' - ')

        words = re.split(u"([ .,!?\n\r\t“”„‘«»≪≫\{\}\(\)\[\]:;\'\"+=*\—_^… ]|[0-9]+)", text)

        sentences = []
        sentence = []
        for word in words:
            if word.lower() in self.words:
                sentence.append((word, self.words[word.lower()]))
            elif word in [u'.', u'!', u'?', u'…']:
                sentence.append((word, 'Type1'))
                sentences.append(sentence)
                sentence = []
            elif word in [u',', u':', u';', u'—', u'–', u'_']:
                sentence.append((word, u'Type2'))
            elif word in [u'(', u')', u'[', u']', u'{', u'}']:
                sentence.append((word, u'Type3'))
            elif word in [u'“', u'”', u'"', u"'", u'»', u'«', u'≪', u'≫', u'„', u'‘']:
                sentence.append((word, u'Type4'))
            elif word in [u' ', u' ', u'', u'\n', u'\n\r', u'\r', u'\t']:
                pass
            elif re.match('^[а-эА-ЭөүһңҗҺҮӨҖҢЁё]$', word):
                sentence.append((word, u'Letter'))
            elif word.isdigit():
                sentence.append((word, u'Num'))
            elif re.match('^[a-zA-Z]+$', word):
                sentence.append((word, u'Latin'))
            elif re.match('^[^а-яА-ЯөүһңҗәҺҮӨҖҢӘЁё]$', word):
                sentence.append((word, u'Sign'))
            elif (re.match(u'[а-яА-ЯөӨүҮһҺңҢҗҖәӘЁё]+$', word)) \
                 or (re.match(u'[а-яА-ЯөӨүҮһҺңҢҗҖәӘЁё]+\-[а-яА-ЯөӨүҮһҺңҢҗҖЁёәӘ]+$', word)):
                if word.count("-") > 1:
                    sentence.append((word, u'Error'))
                else:
                    res = self.analyse(word)
                    modified_word = None
                    if not res:
                        word = word.lower()
                        res = self.analyse(word)
                    if not res and self.is_russian_word(word):
                        res = u'Rus'
                    if not res:
                        modified_word = word.replace(u'һ', u'х')
                        res = self.analyse(modified_word)
                    if not res:
                        modified_word = word.replace(u'-', u'')
                        res = self.analyse(modified_word)

                    if not res:
                        sentence.append((word, u'NR'))
                    elif modified_word:
                        sentence.append((modified_word, res))
                    else:
                        sentence.append((word, res))
            else:
                sentence.append((word, u'Error'))
        if len(sentence) > 0:
            sentences.append(sentence)
        return sentences

    def disambiguate_text(self, text, disam_rules=None):
        """
            Parses text, analyses it and disambiguate morphological ambiguities
        """
        if not disam_rules:
            disam_rules = self.disam_rules
        sentences = self.analyse_text(text)
        for sentence in sentences:
            for word in sentence:
                if len(word[1].split(';')) >= 3:
                    # ambiguos word
                    result = disambiguate_word(sentence, sentence.index(word), disam_rules)
                    if result:
                        sentence[sentence.index(word)] = (word[0], result)
        return sentences
