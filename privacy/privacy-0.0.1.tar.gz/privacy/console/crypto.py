#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import logging

from privacy.core import Privacy
from privacy.core import InvalidRecipient
from privacy.core import InvalidKeyError

from privacy.console.ui import get_passphrase

from privacy.console.base import get_sub_parser_argv
from privacy.console.util import is_file_and_exists

logger = logging.getLogger('privacy')


def execute_command_encrypt():
    from privacy.console.parsers.encrypt import parser

    args = parser.parse_args(get_sub_parser_argv())

    gee = Privacy()
    if is_file_and_exists(args.plaintext):
        plaintext = io.open(args.plaintext, 'rb').read()

    else:
        plaintext = args.plaintext

    try:
        print gee.encrypt(args.recipient, plaintext, sign_from=args.sign_from)
    except InvalidRecipient as e:
        logger.error("failed to encrypt: {0}".format(e))
        raise SystemExit(1)


def execute_command_decrypt():
    from privacy.console.parsers.decrypt import parser

    args = parser.parse_args(get_sub_parser_argv())
    gee = Privacy()
    if args.secret:
        passphrase = args.secret
    elif args.no_secret:
        passphrase = None
    else:
        passphrase = get_passphrase()

    if is_file_and_exists(args.ciphertext):
        ciphertext = io.open(args.ciphertext, 'rb').read()

    else:
        ciphertext = args.ciphertext

    try:
        plaintext = gee.decrypt(ciphertext, passphrase)

    except InvalidKeyError as e:
        logger.error("failed to decrypt: {0}".format(e))
        raise SystemExit(1)

    if plaintext:
        print plaintext


def execute_command_verify():
    from privacy.console.parsers.verify import parser

    args = parser.parse_args(get_sub_parser_argv())
    gee = Privacy()

    if is_file_and_exists(args.signed_data):
        signed_data = io.open(args.signed_data, 'rb').read()

    else:
        signed_data = args.signed_data

    result = gee.verify(signed_data)
    if not result:
        print "Failed to verify"
        raise SystemExit(1)

    status, trust_level = result
    if 'signature valid' not in status.strip():
        print status, trust_level
        raise SystemExit(1)

    print ": ".join([status, trust_level])


def execute_command_sign():
    from privacy.console.parsers.sign import parser

    args = parser.parse_args(get_sub_parser_argv())
    if args.secret:
        passphrase = args.secret
    elif args.no_secret:
        passphrase = None
    else:
        passphrase = get_passphrase()

    gee = Privacy()

    if is_file_and_exists(args.data):
        data = io.open(args.data, 'rb').read()

    else:
        data = args.data

    signed = gee.sign(args.recipient, data, passphrase)

    if signed:
        print signed
