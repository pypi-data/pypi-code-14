from random import randint
from abc import ABC, abstractmethod

from . import Die

class Reviewer(ABC):

  @classmethod
  @abstractmethod
  def review(cls, movie):
    raise NotImplementedError

class WaldorfAndStatler(Reviewer):

  @classmethod
  def review(cls, movie):
    number_rolled = Die.roll()
    if number_rolled < 3:
      movie.thumbs_down()
      print("%s got a thumbs down." % movie.get_title())
    elif number_rolled < 5:
      print("%s was skipped!" % movie.get_title())
    else:
      movie.thumbs_up()
      print("%s got a thumbs up!" % movie.get_title())

class BadMan(Reviewer):
  @classmethod
  def review(cls, movie):
    number_rolled = Die.roll()
    if number_rolled == 6:
      print("%s was skipped!" % movie.get_title())
    else:
      movie.thumbs_down()
      print("%s got a thumbs down." % movie.get_title())
