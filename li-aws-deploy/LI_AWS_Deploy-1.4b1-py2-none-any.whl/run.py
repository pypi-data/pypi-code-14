#!/usr/bin/env python
# coding: utf-8
"""Ferramenta Loja Integrada.

Usage:
    li config <app>
    li deploy <app>
    li debug <app>
    li test <app> (-j | -u)
    li telnet <app> (-p <port>)
    li bash <app>
    python -m tools

Options:
    -h  --help       Mostra esta tela
    -v  --version    Mostra a versao
    -p  --port       Porta para o telnet
    -j  --django     Roda o teste unitario do Django
    -u  --unit       Roda o teste unitario do Python
"""
from __future__ import print_function, unicode_literals, with_statement, nested_scopes
from docopt import docopt

VERSION = "1.4b1"


def main():
    arguments = docopt(__doc__, version=VERSION)
    print(arguments)


def start():
    print(
        "\n\n************************\n\n"
        "LI-Tools v{version}\n\n"
        "************************\n".format(version=VERSION)
    )
    retorno = main()
    if not retorno:
        print("Operação finalizada.\n")

if __name__ == "__main__":
    start()
