__author__ = "Kiran Vemuri"
__email__ = "kkvemuri@uh.edu"
__status__ = "Development"
__maintainer__ = "Kiran Vemuri"

import random
from netaddr import IPNetwork
import string


def random_ip(ip_class='A'):
    """
    Generate random IP address with the specified class
    :param ip_class: <str> class of IP that is to be generated
    :return: IP Network object for the random IP address
    """
    # CLASSES = 'ABC'
    # ip_class = random.choice(CLASSES)

    if ip_class in ["A", "a"]:
        first_octet = random.randint(1, 126)
        cidr_bits = random.randint(8, 30)
    elif ip_class in ["B", "b"]:
        first_octet = random.randint(128, 191)
        cidr_bits = random.randint(16, 30)
    elif ip_class in ["C", "c"]:
        first_octet = random.randint(192, 223)
        cidr_bits = random.randint(24, 30)

    second_octet = random.randint(0, 254)
    third_octet = random.randint(0, 254)
    fourth_octet = random.randint(0, 254)

    rand_ip = "{}.{}.{}.{}/{}".format(first_octet, second_octet, third_octet, fourth_octet, cidr_bits)
    return IPNetwork(rand_ip)


# Function to generate random string
def random_string(str_len, white_space=False, special_char=False):
    """
    Generate a random string of the given length
    :param str_len: <int> length of the string to be generated
    :param white_space: <bool> Include white space as a character for random string True/False
    :param special_char: <bool> Include special characters for the ramdom string True/False
    :return: <str> random string of given length
    """
    char_choice = string.ascii_lowercase + string.ascii_uppercase + string.digits

    if special_char:
        char_choice += "~!@#$%^&*()_+=-{}|:\"<>?[]\;',./"

    if white_space:
        rand_str = ''.join(random.choice(char_choice) for x in xrange(str_len/2 - 1))
        rand_str += ' '
        rand_str += ''.join(random.choice(char_choice) for x in xrange(str_len/2))
    else:
        rand_str = ''.join(random.choice(char_choice) for x in xrange(str_len))

    return rand_str
