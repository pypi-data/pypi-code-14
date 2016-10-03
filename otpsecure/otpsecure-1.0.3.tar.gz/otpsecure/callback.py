from otpsecure.base import Base

class Callback(Base):
  def __init__(self):
    self.id             = None
    self.cid            = None
    self.status 		= None
    self.filename	    = None
    self.filecontent    = None