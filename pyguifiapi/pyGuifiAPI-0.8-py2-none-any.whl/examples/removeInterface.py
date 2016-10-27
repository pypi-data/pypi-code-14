#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from guifiConfig import USERNAME, PASSWORD
from api import GuifiAPI, GuifiApiError

g = GuifiAPI(USERNAME, PASSWORD, secure=True)
g.auth()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Remove an existing device')
        print('Usage: {} <interface_id>'.format(sys.argv[0]))
        sys.exit(1)

    """
    L'API només suporta gestionar interfícies de ràdio sense fils.
    No es poden esborrar interfícies del tipus wLan/Lan, així com tampoc hi pot haver cap ràdio sense interfícies. Les úniques interfícies que es poden treure són les de tipus wLan, les que afegeixen rangs d'IP per clients.
    Queda per implementar el suport de les connexions per cable.
    """

    try:
        g.removeInterface(sys.argv[1])
    except GuifiApiError as e:
        print(e.reason)
