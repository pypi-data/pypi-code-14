'''
Created on 16 Sep 2016
@author: rizarse
'''

import jks, textwrap, base64
from os.path import expanduser
import os.path

from os import makedirs

class JksHandler(object):

    def __init__(self, params):
        pass
    
    @staticmethod
    def writePkAndCerts(ks):
        
        uid = None
        
        home = expanduser("~")
        
        for alias, pk in ks.private_keys.items(): 
            
            uid = alias
            
            if pk.algorithm_oid == jks.util.RSA_ENCRYPTION_OID:
                
                if os.path.exists(home + '/magistral/' + uid) == False:
                    makedirs(home + '/magistral/' + uid)
                
                key = home + '/magistral/' + uid + '/key.pem'
                
                if os.path.exists(key): os.remove(key) 
                                
                with open(key, 'wb') as f:
                    f.seek(0)
                    f.write(bytearray(b"-----BEGIN RSA PRIVATE KEY-----\r\n"))
                    f.write(bytes("\r\n".join(textwrap.wrap(base64.b64encode(pk.pkey).decode('ascii'), 64)), 'utf-8'))
                    f.write(bytearray(b"\r\n-----END RSA PRIVATE KEY-----"))                    
                    f.close()   
             
            counter = 0;
            
            cert = home + '/magistral/' + uid + '/certificate.pem'
            if os.path.exists(cert): os.remove(cert)
            
            with open(cert, 'wb') as f:
                f.seek(0)
                   
                for c in pk.cert_chain:               
                    f.write(bytearray(b"-----BEGIN CERTIFICATE-----\r\n"))
                    f.write(bytes("\r\n".join(textwrap.wrap(base64.b64encode(c[1]).decode('ascii'), 64)), 'utf-8'))
                    f.write(bytearray(b"\r\n-----END CERTIFICATE-----\r\n"))   
                    counter = counter + 1
                    if (counter == 2): break                 
                
                f.close()
            
            ca = home + '/magistral/' + uid + '/ca.pem'
            if os.path.exists(ca): os.remove(ca)
            
            with open(ca, 'wb') as f:         
                for alias, c in ks.certs.items():    
                    f.write(bytearray(b"-----BEGIN CERTIFICATE-----\r\n"))
                    f.write(bytes("\r\n".join(textwrap.wrap(base64.b64encode(c.cert).decode('ascii'), 64)), 'utf-8'))
                    f.write(bytearray(b"\r\n-----END CERTIFICATE-----\r\n"))                    
                    
                f.close()
            
        return uid
                 
    
    @staticmethod
    def printJks(ks):
        
        def print_pem(der_bytes, type):
            print("-----BEGIN %s-----" % type)
            print("\r\n".join(textwrap.wrap(base64.b64encode(der_bytes).decode('ascii'), 64)))
            print("-----END %s-----" % type)

    
        for alias, pk in ks.private_keys.items():
            print("Private key: %s" % pk.alias)
            if pk.algorithm_oid == jks.util.RSA_ENCRYPTION_OID:
                print_pem(pk.pkey, "RSA PRIVATE KEY")
            else:
                print_pem(pk.pkey_pkcs8, "PRIVATE KEY")
        
            for c in pk.cert_chain:
                print_pem(c[1], "CERTIFICATE")
            print()
        
        for alias, c in ks.certs.items():
            print("Certificate: %s" % c.alias)
            print_pem(c.cert, "CERTIFICATE")
            print()
        
        for alias, sk in ks.secret_keys.items():
            print("Secret key: %s" % sk.alias)
            print("  Algorithm: %s" % sk.algorithm)
            print("  Key size: %d bits" % sk.key_size)
            print("  Key: %s" % "".join("{:02x}".format(b) for b in bytearray(sk.key)))
            print()    
