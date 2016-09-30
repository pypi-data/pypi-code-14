from random import choice
from collections import namedtuple

Snack = namedtuple('Snack', ('name', 'carbs'))

class SnackBar:
  SNACKS = [
    Snack('popcorn', 20),
    Snack('candy', 15),
    Snack('nachos', 40),
    Snack('pretzel', 10),
    Snack('soda', 5)
  ]

  @classmethod
  def random(cls):
    return choice(cls.SNACKS)

if __name__ == '__main__':
  popcorn = Snack('popcorn', 20)
  print(popcorn.name)
  print(popcorn.carbs)

  candy = Snack('candy', 15)
  print(candy.name)
  print(candy.carbs)

  print(SnackBar.SNACKS)
  snack = SnackBar.random()
  print("Enjoy your {} ({} carbs)".format(snack.name, snack.carbs))