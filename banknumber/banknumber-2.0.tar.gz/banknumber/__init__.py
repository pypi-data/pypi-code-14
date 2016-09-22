#This file is part of banknumber. The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

import string

'''
Check the Bank code depending on the country
'''
__version__ = '2.0'


def countries():
    '''
    Return the list of country's codes that have check function
    '''
    res = [x.replace('check_code_', '').upper() for x in globals()
          if x.startswith('check_code_')]
    res.sort()
    return res


def check_code_es(number):
    '''
    Check Spanish Bank code.
    '''
    def get_control(ten_digits):
        values = [1, 2, 4, 8, 5, 10, 9, 7, 3, 6]
        value = ten_digits
        control = 0
        for i in range(10):
            control += int(int(value[i]) * values[i])
        control = 11 - (control % 11)
        if control == 11:
            control = 0
        elif control == 10:
            control = 1
        return control

    if len(number) != 20 or not number.isdigit():
        return False

    value = '00' + number[0:8]
    d1 = get_control(value)
    if d1 != int(number[8]):
        return False

    value = number[10:20]
    d2 = get_control(value)
    if d2 != int(number[9]):
        return False

    return True


def check_code(country, account):
    '''
    Check bank code for the given country which should be a
    two digit ISO 3166 code.
    '''
    try:
        checker = globals()['check_code_%s' % country.lower()]
    except KeyError:
        return False
    return checker(account)

#
#  The following code is addapted from django-iban.
#
#  See:
#  https://github.com/benkonrath/django-iban
#

# Dictionary of ISO country code to IBAN length.
# Data from:
# https://en.wikipedia.org/wiki/International_Bank_Account_Number
iban_length = {'AL': 28,
               'AD': 24,
               'AT': 20,
               'AZ': 28,
               'BE': 16,
               'BH': 22,
               'BA': 20,
               'BG': 22,
               'CR': 21,
               'HR': 21,
               'CY': 28,
               'CZ': 24,
               'DK': 18,
               'DO': 28,
               'EE': 20,
               'FO': 18,
               'FI': 18,
               'FR': 27,
               'GE': 22,
               'DE': 22,
               'GI': 23,
               'GR': 27,
               'GL': 18,
               'HU': 28,
               'IS': 26,
               'IE': 22,
               'IL': 23,
               'IT': 27,
               'KZ': 20,
               'KW': 30,
               'LV': 21,
               'LB': 28,
               'LI': 21,
               'LT': 20,
               'LU': 20,
               'MK': 19,
               'MT': 31,
               'MR': 27,
               'MU': 30,
               'MC': 27,
               'MD': 24,
               'ME': 22,
               'NL': 18,
               'NO': 15,
               'PS': 29,
               'PL': 28,
               'PK': 24,
               'PT': 25,
               'RO': 24,
               'SM': 27,
               'SA': 24,
               'RS': 22,
               'SK': 24,
               'SI': 19,
               'ES': 24,
               'SE': 24,
               'CH': 21,
               'TN': 24,
               'TR': 26,
               'AE': 23,
               'GB': 22,
               'VG': 24,
               'PF': 27,
               'TF': 27,
               'YT': 27,
               'NC': 27,
               'PM': 27,
               'WF': 27}


def check_iban(value):
    """ Validation for ISO 13616-1:2007 (IBAN). """

    country_code = value[:2]
    if country_code in iban_length:
        if iban_length[country_code] != len(value):
            return False
    else:
        return False

    value = value[4:] + value[:4]

    value_digits = ""
    for x in value:
        ord_value = ord(x)
        if 48 <= ord_value <= 57:  # 0 - 9
            value_digits += x
        elif 65 <= ord_value <= 90:  # A - Z
            value_digits += str(ord_value - 55)
        else:
            return False

    if int(value_digits) % 97 != 1:
        return False
    return True
