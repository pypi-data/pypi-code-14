from __future__ import absolute_import

import argparse
import json
import requests
import sys

from time import sleep

from .client import Client

# TODO add logging once basescript is pip installable.

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", required=True,
        help="username",
    )
    parser.add_argument("-s", "--secret", required=True,
        help="secret key",
    )
    parser.add_argument("-n", "--name", required=True,
        help="name to query",
    )

    parser.add_argument("-H", "--host", default="http://www.deepcompute.com",
        help="host server, default is %(default)s",
    )
    parser.add_argument("--wait", default=False, action="store_true",
        help="block until the server gets data",
    )

    return parser.parse_args()

def main():
    args = get_args()
    client = Client(args.host, args.user, args.secret)

    data_available = False
    num_tries = 0
    max_tries = 20
    while not data_available:
        num_tries += 1
        resp = client.get_person(args.name)
        data_available = resp.get('data_available', False)
        if data_available:
            sys.stdout.write("%s\n" % json.dumps(resp))
            sys.stdout.flush()
            return

        if not args.wait:
            data = { "data_available": False, "msg": "Lookup in progress. Please try again after some time" }
            sys.stdout.write("%s\n" % json.dumps(resp))
            sys.stdout.flush()
            return

        if num_tries >= max_tries:
            data = { "data_available": False, "msg": "Lookup took too long. Please try again after some time" }
            sys.stdout.write("%s\n" % json.dumps(resp))
            sys.stdout.flush()
            return

        # wait and try again.
        sleep(3)

if __name__ == '__main__':
    main()
