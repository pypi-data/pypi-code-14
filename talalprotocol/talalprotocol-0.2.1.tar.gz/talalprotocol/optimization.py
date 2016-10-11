'''
This file is for new or optimized versions of the ciphers

Binary cipher mods:
handle punctuation and digit inputs
fix output

Note: Binary cipher might be faster if we implement a binary search
'''

from talalprotocol import *
import string
import re
import os


english_alphabets = list(string.ascii_lowercase)
string_punctuation = string.punctuation
string_digits = string.digits



def encrypt_file(filename):

    original_file = filename












binary_test = BinaryCipher()
x = binary_test.BinaryEncryption('I am so gay')
print(x)
#
# y = binary_test.BinaryDecryption(x)
# print(y)



# my_test = CaesarCipher(3)
#
# x = my_test.encryption('I am Talal')
# print(x)
#
# y = my_test.decryption(x)
# print(y)


# passing_val = '0000000 0100000 1000000 0000000 0100000 1000000'
# x = binary_decryption(passing_val)
# print(x)


# print(string_punctuation)
# message = 'a 1 !'
# ciphered_version = binary_encryption(message)
#
# print(ciphered_version)


# x = caesar_cipher('Hi I am gay',1)
# y = caesar_decipher ('ij j bn',1)
#
# x = vigenere_cipher('My name is talal','math')
# print(x)
#
# y = vigenere_decipher(x, 'math')
# print(y)




