#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import logbook

from credits.stringify import stringify
from credits.address import CreditsAddressProvider

logger = logbook.Logger(__name__)


def test_CreditsAddressProvider_get_address(hash_provider):
    tests = [
        {
            "input": "2cd32af3ec59cac5e1b6acb2a6ed4116de68aa68ffa242d43229a1ca0a4c6c1a",
            "output": "1FG3LHD7kmQeZnCUXQJ756H2sGvAwiQCY"
        },
        {
            "input": "e4a3dad9a6ee130a2a5564e2db7542c80fb87f6bf44b16b123bd5c2d871ebad6",
            "output": "17BFRzguaynmGbH8yG9TduAiVEmiR4bQUs"
        },
        {
            "input": "2fb08f51d36f84fb04db02f6aa392398469215c28c8152a7ec3916d67edce57a",
            "output": "17qJUw7avjKQVYDAXMxf5CCP1yNTYyxnjE"
        },
    ]

    for t in tests:
        assert CreditsAddressProvider(t["input"]).get_address() == t["output"]


def test_stringify():
    tests = [
        {
            "input": "test",
            "output": "74657374",
        },
        {
            "input": 5,
            "output": "0x5",
        },
        {
            "input": "5",
            "output": "35",
        },
        {
            "input": [
                1,
                "test",
                "data"
            ],
            "output": "[0x1,74657374,64617461]",
        },
        {
            "input": {
            "test": "data",
            "list": [
                1,
                2,
                3,
                4,
                5
            ]
            },
            "output": "{6c697374:[0x1,0x2,0x3,0x4,0x5],74657374:64617461}",
        },
        {
            "input": {
                1: 2,
                3: 4,
                5: 6
            },
            "output": "{0x1:0x2,0x3:0x4,0x5:0x6}"
        },
        {
            "input": {
                "test": "data",
                "list": [
                  1,
                  2,
                  3,
                  4,
                  5
                ],
                "dict": {
                  "1": 2,
                  "3": 4,
                  "5": 6
                }
            },
            "output": "{64696374:{31:0x2,33:0x4,35:0x6},6c697374:[0x1,0x2,0x3,0x4,0x5],74657374:64617461}",
        }
    ]

    for t in tests:
        assert(stringify(t["input"]) == t["output"])
