'''
Major rewrite of vigenere cipher

Goal:
more efficient implementation using modular arithmetic

Required mods:
a. fix the key key spanning over the message
b. deal with the empty spaces

'''


def vigenere_cipher():

    original_text = input('Enter the text you desire to encrypt: ')
    original_text = original_text.lower()
    keyword = input('Enter the encryption key word: ')
    keyword = list(keyword)

    ciphered_text = []

    for character in original_text:
        if character.isdigit():
            ciphered_text.append(character)

        elif character == '':
            continue

        elif character in english_alphabets:
            ciphered_text.append(english_alphabets[
                                     (english_alphabets.index(
                                         character) + keyword.index()) % 26])

    print(''.join(ciphered_text))



