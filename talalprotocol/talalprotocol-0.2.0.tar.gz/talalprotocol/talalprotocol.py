# -----------------------------------------------------------------------------
# Name: talalprotocol
# Purpose: provide various encryption algorithms
#
# Author: Talal Khalil
# Start Date: 8/01/2016
# Latest mod: 9/20/2016
#
# -----------------------------------------------------------------------------

'''
This module provides the following encryption functions:


1. Vigenere Cipher
    function calls:
        a. vigenere_cipher(message, key)
        b. vigenere_decipher(message, key)

2. Caesar Cipher
    function calls:
        a. caesar_cipher(message, shift_value)
        b. caesar_decipher(message, shift_value)

3. Binary Encryption algorithm (custom)
    function call:
        a. binary_encryption(message)

'''

import string
x = string.ascii_lowercase
english_alphabets = list(x)
string_punctuation = string.punctuation

def caesar_cipher(message, shift_value):
    '''
        This function ciphers any submitted message using Caesar Cipher

        Encryption mathematical representation:
        caesar_cipher(x) = (x + n) mod 26
        x: letter index     n: shift value

        Parameters:
        message
        shift value

        Returns:
        ciphered text
        '''

    # handles floats
    shift_value = int(shift_value)

    # handles negative shift values
    check = True
    while check:
        if shift_value < 0:
            print('Shift values should be positive. Try again.')
            quit()
        else:
            check = False

    message = message.lower()
    ciphered_text = ''

    #string_punctuation = string.punctuation

    for char in message:
        if char.isdigit():
            ciphered_text = ciphered_text + char
        elif char in string_punctuation:
            ciphered_text = ciphered_text + char
        elif char in english_alphabets:
            ciphered_text = ciphered_text + (
            english_alphabets[(english_alphabets.index(
                char) + shift_value) % 26])
        else:
            ciphered_text = ciphered_text + ' '

    #print(ciphered_text)
    return ciphered_text


def caesar_decipher(message, shift_value):
    '''
    This function ciphers any submitted message using Caesar Cipher

        Encryption mathematical representation:
        caesar_cipher(x) = (x - n) mod 26
        x: letter index     n: shift value

        Parameters:
        message
        shift value

        Returns:
        ciphered text

    '''

    shift_value = int(shift_value)

    check = True
    while check:
        if shift_value < 0:
            print('Shift values should be positive. Try again.')
            quit()
        else:
            check = False

    message = message.lower()
    ciphered_text = ''
    #string_punctuation = string.punctuation

    for char in message:
        if char.isdigit():
            ciphered_text = ciphered_text + char

        elif char in string_punctuation:
            ciphered_text = ciphered_text + char


        elif char in english_alphabets:
            ciphered_text = ciphered_text + (
            english_alphabets[(english_alphabets.index(
                char) - shift_value) % 26])
        else:
            ciphered_text = ciphered_text + ' '

    #print(ciphered_text)
    return ciphered_text


def vigenere_cipher(message,key):
    '''
    This function ciphers any submitted message using Vigenere Cipher

    Encryption mathematical representation:
    vigenere_cipher(y) = (y + k) mod 26
    y: letter index   k: corresponding key letter index

    Parameters:
    message
    key

    Returns:
    ciphered text
    '''
    message = message.lower()
    key = key.lower()

    key_list = []
    key_length = 0

    while key_length < len(message):
        for letter in key:
            if key_length < len(message):
                key_list.append(letter)
                key_length += 1
    # print(key_list)

    encrypted_message = ''
    index_value = 0
    key_pointer = 0

    for character in message:
        if character.isdigit():
            encrypted_message = encrypted_message + character

        elif character in string_punctuation:
            ciphered_text = encrypted_message + character

        elif character in english_alphabets:
            new_index_value = english_alphabets.index(key_list[key_pointer]) + \
                              english_alphabets.index(character)
            if new_index_value > 25:
                new_index_value -= 26
            encrypted_message = encrypted_message + (
            english_alphabets[new_index_value])
            key_pointer += 1
        else:
            encrypted_message = encrypted_message + ' '

    return encrypted_message

def vigenere_decipher(message, key):
    '''
    This function deciphers any vigenere_ciphered message

    Parameters:
    message
    key

    Returns:
    deciphered message
    '''
    key_length = 0
    key_list = []

    while key_length < len(message):
        for letter in key:
            if key_length < len(message):
                key_list.append(letter)
                key_length += 1

    decrypted_message = ''
    index_value = 0
    key_pointer = 0

    for character in message:
        if character.isdigit():
            decrypted_message = decrypted_message + character

        elif character in string_punctuation:
            decrypted_message = decrypted_message + character

        elif character in english_alphabets:
            new_index = english_alphabets.index(character) - \
                        english_alphabets.index(key_list[key_pointer])
            if new_index < 0:
                new_index += 26
            decrypted_message = decrypted_message + (english_alphabets[new_index])
            key_pointer += 1
        else:
            decrypted_message = decrypted_message + ' '

    return decrypted_message



def converting_to_binary(item1):

    digit_list = list(string.digits)
    string_punctuation = list(string.punctuation)

    if item1 in digit_list:
        # added 32 = 100000 as a flag bit to indicate that a char is a digit
        item1 = int(item1) + 32
        binary_value = bin(item1)[2:].zfill(6)
    else:
        binary_value = bin(item1)[2:].zfill(6)

    return binary_value



def binary_encryption(message):
    '''
    This is a custom encryption algorithm and documentation is still private

    Parameter:
    message

    Returns:
    encrypted message
    '''

    message = message.lower()
    binary_ciphered_message = ''

    for char in message:
        if char.isdigit():
            digit_in_binary = converting_to_binary(char)
            binary_ciphered_message += digit_in_binary

        elif char in string_punctuation:
            binary_ciphered_message += char

        elif char in english_alphabets:
            index = english_alphabets.index(char)
            x = converting_to_binary(index)
            binary_ciphered_message += x
        else:
            binary_ciphered_message += ' '

    return binary_ciphered_message



def main():
    pass


if __name__ == '__main__':
    main()
