# -*- coding: utf-8 -*-
import argparse
import getpass
import os
import sys

import efesto
from efesto.Models import Users


def create_user(name, password):
    user = Users(name=name, password=password, email=email, rank=rank, enabled=True)
    user.save()

def main():
    argparse
