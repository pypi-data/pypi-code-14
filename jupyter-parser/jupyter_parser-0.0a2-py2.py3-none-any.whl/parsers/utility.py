import os


def header(text):
    """given text, return text centered in terminal"""
    rows, columns = os.popen('stty size', 'r').read().split()
    text = ' ' + text + ' '
    return text.center(int(columns), "#")
