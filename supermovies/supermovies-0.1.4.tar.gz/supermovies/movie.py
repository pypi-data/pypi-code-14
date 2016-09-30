from collections import defaultdict

from . import RankableMixin
from . import Snack

class Movie(RankableMixin):
  def __init__(self, title, rank=0):
    self.set_title(title)
    self.set_rank(rank)
    self.__snack_carbs = defaultdict(lambda: 0)

  @classmethod
  def from_csv(cls, line):
    name, rank = line.strip().split(',')
    return cls(name, rank)

  def to_csv(self):
    return "{},{}".format(self.get_title(),self.get_rank())

  def get_title(self):
    return self._title

  def set_title(self, new_title):
    self._title = new_title.capitalize()

  def increment_rank(self):
    self._rank += 1

  def decrement_rank(self):
    self._rank -= 1

  def get_rank(self):
    return self._rank

  def set_rank(self, new_rank):
    self._rank = self.filter(new_rank)

  # Generator
  def snacks(self):
    for name, carbs in self.__snack_carbs.items():
      yield( Snack(name, carbs) )

  def carbs_consumed(self):
    return sum(self.__snack_carbs.values())

  def ate_snack(self, snack):
    self.__snack_carbs[snack.name] += snack.carbs
    print("{} led to {} {} carbs being consumed.".format(self.get_title(), snack.carbs, snack.name))
    print("{}'s snacks: {}".format(self.get_title(), dict(self.__snack_carbs)))

  @staticmethod
  def filter(value):
    try:
      return int(value)
    except:
      raise ValueError('Movie rank must be an integer. Value given: %s' % value)

  def __str__(self):
    return "%s has a rank of %d (%s)" % (self.get_title(), self.get_rank(), self.status)

  def __repr__(self):
    return self.__str__()

if __name__ == '__main__':
  movie = Movie("goonies", 15)
  print(movie)
  movie.thumbs_up()
  movie.thumbs_up()
  print(movie)
  print(movie.get_title())