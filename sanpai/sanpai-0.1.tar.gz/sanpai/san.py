#!/usr/bin/env python


def inspect(pem_file):

    try:
        from cryptography import x509
        from cryptography.hazmat.backends import default_backend

        result = _get_from_crypto(pem_file=pem_file)

    except:
        result = _get_from_openssl(pem_file=pem_file)

    return result


def _get_from_crypto(pem_file):

    with open(pem_file, 'r') as f:
        pem_file = f.read()

    cert = x509.load_pem_x509_certificate(pem_file, default_backend())

    san_domains = []

    for name in cert.extensions.get_extension_for_oid(x509.ExtensionOID.SUBJECT_ALTERNATIVE_NAME).value.get_values_for_type(x509.DNSName):
        san_domains.append(name)

    return san_domains


def _get_from_openssl(pem_file):

    import subprocess

    cert_body = subprocess.check_output(['openssl', 'x509', '-text', '-noout', '-in', pem_file])
    san_body = ''.join(cert_body.split('DNS:')[1:]).split('X509')[0]

    san_domains = []

    for d in san_body.split(','):
        san_domains.append(d.strip())

    return san_domains
