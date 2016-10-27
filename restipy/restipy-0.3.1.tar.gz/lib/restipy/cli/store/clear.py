from ..local_store import LocalStore

def do(args):
    local_store = LocalStore(args.save_path, args.save_filename)
    local_store.set_data({})
    local_store.dump()