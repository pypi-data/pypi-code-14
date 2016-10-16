"""Compare environment variables in the terminal.
"""
import json
import os
from pathlib import Path
import sys
import time

__version__ = '0.1'

if sys.platform != 'win32':
    TERM_BOLD = '\x1b[1m'
    TERM_RESET = '\x1b[0m'
else:
    TERM_BOLD = TERM_RESET = ''

def data_dir(make=False):
    if sys.platform == 'win32':
        d = Path(os.environ['APPDATA'])
    elif sys.platform == 'darwin':
        d = Path.home() / 'Library'
    elif 'XDG_DATA_HOME' in os.environ:
        d = Path('XDG_DATA_HOME')
    else:
        d = Path.home() / '.local/cache'

    d = d / 'envzigzag'
    if make:
        d.mkdir(parents=True, exist_ok=True)
    return d


def zig_main(argv=None):
    """Record the current environment to a JSON file"""
    data = {
        'timestamp': time.time(),
        'environ': dict(os.environ),
    }
    # _ records the last command; usually not interesting
    data['environ'].pop('_', None)
    with (data_dir(make=True) / 'zig.json').open('w') as f:
        json.dump(data, f, indent=2)

def dict_compare(a, b):
    """Compare two dictionaries.

    Returns three dictionaries:
    - Entries in a but not b
    - Entries in b but not a
    - Entries in both but different - values are (aval, bval)
    """
    aonly = {k: a[k] for k in (a.keys() - b.keys())}
    bonly = {k: b[k] for k in (b.keys() - a.keys())}
    changed = {k: (a[k], b[k]) for k in (a.keys() & b.keys()) if a[k] != b[k]}
    return aonly, bonly, changed

def print_one_side(header, vals):
    if not vals:
        return False

    print(header)
    for k, v in sorted(vals.items()):
        print('  ', TERM_BOLD, k, '=', TERM_RESET, v, sep='')
    print()
    return True

def print_changes(changed):
    if not changed:
        return False

    print('Changed:')
    for k, (vzig, vzag) in sorted(changed.items()):
        print('  ', TERM_BOLD, k, '=', TERM_RESET, sep='')
        print('  ├zig: ', vzig, sep='')
        print('  └zag: ', vzag, sep='')
    return True

def print_difference(zig_env, zag_env):
    zig_only, zag_only, changed = dict_compare(zig_env, zag_env)

    output = print_one_side('Removed [in zig, not zag]:', zig_only) \
           + print_one_side('Added   [in zag, not zig]:', zag_only) \
           + print_changes(changed)

    if not output:
        print('Snap! No changes between zig and zag.')

def zag_main(argv=None):
    try:
        with (data_dir() / 'zig.json').open() as f:
            zig_data = json.load(f)
    except FileNotFoundError:
        sys.exit('Run envzig first to make a snapshot, then envzag to compare.')

    env_now = os.environ.copy()
    # _ records the last command; usually not interesting
    env_now.pop('_', None)

    print_difference(zig_data['environ'], env_now)
