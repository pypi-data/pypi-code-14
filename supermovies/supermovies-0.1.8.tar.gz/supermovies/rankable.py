class RankableMixin:
  def thumbs_up(self):
    self.increment_rank()

  def thumbs_down(self):
    self.decrement_rank()

  @property
  def normalized_rank(self):
    return self.get_rank() / 10

  @property
  def status(self):
    return 'Hit' if self.is_a_hit() else 'Flop'

  def is_a_hit(self):
    return self.get_rank() >= 10

  def __lt__(self, other):
    return other.get_rank() < self.get_rank()
