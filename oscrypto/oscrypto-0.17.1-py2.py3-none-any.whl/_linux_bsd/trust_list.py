# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

import os

from asn1crypto.pem import unarmor
from asn1crypto.x509 import TrustedCertificate

from .._errors import pretty_message


__all__ = [
    'extract_from_system',
    'system_path',
]


def system_path():
    """
    Tries to find a CA certs bundle in common locations

    :raises:
        OSError - when no valid CA certs bundle was found on the filesystem

    :return:
        The full filesystem path to a CA certs bundle file
    """

    ca_path = None

    # Common CA cert paths
    paths = [
        '/usr/lib/ssl/certs/ca-certificates.crt',
        '/etc/ssl/certs/ca-certificates.crt',
        '/etc/ssl/certs/ca-bundle.crt',
        '/etc/pki/tls/certs/ca-bundle.crt',
        '/etc/ssl/ca-bundle.pem',
        '/usr/local/share/certs/ca-root-nss.crt',
        '/etc/ssl/cert.pem'
    ]

    # First try SSL_CERT_FILE
    if 'SSL_CERT_FILE' in os.environ:
        paths.insert(0, os.environ['SSL_CERT_FILE'])

    for path in paths:
        if os.path.exists(path) and os.path.getsize(path) > 0:
            ca_path = path
            break

    if not ca_path:
        raise OSError(pretty_message(
            '''
            Unable to find a CA certs bundle in common locations - try
            setting the SSL_CERT_FILE environmental variable
            '''
        ))

    return ca_path


def extract_from_system():
    """
    Extracts trusted CA certs from the system CA cert bundle

    :return:
        A list of 3-element tuples:
         - 0: a byte string of a DER-encoded certificate
         - 1: a set of unicode strings that are OIDs of purposes to trust the
              certificate for
         - 2: a set of unicode strings that are OIDs of purposes to reject the
              certificate for
    """

    all_purposes = '2.5.29.37.0'
    ca_path = system_path()

    output = []
    with open(ca_path, 'rb') as f:
        for armor_type, _, cert_bytes in unarmor(f.read(), multiple=True):
            # Without more info, a certificate is trusted for all purposes
            if armor_type == 'CERTIFICATE':
                output.append((cert_bytes, set(), set()))

            # The OpenSSL TRUSTED CERTIFICATE construct adds OIDs for trusted
            # and rejected purposes, so we extract that info.
            elif armor_type == 'TRUSTED CERTIFICATE':
                cert, aux = TrustedCertificate.load(cert_bytes)
                reject_all = False
                trust_oids = set()
                reject_oids = set()
                for purpose in aux['trust']:
                    if purpose.dotted == all_purposes:
                        trust_oids = set([purpose.dotted])
                        break
                    trust_oids.add(purpose.dotted)
                for purpose in aux['reject']:
                    if purpose.dotted == all_purposes:
                        reject_all = True
                        break
                    reject_oids.add(purpose.dotted)
                if reject_all:
                    continue
                output.append((cert.dump(), trust_oids, reject_oids))

    return output
