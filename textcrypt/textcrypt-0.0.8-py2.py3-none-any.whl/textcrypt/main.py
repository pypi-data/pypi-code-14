from Crypto.Cipher import AES
import base64
import os

class encryption:
  def __init__(self):
    doNothing = True

  def keyGen(self, size=16):
    secret = os.urandom(size)
    return secret

  def padKey(self, text):
    if len(text) <= 16:
      for i in range(0, 16 - len(text)):
        text += '$'
    else:
      text = text[0:16]
    return text

  def encrypt(self, privateInfo, key):
    BLOCK_SIZE = 16
    PADDING = '{'
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    secret = key
    cipher = AES.new(secret)
    encoded = EncodeAES(cipher, privateInfo)
    return encoded

  def decrypt(self, encryptedString, key):
    PADDING = '{'
    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e))
    encryption = encryptedString
    cipher = AES.new(key)
    decoded = DecodeAES(cipher, encryption)
    # Find the end
    notHit = True
    index = len(decoded)
    while notHit:
      index -= 1
      if not decoded[index] == PADDING:
        notHit = False
    decoded = decoded[0:index+1]
    return decoded
