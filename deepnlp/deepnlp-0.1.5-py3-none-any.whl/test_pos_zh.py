#coding:utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals # compatible with python3 unicode coding

import pos_tagger
tagger = pos_tagger.load_model(lang = 'zh')

#Segmentation
text = "我 爱 吃 北京 烤鸭"
words = text.split(" ") # words in unicode coding
print (" ".join(words).encode('utf-8'))

#POS Tagging
tagging = tagger.predict(words)
for (w,t) in tagging:
    str = w + "/" + t
    print (str.encode('utf-8'))

#Results
#我/r
#爱/v
#吃/v
#北京/ns
#烤鸭/n
