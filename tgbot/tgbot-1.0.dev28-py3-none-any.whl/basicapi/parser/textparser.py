# -*- coding: utf-8 -*-
__author__ = 'Thomas'


from abc import ABCMeta,abstractmethod

class MessageAbstract(metaclass=ABCMeta):
   def parsetext(self,message):
      pass
