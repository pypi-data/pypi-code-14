"""请写一个能处理去掉=的base64解码函数：

# -*- coding: utf-8 -*-

import base64

def safe_base64_decode(s):

    pass

# 测试:
assert b'abcd' == safe_base64_decode(b'YWJjZA=='), safe_base64_decode('YWJjZA==')
assert b'abcd' == safe_base64_decode(b'YWJjZA'), safe_base64_decode('YWJjZA')
print('Pass')"""
import base64
def safe_base64_decode(s):
    pass
    p=len(s)%4
    for i in range(p):
        s=s+b'='
    print(s)
    return(base64.urlsafe_b64decode(s))
"""
1、assert语句用来声明某个条件是真的。
2、如果你非常确信某个你使用的列表中至少有一个元素，而你想要检验这一点，
并且在它非真的时候引发一个错误，那么assert语句是应用在这种情形下的理想语句。
3、当assert语句失败的时候，会引发一AssertionError。
测试程序：
>>> mylist = ['item']
>>> assert len(mylist) >= 1
>>> mylist.pop()
'item'
>>> assert len(mylist) >= 1
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError
>>>
"""
assert b'abcd' == safe_base64_decode(b'YWJjZA=='), safe_base64_decode('YWJjZA==')
assert b'abcd' == safe_base64_decode(b'YWJjZA'), safe_base64_decode('YWJjZA')
assert b'a' == safe_base64_decode(b'YQ=='), safe_base64_decode('YQ==')
assert b'a' == safe_base64_decode(b'YQ'), safe_base64_decode('YQ')
assert b'ab' == safe_base64_decode(b'YWI='), safe_base64_decode('YWI=')
assert b'ab' == safe_base64_decode(b'YWI'), safe_base64_decode('YWI')
assert b'abc' == safe_base64_decode(b'YWJj'), safe_base64_decode('YWJj')
print('Pass')

        
    
