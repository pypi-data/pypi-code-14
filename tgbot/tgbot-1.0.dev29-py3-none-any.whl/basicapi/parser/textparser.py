# -*- coding: utf-8 -*-
__author__ = 'Thomas'


from abc import ABCMeta,abstractmethod

class MessageAbstract(metaclass=ABCMeta):

   @abstractmethod
   def parsemessage(self,message):
      pass
