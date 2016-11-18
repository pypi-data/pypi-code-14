class C2(persistent.Persistent):
  def __hash__(self):
      return hash(self.v)
  def __eq__(self, other):
      return self.v == other.v
  def __init__(self, v):
      self.v = v
