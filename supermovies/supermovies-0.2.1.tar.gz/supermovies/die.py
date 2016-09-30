from random import randint

class Die:
  @classmethod
  def roll(cls):
    return randint(1, 6)