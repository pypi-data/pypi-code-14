import argparse
import re

from lambpack import to_dir, to_zip

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("dest")
    parser.add_argument("handler")
    parser.add_argument("-z/--zip", dest="zip", action="store_true", default=True)
    parser.add_argument("-d/--no-zip", dest="zip", action="store_false")
    parser.add_argument("--env", type=env_string, action="append")
    args = parser.parse_args()

    kwargs = {
        "path": args.path,
        "dest": args.dest,
        "handler": args.handler,
        "env": dict(args.env or {})
    }
    if args.zip:
        to_zip(**kwargs)
    else:
        to_dir(**kwargs)

def env_string(string):
    match = re.search(r"^(.*?)=(.*)$", string)
    if not match:
        raise ValueError("Expected key=value")
    return match.groups()

if __name__ == "__main__":
    main()
