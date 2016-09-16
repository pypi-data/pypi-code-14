# -----------------------------------------------------------------------------
# Name: talalprotocol 
# Purpose: provide various encryption functions
#
# Author: Talal Khalil
# Start Date: 8/01/2016
# Latest mod: 9/15/2016
# Notes: 
# a. major rewrite (more efficient) to vigenere 
# b. Add RSA 
# -----------------------------------------------------------------------------

'''
This module provides the following encryption functions:

1. Vigenere Cipher 
    function calls: vigenere_cipher() or vigenere_decipher() 

2. Caesar Cipher  
    function calls: caesar_cipher() and caesar_decipher()

'''

import string
import re

english_alphabets = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
                         'n','o','p','q','r','s','t','u','v','w','x','y','z']

def caesar_cipher():
    '''
    This function ciphers any submitted message using Caesar Cipher

    Encryption mathematical representation:
    caesar_cipher(x) = (x + n) mod 26 
    x: letter index     n: shift value 


    Parameters:
    N/A (the user will be prompted)
    Returns:
    ciphered text
    '''
    original_text = input('Enter the text you desire to encrypt: ')
    original_text = original_text.lower()
    shift_value = int(input('Choose the shifting value (a number from 1 - 26): '))
    ciphered_text = []
    for character in original_text:
        if character.isdigit():
            ciphered_text.append(character)

        elif character in english_alphabets:
            ciphered_text.append(english_alphabets[
                (english_alphabets.index(character) + shift_value) % 26])

    print(''.join(ciphered_text))

def caesar_decipher():
    '''
    This function deciphers any Caesar-encrpyted message 
    '''
    ciphered_text = input('What is the message you desire to decrypt: ')
    ciphered_text = ciphered_text.lower()
    key_word = input('Enter the encryption key: ')
    key_word = key_word.lower()



def vigenere_cipher():
    '''
    This function ciphers any submitted message using Vigenere Cipher

    Encryption mathematical representation:
    vigenere_cipher(y) = (y + k) mod 26
    y: letter index   k: corresponding key letter index  

    Parameters:
    N/A (the user will be prompted)
    Returns:
    ciphered text
    '''
    original_text = input('Enter the text you desire to encrypt:')
    original_text = original_text.lower()
    original_text = re.sub(r"\s+","", original_text)
    #print(original_text)

    key_word = input('Enter desired key word for encryption: ')
    key_word = key_word.lower()
    
    key_list = []
    while key_length < len(original_text):
        for letter in key_word:
            if key_length < len(original_text):
                key_list.append(letter)
                key_length +=1
    #print(key_list)

    encrypted_text_list = []
    index_value = 0
    key_pointer = 0

    for character in original_text:
        if character.isdigit():
            encrypted_text_list.append(character)
        else:
            new_index_value = english_alphabets.index(key_list[key_pointer]) +\
                english_alphabets.index(character)
            if new_index_value > 25:
                new_index_value -= 26
            encrypted_text_list.append(english_alphabets[new_index_value])
            key_pointer +=1
    print (''.join(encrypted_text_list))


def vigenere_decipher():
    '''
    This function deciphers any vigenere_ciphered message

    Parameter:
    N/A (the user will be prompted)
    Returns:
    deciphered message
    '''
    
    original_text = input('Enter the text you want to decipher: ')
    key_word = input('Enter the shared key word: ')

    key_length = 0
    key_list = []

    while key_length < len(original_text):
        for letter in key_word:
            if key_length < len(original_text):
                key_list.append(letter)
                key_length+=1
    print(key_list)

    decrypted_text_list = []
    index_value = 0
    key_pointer = 0

    for char in original_text:
        if char.isdigit():
            decrypted_text_list.append(char)
        else:
            new_index = english_alphabets.index(char) - \
                        english_alphabets.index(key_list[key_pointer])
            if new_index < 0:
                new_index += 26
            decrypted_text_list.append(english_alphabets[new_index])
            key_pointer +=1
    print(''.join(decrypted_text_list))


def main():
    pass

if __name__ == '__main__':
    main()