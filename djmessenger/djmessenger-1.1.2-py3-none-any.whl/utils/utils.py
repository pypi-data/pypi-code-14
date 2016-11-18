# -*- coding: utf-8 -*-
import importlib
import logging

from djmessenger.utils.serializable import Serializable


logger = logging.getLogger(__name__)


def load_class(fully_qualified_name):
    """Load class by its fully qualified name

    :param fully_qualified_name: if given fully qualified name is a.b.c, try to load the
                      module from a.b and load the class c in a.b module
    :return: A class
    :raise ImportError: not able to load module
    :raise AttributeError: not able to load class
    """
    tokens = fully_qualified_name.split('.')
    # if len(tokens) == 1, then it is a module, raise exception
    if len(tokens) == 1:
        raise ValueError('The fully qualified name you gave was %s which can '
                         'not represent a class but a module' % fully_qualified_name)
    else:
        class_name = tokens.pop()
        module_name = '.'.join(tokens)

    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        logger.error('Not able to import module named %s' % module_name)
        raise e
    try:
        ret = getattr(module, class_name)
    except AttributeError as e:
        logger.error('Not able to get class %s from module %s' %
                     (class_name, module_name))
        raise e
    return ret


def get_class_name(obj):
    """
    Given a type of an instance, return its fully qualified class name

    :param obj:
    :type obj: type or object
    :return: fully qualified class name
    :rtype: str
    """
    if not isinstance(obj, type):
        raise ValueError('Given class must be a type')
        return '%s.%s' % (obj.__module__, obj.__name__)
    else:
        return '%s.%s' % (obj.__module__, obj.__class__.__name__)


class LocalizedString(Serializable):
    """
    We are using this LocalizedString class to implement i18n support, so every
    string that needs to be localized(including variables in settings), needs
    to be able to deserialize back to this class

    The json format is

    ::

        {
          "base_string": "default string, in any language, if locale not found, then use this",
          "translations": {
            "en_US": "English translation",
            "zh_TW": "Traditional Chinese translation",
            ...
          }
        }

    The key in translations dict is locale defined by Facebook and can be found
    in facebook_locales.py
    """
    def __init__(self, base_string, translations):
        """

        :param base_string: base string
        :param translations: a dict which maps from FacebookLocale to its
                             corresponding translation
        """
        self.base_string = base_string
        self.translations = translations

    def get_text_by_locale(self, locale):
        """

        :param locale:
        :type locale: FacebookLocale
        :return:
        """
        if locale.name in self.translations and self.translations[locale.name]:
            return self.translations[locale.name]
        else:
            return self.base_string
