#!/usr/bin/env python
import optparse
import urllib.request
from bs4 import BeautifulSoup
import re

def main():
    p = optparse.OptionParser()
    p.add_option('--url', '-u', default="http://www.rcsb.org/pdb/home/home.do")
    options, arguments = p.parse_args()
    fp = urllib.request.urlopen(options.url)
    mybytes = fp.read()
    # note that Python3 does not read the html code as string
    # but as html code bytearray, convert to string with
    html_doc = mybytes.decode("utf8")
    fp.close()
    soup = BeautifulSoup(html_doc,"lxml")
    html_text = soup.get_text()
    #linkre = re.compile("href=['\"]([^\"'>]*?)['\"].*?")
    word_re = re.compile("[a-zA-Z]*")
    word_arr = []
    for x in word_re.findall(html_text):##返回所有有匹配的列表
        if x:
            pre_word = camel_to_underline(x)
            pre_words = pre_word.split('_')
            for word in pre_words:
               if word not in word_arr and len(word) > 1:
                   word_arr.append(word)
    for x in word_arr:
        print(x)


def camel_to_underline(camel_format):  
    ''''' 
        驼峰命名格式转下划线命名格式 
    '''  
    underline_format=''  
    if isinstance(camel_format, str):  
        for _s_ in camel_format:  
            underline_format += _s_ if _s_.islower() else '_'+_s_.lower()  
    return underline_format  

def underline_to_camel(underline_format):  
    ''''' 
        下划线命名格式驼峰命名格式 
    '''  
    camel_format = ''  
    if isinstance(underline_format, str):  
        for _s_ in underline_format.split('_'):  
            camel_format += _s_.capitalize()  
    return camel_format  

if __name__ == "__main__":
    sys.exit(main())
