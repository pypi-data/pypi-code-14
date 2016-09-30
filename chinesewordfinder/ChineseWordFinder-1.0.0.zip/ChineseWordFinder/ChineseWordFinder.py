# -*- coding=utf-8 -*-
# 加上word切词；对‘/’周围的词改变其灵活性
import sys
import os, codecs, re, math
import collections
import time


start_time = time.time()
max_word_len = 5 
entropy_threshold = 1
max_to_flush = 10000
cut_list = frozenset(u".#@ ~-=*&[。，,！……!《》<>\"':：？\?、\|“”‘’；]{}（）{}"
                     u"【】()｛｝（）：？！。，;、~——+％%`:“”＂'‘\n\r")

dicts = ['daici.txt', 'fuci.txt', 'jieci.txt', 'lianci.txt', 'liangci.txt', 'tanci.txt', 'zhuci.txt',
         'zhudongci.txt', 'cizu.txt', 'xingshi.txt', 'shuci.txt']
dicts_txt = []
#将词性词典中的词存入dicts_txt中，dicts_txt为二维list
for dict_i in xrange(0, 9):
    dicts_tmp = []
    d_i = 0
    d_s = ''
    dict_file = codecs.open('dicts/'+dicts[dict_i], 'r', 'utf-8')
    dict_txt = dict_file.read()
    while d_i < len(dict_txt):
        if dict_txt[d_i] != '\r':
            d_s = d_s + dict_txt[d_i]
            d_i = d_i + 1
        else:
            dicts_tmp.append(d_s)
            d_s = ''
            d_i = d_i + 2
    dicts_txt.append(dicts_tmp)

# 将cizu_num存入list cizu_nums中
cizu_nums = []
cizu_num_file = codecs.open('dicts/cizu_num.txt', 'r', 'utf-8')
for cizu_num_line in cizu_num_file:
        cizu_num_tmp = cizu_num_line.split(' ')
        cizu_nums.append(cizu_num_tmp[0])
        cizu_nums.append(int(cizu_num_tmp[1]))

class WordBase(object):
    def __init__(self):
        self.base_freq = 0
        self.base_ps = 0.0
        self.type = ''


class BaseCuttor(object):
    def __init__(self):
        # self.WORD_MAX = 8
        # Use 6 is better, but it will not cut the word longer than 5
        self.WORD_MAX = 6
        self.refer_prob = 15.0
        self.default_prob = 150.0
        self.fn_stage1 = self.__stage1_null

    def exist(self, term):
        pass

    def get_prob(self, term):
        pass

    def word_type(self, term, type):
        return False

    def cut_to_sentence(self, line):
        if not isinstance(line, unicode):
            try:
                line = line.decode('utf-8')
            except UnicodeDecodeError:
                line = line.decode('gbk', 'ignore')
        for s, need_cut in self.fn_stage1(line):
            if need_cut:
                if s != '':
                    str = ''
                    for c in s:
                        if c in cut_list:
                            if str != '':
                                yield (str, True)
                            str = ''
                            yield (c, False)
                        else:
                            str += c
                    if str != '':
                        yield (str, True)
            else:
                yield (s, False)

    def __stage1_null(self, sentence):
        yield (sentence, True)


class Word(WordBase):
    def __init__(self, id):
        super(WordBase, self).__init__()

        self.process_freq = 1
        self.total_freq = 1
        self.valid = 0
        self.process_ps = 0.0
        self.id = id
        self.l_len = 0
        self.r_len = 0
        self.l = collections.Counter()
        self.r = collections.Counter()
        self.base_freq = 0
        self.base_ps = 0.0
        self.curr_ps = 0.0

    def add(self):
        self.process_freq += 1
        self.total_freq += 1

    def add_l(self, word):
        if word in self.l:
            self.l[word] += 1
        else:
            self.l[word] = 1
        self.l_len += 1
    
    def add_r(self, word):
        if word in self.r:
            self.r[word] += 1
        else:
            self.r[word] = 1
        self.r_len += 1

    def reset(self, id):
        self.process_freq = 1
        self.id = id
        self.l_len = 0
        self.r_len = 0
        self.l = collections.Counter()
        self.r = collections.Counter()

# TODO has a better implement?
# How to add fields to Objects dynamically ?


def info_entropy(words, total):
    result = 0 
    for word, cnt in words.iteritems():
        p = float(cnt) / total
        result -= p * math.log(p)
    return result


def word_cut_sentence(txt):
    new_txt = ''
    txt_i = 0
    def compare_a_b(a, b, b_index, length):
        length_tmp = 5
        while length_tmp > length:
            length_k = 1
            while length_tmp - length_k > -1:
                if a == b[b_index - length_tmp + length_k: b_index + length_k]:
                    return True
                length_k += 1
            length_tmp -= 1
        if length_tmp == length:
            return False

    while (txt_i < len(txt)):
        if (txt[txt_i] == ' '):
            txt_i = txt_i + 2
            continue
        flag1 = True
        flag2 = True
        flag3 = True
        for j in xrange(0, 8):
            for k in xrange(0, len(dicts_txt[j])):
                if txt[txt_i: txt_i + 3] == dicts_txt[j][k]:
                    flag1 = False
                    new_txt = new_txt+'/'
                    new_txt = new_txt + txt[txt_i: txt_i+3]
                    new_txt = new_txt + '/'
                    txt_i = txt_i + 3
                    break

                elif txt[txt_i: txt_i + 2] == dicts_txt[j][k]:
                    flag1 = False
                    for c_j in xrange(94628, 94858):
                        if compare_a_b(dicts_txt[8][c_j], txt, txt_i, 2):
                            flag3 = False
                            new_txt = new_txt + txt[txt_i]
                            txt_i = txt_i + 1
                            break
                    if flag3:
                        new_txt = new_txt + '/'
                        new_txt = new_txt + txt[txt_i: txt_i + 2]
                        new_txt = new_txt + '/'
                        txt_i = txt_i + 2
                    break
                elif txt[txt_i] == dicts_txt[j][k]:
                    flag1 = False
                    for c_i in xrange(cizu_nums[cizu_nums.index(txt[txt_i]) + 1],
                                      cizu_nums[cizu_nums.index(txt[txt_i]) + 3]):

                        if compare_a_b(dicts_txt[8][c_i], txt, txt_i, 1):
                            # if dicts_txt[8][c_i] ==file1_txt[i: i+c_k] or dicts_txt[8][c_i] == file1_txt[i-c_k+1: i+1]:
                            new_txt = new_txt + txt[txt_i]
                            flag2 = False
                            txt_i = txt_i + 1
                            break
                        if flag2 is False:
                            break
                    if flag2:
                        new_txt = new_txt + '/'
                        new_txt = new_txt + txt[txt_i]
                        new_txt = new_txt + '/'
                        txt_i = txt_i + 1
                    break
            if flag1 is False:
                break
        if flag1:
            new_txt = new_txt + txt[txt_i]
            txt_i = txt_i + 1
    return new_txt

    # words = []
    # i = 0
    # c = ''
    #
    # cizu = []
    # c_s = ''
    # c_j = 0
    # while (c_j < len(dicts_txt[8])):
    #
    #     if dicts_txt[8][c_j] != '\r':
    #         c_s = c_s + dicts_txt[8][c_j]
    #         c_j = c_j + 1
    #     else:
    #         cizu.append(c_s)
    #         c_s = ''
    #         c_j = c_j + 2
    #
    # while i < len(txt):
    #     flag1 = True
    #     flag2 = True
    #     flag3 = True
    #     for j in xrange(0, 8):
    #         if (dicts_txt[j].find(txt[i]) != -1 and dicts_txt[j][dicts_txt[j].index(txt[i]) + 1] == '\r' and
    #                     dicts_txt[j][dicts_txt[j].index(txt[i]) - 1] == '\n'):
    #             flag1 = False
    #             for k in xrange(4, 1, -1):
    #                 if dicts_txt[j].find(txt[i:i + k]) != -1:
    #                     words.append('/')
    #                     words.append(txt[i:i+k])
    #                     words.append('/')
    #                     i = i + k
    #                     flag2 = False
    #                     break
    #                 elif dicts_txt[j].find(txt[i - k:i + 1]) != -1 and txt[i-1] != '\n':
    #                     words.append('/')
    #                     words.append(txt[i-k:i+1])
    #                     words.append('/')
    #                     i = i + k
    #                     flag2 = False
    #                     break
    #             if flag2:
    #                 for c_i in xrange(0, len(cizu)):
    #                     for c_k in (2, 6):
    #                         if cizu[c_i] == txt[i: i + c_k] or cizu[c_i] == txt[i - c_k + 1: i + 1]:
    #                             words.append(txt[i])
    #                             i = i + 1
    #                             flag3 = False
    #                             break
    #                     if (flag3 == False):
    #                         break
    #                 if (flag3 != False):
    #                     words.append('/')
    #                     words.append(txt[i])
    #                     words.append('/')
    #                     i = i + 1
    #             break
    #     if flag1:
    #         words.append(txt[i])
    #         i = i + 1
    # new_txt = c.join(words)
    # return new_txt
    

class Process(object):
    def __init__(self, id):
        self.id = id
        self.words = []
        self.cache_lines = []
    
    def add_words(self, word):
        self.words.append(word)

    def do_sentence(self, sentence, word_dict):
        s = ''
        cache_sentences = []
        for k in xrange(0, len(sentence)):
            if sentence[k] != '/':
                s = s + sentence[k]
            else:
                s = ''
                if s!= '':
                    cache_sentences = cache_sentences.append(s)
        for m in xrange(0, len(cache_sentences)):
            if len(cache_sentences[m])>1:
                l = len(cache_sentences[m])
                wl = min(l, max_word_len)
                for i in xrange(2, wl + 1):
                    for j in xrange(0, l - i + 1):
                        if j == 0:
                            if j < l - i:
                                if m>0:
                                    word_dict.add_word_lr(cache_sentences[m][j:j + i], cache_sentences[m-1][-1],
                                                      cache_sentences[m][j + i])
                                else:
                                    word_dict.add_word_r(cache_sentences[m][j:j +i], cache_sentences[m][j + i])
                            else:
                                if 0<m<len(cache_sentences)-1:
                                    word_dict.add_word_lr(cache_sentences[m][j:j + i], cache_sentences[m-1][-1],
                                                          cache_sentences [m+1][0])
                                elif m>0:
                                    word_dict.add_word_l(cache_sentences[m][j:j + i], cache_sentences[m-1][-1])
                                elif m<len(cache_sentences)-1:
                                    word_dict.add_word_r(cache_sentences[m][j:j + i], cache_sentences [m+1][0])
                                else:
                                    word_dict.add_word(cache_sentences[m][j + i])
                        else:
                            if j < l - i:
                                word_dict.add_word_lr(cache_sentences[m][j:j + i], cache_sentences[m][j - 1],
                                                      cache_sentences[m][j + i])
                            elif m < len(cache_sentences)-1:
                                word_dict.add_word_lr(cache_sentences[m][j:j + i], cache_sentences[m][j - 1],
                                                          cache_sentences[m+1][0])
                            else:
                                word_dict.add_word_l(cache_sentences[m][j:j + i], cache_sentences[m][j - 1])

    def calc(self, word_dict):
        # calc all ps first
        for word in self.words:
            this_word = word_dict.get_word(word)
            this_word.process_ps = float(this_word.process_freq)/word_dict.process_total
    
        # then calc the ps around the word
        for word in self.words:
            this_word = word_dict.get_word(word)
            if len(word) > 1:
                p = 0
                for i in xrange(1, len(word)):
                    t = word_dict.ps(word[0:i]) * word_dict.ps(word[i:])
                    p = max(p, t)
                if p > 0 and this_word.process_freq >= 3 and this_word.process_ps / p > 100:
                    if this_word.l_len > 0 and info_entropy(this_word.l, this_word.l_len) < entropy_threshold:
                        continue
                    if this_word.r_len > 0 and info_entropy(this_word.r, this_word.r_len) < entropy_threshold:
                        continue
                    this_word.valid += 1
                    print word
                    print this_word.valid
                    this_word.curr_ps = math.log(float(this_word.total_freq + this_word.base_freq) / float(
                        word_dict.base_total + word_dict.total / word_dict.id))


class WordDict(BaseCuttor):

    def __init__(self, new_dict=True):
        super(WordDict, self).__init__()

        self.dict = {}
        self.total = 0
        self.base_total = 0
        self.id = 0
        self.process_total = 0
        self.current_line = 0
        
        self.WORD_MAX = 5
        
        '''with codecs.open(dict_file, "r", "utf-8") as file:
            for line in file:
                tokens = line.split(" ")
                word = tokens[0].strip()
                if len(tokens) >= 2:
                    this_word = Word(0)
                    freq = int(tokens[1].strip())
                    this_word.base_freq = freq
                    self.dict[word] = this_word
                    self.base_total += freq
        
        #normalize
        for word, term in self.dict.iteritems():
            term.base_ps = math.log(float(term.base_freq)/self.base_total)
            term.curr_ps = term.base_ps'''

        if not new_dict:
            # TODO for getting dict from MAIN_DICT
            self.dict = get_modified_dict()

        self.new_process()

    def add_user_dict(self, filename):
        with codecs.open(filename, "r", "utf-8") as file:
            for line in file:
                tokens = line.split(" ")
                word = tokens[0].strip()
                if len(tokens) >= 2:
                    freq = int(tokens[1].strip())
                    if word in self.dict:
                        this_word = self.dict[word]
                        this_word.base_freq += freq
                        self.base_total += freq
                    else:
                        this_word = Word(0)
                        this_word.base_freq = freq
                        self.dict[word] = this_word
                        self.base_total += freq
        # normalize
        for word, term in self.dict.iteritems():
            term.base_ps = math.log(float(term.base_freq)/self.base_total)
            term.curr_ps = term.base_ps
    
    def exist(self, word):
        if word not in self.dict:
            return False
        this_word = self.dict[word]
        return (this_word.curr_ps < 0.0) or (this_word.valid > self.id/2)

    def get_prob(self, word):
        if word in self.dict:
            return self.dict[word].curr_ps
        else:
            return 0.0
    
    def new_process(self):
        self.id += 1
        self.process = Process(self.id)
        self.process_total = 0
        return self.process
    
    def add_word(self, word):
        if word in self.dict:
            this_word = self.dict[word]
            if self.id == this_word.id:
                this_word.add()
            else:
                this_word.reset(self.id)
                self.process.add_words(word)
        else:
            this_word = Word(self.id)
            self.dict[word] = this_word
            self.process.add_words(word)
        self.process_total += 1
        self.total += 1
        return this_word

    def nick_finder(self, txt):
        fuhao_list = frozenset(u".#/~-=*&@[。，,！……!《》<>\"'：？\?、\|“”‘’；]{}（）{}【】()｛｝（）：？！。，;、~+％%`“”＂'‘")
        for i in xrange(0, len(txt)):
            j = 1
            if (txt[i] == '@'):
                try:
                    while (txt[i + j] != ' '.decode('utf-8') and txt[i + j] != ':'.decode('utf-8') and txt[
                            i + j] not in fuhao_list):
                        j = j + 1

                    if ((txt[i + j] == ' '.decode('utf-8') or txt[i + j] == ':'.decode('utf-8')) and j < 31):
                        nick = txt[i + 1:i + j]
                        if nick in self.dict:
                            this_word = self.dict[nick]
                            this_word.total_freq += 1
                        else:
                            this_word =Word(self.id)
                            self.dict[nick] = this_word
                            this_word.valid =1
                except IndexError:
                    if (j < 31):
                        nick = txt[i + 1:i + j]
                        if nick in self.dict:
                            this_word = self.dict[nick]
                            this_word.total_freq += 1
                        else:
                            this_word =Word(self.id)
                            self.dict[nick] = this_word
                            this_word.valid =1

    def theme_finder(self, txt):
        i = 0
        themes = []
        new_themes = []
        while (i < len(txt)):
            i = i + 1
            if (txt[i - 1] == '(' and txt[i] == "\'"):
                i = i + 1
                try:
                    while (txt[i - 1] != ')' or txt[i] != ','):
                        if (txt[i] == '#'):
                            k = 1
                            try:
                                while (txt[i + k] != '#' and k < 139 and (txt[i + k - 1] != ')' or txt[i + k] != ',')):
                                    k = k + 1
                                if (txt[i + k] == '#' and k < 139):
                                    theme = txt[i + 1:i + k]
                                    if theme != '':
                                        if theme in self.dict:
                                            this_theme = self.dict[theme]
                                            this_theme.total_freq += 1
                                        else:
                                            this_theme = Word(self.id)
                                            self.dict[theme] = this_theme
                                            this_theme.valid = 1
                                    i = i + k
                            except IndexError:
                                pass
                        i = i + 1
                except IndexError:
                    pass

    def learn(self, sentence):
        self.nick_finder(sentence)
        self.theme_finder(sentence)
        new_sentence = word_cut_sentence(sentence)
        for s, need_cut in self.cut_to_sentence(new_sentence):
            if not need_cut:
                continue
            self.process.do_sentence(s, self)
            self.current_line += 1
            if self.current_line > max_to_flush:
                print time.time() - time.time()
                self.process.calc(self)
                self.new_process()
                self.current_line = 0

    def learn_flush(self):
        self.process.calc(self)
        self.new_process()
        self.current_line = 0

    def add_word_l(self, word, l):
        w = self.add_word(word)
        w.add_l(l)
    
    def add_word_r(self, word, r):
        w = self.add_word(word)
        w.add_r(r)
    
    def add_word_lr(self, word, l, r):
        w = self.add_word(word)
        w.add_l(l)
        w.add_r(r)

    def ps(self, word):
        if word in self.dict and self.dict[word].id == self.id:
            return self.dict[word].process_ps
        else:
            return 0.0

    def get_word(self, word):
        return self.dict[word]

    def save_to_file(self, filename, sorted=False):
        word_dict = self
        if sorted:
            final_words = []
            for word, term in word_dict.dict.iteritems():
                # if term.valid > word_dict.id/2 and term.base_freq == 0:
                # Use this to save more word
                if term.valid > 0 and term.base_freq == 0:
                    final_words.append(word)

            final_words.sort(cmp = lambda x, y: cmp(word_dict.get_word(y).total_freq, word_dict.get_word(x).total_freq))
            
            with codecs.open(filename, 'w', 'utf-8') as file:
                for word in final_words:
                    v = word_dict.get_word(word).total_freq

                    file.write("%s %d\n" % (word, v))
        else:
            with codecs.open(filename, 'w', 'utf-8') as file:
                for word, term in word_dict.dict.iteritems():
                    if term.valid > 0 and term.base_freq == 0:
                        file.write("%s %d\n" % (word, term.total_freq))

def finder (segfile, resultfile, sorted=True):
    flag = sorted
    word_dict = WordDict()
    learn_file = codecs.open(segfile, 'r', 'utf-8')
    learn_txt = learn_file.read()
    word_dict.learn(learn_txt)
    word_dict.learn_flush()
    word_dict.save_to_file(resultfile, flag)
    end_time = time.time()
    last_time = end_time - start_time
    print '运行时间'+ str(last_time)
