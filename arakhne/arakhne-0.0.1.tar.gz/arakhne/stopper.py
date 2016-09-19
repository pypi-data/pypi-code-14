# -*- coding: utf-8 -*-

# ===============
# David J. Thomas
#  thePortus.com
# ===============

import os
from collections import UserList
from nltk.tokenize.punkt import PunktLanguageVars


class Stopper(UserList):
    """ Stopper

    Gets a filepath containing stopwords and provides filtering

    Extends:
        UserList
    """

    def __init__(self, **kwargs):
        """
        Constructs and stores filepath and attempts to load specified file

        Arguments:
            filepath {str} -- stopword filepath

        Keyword Arguments:
            absolute {bool} -- is filepath rel/abs (default: {False})
        """

        # Calling superclass init function
        super().__init__()
        # Only building path and auto-loading if path argument sent
        if 'path' not in kwargs:
            self.path = ''
        elif kwargs['path'] != '':
            # If 'absolute' specified, take as is, else build path
            if 'absolute' in kwargs:
                self.path = kwargs['path']
            else:
                self.path = os.path.join(
                    os.path.abspath(
                        os.getcwd()
                    ),
                    kwargs['path']
                )
            # If encoding is specified, copy it, else default to utf-8
            if 'encoding' in kwargs:
                self.encoding = kwargs['encoding']
            else:
                self.encoding = 'utf-8'
            # Calling loading method
            self.load()
        # If a pre-loaded list was passed, add all pharases inside
        if 'list' in kwargs:
            for stop_phrase in kwargs['list']:
                self.data.append(stop_phrase)

    def load(self, path=None):
        """
        Loads the list of stopwords from the specified file
        """
        if not self.path and not path:
            print('Error, no path specified')
            return False
        # If no file is found, raise an exception
        if not os.path.exists(self.path):
            print('Error: no file found at', self.path)
            raise FileNotFoundError
        # Opening the file
        with open(
            self.path, mode='r+', encoding=self.encoding, newline='\n'
        ) as stop_file:
            # Looping each line and appending the instance
            for stop_phrase in stop_file:
                self.data.append(stop_phrase.lower().strip())
        self.data = sorted(list(set(self.data)))
        return True

    def add(self, other):
        """
        Appends all the items from another stoplist to the current

        Arguments:
            other {list} -- List to copy

        Raises:
            TypeError -- In case other is non-list
        """

        if type(other) != list:
            raise TypeError
        new_list = self.data
        for stop_phrase in other:
            new_list.append(stop_phrase)
        return self.__class__(list=sorted(list(set(new_list))))

    def filter(self, text):
        """ filter

        Filters received text of stopwords from the file specified on init

        Arguments:
            text {str} -- text to filter of stopwords
        """

        # Make tokenizer and tokenize received text
        tokenizer = PunktLanguageVars()
        tokens = tokenizer.word_tokenize(str(text).lower())
        filtered_words = []
        for word in tokens:
            if word not in self.data:
                filtered_words.append(word)
        return " ".join(filtered_words)
