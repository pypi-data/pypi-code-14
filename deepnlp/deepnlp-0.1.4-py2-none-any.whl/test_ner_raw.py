#coding:utf-8

#Set Default codec coding to utf-8 to print chinese correctly
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()

import ner_tagger
tagger = ner_tagger.load_model(lang = 'zh')

#Segmentation
text = "我 爱 吃 北京 烤鸭"
words = text.split(" ")
print (" ".join(words).encode('utf-8'))

#NER Tagging
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
