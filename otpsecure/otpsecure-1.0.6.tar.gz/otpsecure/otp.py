from otpsecure.base import Base

class Otp(Base):
  def __init__(self):
    self.clientToken    = None
    self.clientOtp      = None
    self.id             = None
    self.customid       = None
    self.pdf_shortUrl   = None
    self.html_shortUrl  = None