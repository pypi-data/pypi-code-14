import sys
import os
import base64
import binascii
import traceback
import StringIO
import Crypto
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA512


class SeasCrypto:
	def __init__(self,  k=16):
		self.k = k
	
	def symmetricEncrypt(self, key, text):
		try :
			iv = os.urandom(16)
			aesCipher = AES.new(key, AES.MODE_CBC, iv)
			cipherText = aesCipher.encrypt(self.PKCS7pad(text))
			
			return base64.b64encode(iv) + base64.b64encode(cipherText)
		except:
			print "Error in symmetric encryption."
			print sys.exc_info()[1]
			return None
	
	def symmetricDecrypt(self, key, text):
		decodedIv = base64.b64decode(text[0:24])
		decodedContent = base64.b64decode(text[24:])
		
		try :
			aesCipher = AES.new(key, AES.MODE_CBC, decodedIv)
			return self.PKCS7strip(aesCipher.decrypt(decodedContent))
		except:
			print "Symmetric decryption failed"
			print sys.exc_info()[1]
			return None
		
	def asymmetricEncrypt(self, pubKey, text):
		try :
			# 16 bytes = 128 bits
			aesKey = os.urandom(16)
			iv = os.urandom(16)
			aesCipher = AES.new(aesKey, AES.MODE_CBC, iv)
			pkcsCipher = PKCS1_OAEP.new(pubKey)
			cipherText = aesCipher.encrypt(self.PKCS7pad(text))
			keyText = pkcsCipher.encrypt(aesKey)

			return base64.b64encode(keyText) + "\n" + base64.b64encode(iv) + base64.b64encode(cipherText), aesKey
		except:
			print "Error while encrypting."
			print sys.exc_info()[1]
			traceback.print_exc()
			return None
	
	def asymmetricDecrypt(self, privKey, text):
		keyEnd = text.find('\n')
		
		decodedKey = base64.b64decode(text[0:keyEnd])
		decodedIv = base64.b64decode(text[keyEnd+1:keyEnd+25])
		decodedContent = base64.b64decode(text[keyEnd+25:])
		
		try :
			pkcsCipher = PKCS1_OAEP.new(privKey)
			decryptedKey = pkcsCipher.decrypt(decodedKey)
			aesCipher = AES.new(decryptedKey, AES.MODE_CBC, decodedIv)
			return self.PKCS7strip(aesCipher.decrypt(decodedContent)), decryptedKey
		except:
			print "Decryption failed"
			print sys.exc_info()[1]
			return None, None
	
	def sign(self, privKey, dataBytes):
		# create a signature for the bytes
		hash = SHA512.new(self, dataBytes).digest()
		signature = privKey.sign(hash, '')
		return base64.base64dencode(signature)
	
	def verifySignature(signature, pubKey, dataBytes):
		signatureBytes =  base64.base64decode(signature)
		hash = SHA512.new(dataBytes).digest()
		return pubKey.verify(hash, signature)
	
	def extractPemFormatPrivateKey(self, key, algorithm):
		if (algorithm == "RSA"):
			return RSA.importKey(key)
		return None
		
	def extractPemFormatPublicKey(self, key, algorithm):
		if (algorithm == "RSA"):
			return RSA.importKey(key)
		return None
	
	def PKCS7strip(self, text):
		'''
		Remove the PKCS#7 padding from a text string
		'''
		nl = len(text)
		val = int(binascii.hexlify(text[-1]), 16)
		if val > self.k:
			raise ValueError('Input is not padded or padding is corrupt')

		l = nl - val
		return text[:l]
	
	def PKCS7pad(self, text):
		'''
		Pad an input string according to PKCS#7
		'''
		l = len(text)
		output = StringIO.StringIO()
		val = self.k - (l % self.k)
		for _ in xrange(val):
			output.write('%02x' % val)
		return text + binascii.unhexlify(output.getvalue())