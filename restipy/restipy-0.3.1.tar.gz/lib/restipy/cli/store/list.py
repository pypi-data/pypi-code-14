import json

from ..local_store import LocalStore

def do(args):
    local_store = LocalStore(args.save_path, args.save_filename)
    print json.dumps(local_store.get_data())