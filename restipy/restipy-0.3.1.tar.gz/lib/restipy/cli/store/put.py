from ..local_store import LocalStore

def do(args):
    local_store = LocalStore(args.save_path, args.save_filename)
    data = local_store.get_data()
    data[args.key] = args.value
    
    local_store.dump()