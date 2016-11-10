from otpsecure.base import Base

class Document(Base):
  def __init__(self):
    self.filename	    = None
    self.filecontent    = None
