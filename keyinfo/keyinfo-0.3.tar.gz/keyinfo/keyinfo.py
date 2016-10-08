__author__ = 'pvde'

# Partly based on an earlier module by EJVN.

from lxml import etree

from cryptography.x509 import NameOID, load_pem_x509_certificate, Certificate

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

import struct, base64, hashlib, logging, re

_NSMAP = {'ds': 'http://www.w3.org/2000/09/xmldsig#',
          'dsig11' : 'http://www.w3.org/2009/xmldsig11#',
          'xml': 'http://www.w3.org/XML/1998/namespace'}

_DIGESTMETHODS = {
    'http://www.w3.org/2001/04/xmlenc#sha512': hashlib.sha512,
    'http://www.w3.org/2001/04/xmlenc#sha256': hashlib.sha256
}

XMLSIG1 = '1.0'
XMLSIG11 = '1.1'


def to_keyinfo_sig1(cert_or_list, prefix=''):
    return to_keyinfo(cert_or_list, prefix, XMLSIG1)

def to_keyinfo_sig11(cert_or_list, prefix=''):
    return to_keyinfo(cert_or_list, prefix, XMLSIG11)

def to_keyinfo(cert_or_list, prefix='', version=XMLSIG11):
    if isinstance(cert_or_list, Certificate):
        first_cert = cert_or_list
        other_certs = []
    elif isinstance(cert_or_list, list):
        first_cert = cert_or_list[0]
        other_certs = cert_or_list[1:]
    else:
        raise Exception('Input must be Certificate or list of Certificates')
    keyinfo = etree.Element(_ds('KeyInfo'), nsmap=_NSMAP)
    _x509keyname(first_cert, keyinfo, prefix)
    _keyvalue(first_cert, keyinfo)
    _x509data(first_cert, other_certs, keyinfo, prefix, version)
    return keyinfo

def from_keyinfo(keyinfo, chain=False):
    return _cert_or_chain_from_keyinfo(keyinfo)

def _cert_or_chain_from_keyinfo(keyinfo, chain=True):
    x509_data = keyinfo.find(_ds('X509Data'))
    x509_cert_list = x509_data.findall(_ds('X509Certificate'))

    first_x509_cert = x509_cert_list[0]
    first_x509_cert_data = first_x509_cert.text

    pem_formatted =_add_pem_delimiters(first_x509_cert.text)
    first_certificate = load_pem_x509_certificate(pem_formatted,
                                                  default_backend())
    _check_x509digest(x509_data, first_x509_cert_data)
    _check_x509_issuer_serial(x509_data, first_certificate)

    if chain:
        cert_list = [first_certificate]
        for x509_cert in x509_cert_list:
            pem_formatted =_add_pem_delimiters(x509_cert.text)
            cert = load_pem_x509_certificate(pem_formatted,
                                             default_backend())
            cert_list.append(cert)
        return cert_list
    else:
        return first_certificate

def _check_x509digest(x509_data, x509_cert_data):
    # Checks that the claimed digests match the certificate
    for x509_digest in x509_data.findall(_dsig11('X509Digest')):
        algorithm = x509_digest.get('Algorithm')
        hashfunction = _DIGESTMETHODS[algorithm]
        stated_digest = x509_digest.text
        computed_digest = base64.b64encode(hashfunction(x509_cert_data).digest())
        if str(stated_digest) != str(computed_digest):
            raise Exception('Mismatch in {} X509Digest: expecting {}, found {}'.format(algorithm,
                                                                                       computed_digest,
                                                                                       stated_digest))

def _check_x509_issuer_serial(x509_data, certificate):
    # Checks that the claimed issuer and serial match the certificate
    expected_issuer = str(_nameattributes(certificate.issuer))
    expected_serial = str(certificate.serial)

    for x509_issuer_serial in x509_data.findall(_ds('X509IssuerSerial')):
        x509_issuer_name = x509_issuer_serial.findtext(_ds('X509IssuerName'))
        x509_serial_number = str(x509_issuer_serial.findtext(_ds('X509SerialNumber')))
        if x509_serial_number != expected_serial:
            raise Exception('Mismatch in serial number: expecting \"{}\", found \"{}\"'.format(expected_serial,
                                                                                       x509_serial_number))
        if x509_issuer_name != expected_issuer:
            raise Exception('Mismatch in X509IssuerName: expecting \"{}\", found \"{}\"'.format(expected_issuer,
                                                                                        x509_issuer_name))

def _keyvalue(cert, keyinfo):
    keyvalue = etree.SubElement(keyinfo, _ds('KeyValue'))
    rsakeyvalue = etree.SubElement(keyvalue, _ds('RSAKeyValue'))
    public_key = cert.public_key()
    if isinstance(public_key, rsa.RSAPublicKey):
        public_numbers = public_key.public_numbers()
        modulus = etree.SubElement(rsakeyvalue, _ds('Modulus'))
        modulus.text = _bigint_to_base64(public_numbers.n)
        exponent = etree.SubElement(rsakeyvalue, _ds('Exponent'))
        exponent.text =  _int_to_base64(public_numbers.e)
    else:
        raise NotImplementedError('Only RSA Keys supported in this version.')


def _int_to_base64(value):
    if value == 0:
        return base64.b64encode('\x00')
    else:
        bytes = struct.pack("!I", value) # to big-endian representation!
        return base64.b64encode(bytes.lstrip('\x00'))

def _bigint_to_base64(i):
    multipleOfTwo = 0
    b = bytearray()
    b.reverse()
    while i:
        multipleOfTwo = (multipleOfTwo + 1) % 2
        b.append(i & 0xFF)
        i >>= 8
    if not multipleOfTwo:
        pass #b.append('\x00')
    b.reverse()
    return _formatBase64( base64.b64encode(b) )

def _formatBase64(base64string):
    length = len(base64string)
    newString = base64string[0:76]
    for i in range(76, length, 76):
        newString = "{}\n{}".format(newString, base64string[i:i+76])
    return newString

def _x509data(cert, othercerts, keyinfo, prefix, version):
    x509data = etree.SubElement(keyinfo,_ds('X509Data'))

    if version is XMLSIG11:
        _x509digest(cert, x509data)
    elif version is XMLSIG1:
        _x509issuer_serial(cert, x509data)
    _x509subjectname(cert, x509data)
    _x509certificate(cert, x509data)
    for other in othercerts:
        _x509certificate(other, x509data)

def _x509certificate(cert, x509data):
    x509cert = etree.SubElement(x509data,_ds('X509Certificate'))
    x509cert.text = _x509certdata(cert)


def _x509subjectname(cert, x509data):
    subjectname = etree.SubElement(x509data, _ds('X509SubjectName'))
    subjectname.text = _nameattributes(cert.subject)

def _x509keyname(cert, keyinfo, prefix):
    x509keyname = etree.SubElement(keyinfo,_ds('KeyName'))
    x509keyname.text = prefix+(cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0]).value

def _x509digest(cert, x509data):
    x509digest = etree.SubElement(x509data, _dsig11('X509Digest'),
                                  Algorithm='http://www.w3.org/2001/04/xmlenc#sha512')
    x509digest.text = base64.b64encode(hashlib.sha512(_x509certdata(cert)).digest())
    x509digest = etree.SubElement(x509data, _dsig11('X509Digest'),
                                  Algorithm='http://www.w3.org/2001/04/xmlenc#sha256')
    x509digest.text = base64.b64encode(hashlib.sha256(_x509certdata(cert)).digest())

def _x509issuer_serial(cert, x509data):
    issuerserial = etree.SubElement(x509data,_ds('X509IssuerSerial'))
    _x509issuername(cert, issuerserial)
    serial = etree.SubElement(issuerserial, _ds('X509SerialNumber'))
    serial.text = str(cert.serial)

def _x509issuername(cert, x509data):
    issuername = etree.SubElement(x509data, _ds('X509IssuerName'))
    issuername.text = _nameattributes(cert.issuer)

def _x509certdata(cert):
    pemencoded = cert.public_bytes(serialization.Encoding.PEM)
    return _strip_pem_delimiters(pemencoded)

def _nameattributes(named):
    attl = []
    for (label,oid) in [
        ('CN',NameOID.COMMON_NAME),
        ('L',NameOID.LOCALITY_NAME),
        ('O',NameOID.ORGANIZATION_NAME),
        ('C',NameOID.COUNTRY_NAME)]:
        for att in named.get_attributes_for_oid(oid):
            attl.append("{}={}".format(label,att.value))
    return ', '.join(attl)



def _strip_pem_delimiters(data):
    data = data.replace('-----BEGIN CERTIFICATE-----\n','')
    data = data.replace('-----END CERTIFICATE-----\n','')
    data = data.replace('\n\n','\n')
    data.strip()
    return data

def _add_pem_delimiters(data):
    return "-----BEGIN CERTIFICATE-----\n{}-----END CERTIFICATE-----\n".format(data)

def _ds(el):
    return '{{{}}}{}'.format(_NSMAP['ds'],el)

def _dsig11(el):
    return '{{{}}}{}'.format(_NSMAP['dsig11'],el)

_PEM_RE_CERTIFICATE_START_END = re.compile(
    b"-----BEGIN CERTIFICATE----\r?(.+?)\r?-----END CERTIFICATE-----\r?\n?", re.DOTALL)

def load_pem_x509_certificate_chain(data, handler=default_backend()):
    cert_data_list = [ match.group(0)
                       for match in _PEM_RE_CERTIFICATE_START_END.finditer(data)    ]
    return [ load_pem_x509_certificate(cert, handler)
             for cert in cert_data_list ]


