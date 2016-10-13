# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from random import randrange, sample
from sys import stdin, stdout


__version__ = "0.0.4"


_RUNES = (
  (
    u"\u030d", u"\u030e", u"\u0304", u"\u0305", u"\u033f", u"\u0311",
    u"\u0306", u"\u0310", u"\u0352", u"\u0357", u"\u0351", u"\u0307",
    u"\u0308", u"\u030a", u"\u0342", u"\u0343", u"\u0344", u"\u034a",
    u"\u034b", u"\u034c", u"\u0303", u"\u0302", u"\u030c", u"\u0350",
    u"\u0300", u"\u0301", u"\u030b", u"\u030f", u"\u0312", u"\u0313",
    u"\u0314", u"\u033d", u"\u0309", u"\u0363", u"\u0364", u"\u0365",
    u"\u0366", u"\u0367", u"\u0368", u"\u0369", u"\u036a", u"\u036b",
    u"\u036c", u"\u036d", u"\u036e", u"\u036f", u"\u033e", u"\u035b",
    u"\u0346", u"\u031a",
  ),
  (
    u"\u0315", u"\u031b", u"\u0340", u"\u0341", u"\u0358", u"\u0321",
    u"\u0322", u"\u0327", u"\u0328", u"\u0334", u"\u0335", u"\u0336",
    u"\u034f", u"\u035c", u"\u035d", u"\u035e", u"\u035f", u"\u0360",
    u"\u0362", u"\u0338", u"\u0337", u"\u0361", u"\u0489",
  ),
  (
    u"\u0316", u"\u0317", u"\u0318", u"\u0319", u"\u031c", u"\u031d",
    u"\u031e", u"\u031f", u"\u0320", u"\u0324", u"\u0325", u"\u0326",
    u"\u0329", u"\u032a", u"\u032b", u"\u032c", u"\u032d", u"\u032e",
    u"\u032f", u"\u0330", u"\u0331", u"\u0332", u"\u0333", u"\u0339",
    u"\u033a", u"\u033b", u"\u033c", u"\u0345", u"\u0347", u"\u0348",
    u"\u0349", u"\u034d", u"\u034e", u"\u0353", u"\u0354", u"\u0355",
    u"\u0356", u"\u0359", u"\u035a", u"\u0323"
  )
)

def _is_rune(x):
  return any(x in runes for runes in _RUNES)


POSITION_NONE = 0x0000
POSITION_DOWN = 0x0001
POSITION_MIDDLE = 0x0002
POSITION_UP = 0x0004


class Z(object):
  def __init__(self, magnitude=0, positions=POSITION_MIDDLE|POSITION_DOWN):
    assert magnitude in range(0, 3)
    self.magnitude = magnitude
    self.positions = positions

  def corrupt(self, xs):
    return u"".join(self.integrate(x) for x in xs)

  def integrate(self, x):
    if _is_rune(x) or not x.strip():
      return x

    retval = [x]
    levels = self._gen_random_sz()

    size = (
      levels[0] if POSITION_UP   & self.positions else 0,
      levels[1] if POSITION_MIDDLE & self.positions else 0,
      levels[2] if POSITION_DOWN   & self.positions else 0,
    )

    retval += sample(_RUNES[0], size[0])
    retval += sample(_RUNES[1], size[1])
    retval += sample(_RUNES[2], size[2])
    return u"".join(retval)

  def _gen_random_sz(self):
    return (
      (
        randrange(0, 8, 1),
        randrange(0, 2, 1),
        randrange(0, 8, 1),
      ),
      (
        randrange(0, 16, 1) // 2 + 1,
        randrange(0, 6, 1)  // 2,
        randrange(0, 16, 1) // 2 + 1,
      ),
      (
        randrange(0, 64, 1) // 4 + 3,
        randrange(0, 16, 1) // 4 + 1,
        randrange(0, 64, 1) // 4 + 3,
      )
    )[self.magnitude]


def main():
  parser = ArgumentParser(description="Invoke chaos")

  parser.add_argument("-v", "--version",
                      action="version",
                      version=__version__)

  parser.add_argument("-u", "--up",
                      action="append_const",
                      dest="positions",
                      const=POSITION_UP)

  parser.add_argument("-m", "--middle",
                      action="append_const",
                      dest="positions",
                      const=POSITION_MIDDLE)

  parser.add_argument("-d", "--down",
                      action="append_const",
                      dest="positions",
                      const=POSITION_DOWN)

  parser.add_argument("-s", "--size",
                      action="store",
                      type=int,
                      choices=list(range(0, 3)),
                      default=0)

  args = parser.parse_args()

  positions = POSITION_NONE
  for p in args.positions or []:
    positions |= p

  if POSITION_NONE == positions:
    positions = POSITION_MIDDLE|POSITION_DOWN

  z = Z(args.size, positions)
  for line in stdin:
    stdout.write(z.corrupt(line.decode("utf_8")).encode("utf_8"))


if "__main__" == __name__:
  main()
