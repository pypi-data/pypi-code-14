# -*- coding:utf-8 -*-
import json
from .redis import Redis, parse_args


def start_client():
    r = Redis()
    args = parse_args()
    keys = [args.key] if args.key else []
    if args.json:
        mapping = [json.loads(args.args[0])]
        result = getattr(r, args.cmd)(*(keys + mapping))
    else:
        result = getattr(r, args.cmd)(*(keys + args.args))
    if result:
        print result