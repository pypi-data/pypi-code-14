"""This Should all be done on import, this verifys everything is ok"""
from os import listdir, mkdir, path
from shutil import copy
from sys import argv
import yaml
from .values import PATH, ALT_PATH, DATA_DIR, CONFIG_FILE

# Verify All Files Exist
if not path.exists(PATH):
    print('[-] Creating DIR "{}"', PATH)
    copy(path.join(ALT_PATH, 'config'), PATH)
    input('[!] Edit the config then press enter')
print('[~] Verifing all files are present.')
for p in listdir(ALT_PATH):
    o1 = path.join(ALT_PATH, p)
    o2 = path.join(PATH, p)
    if not path.exists(o2):
        if path.isdir(o1):
            mkdir(o2)
        else:
            with open(o2, 'wb') as f:
                with open(o1, 'rb') as f2:
                    [f.write(x) for x in f2]

# Verify All Config Keys Exist
print('[~] Verifing Config (Will create values that are missing)')
origional = new = {}
with open(CONFIG_FILE) as x:
    origional = yaml.load(x)
with open(path.join(ALT_PATH, 'config', 'config.yml')) as x:
    new = yaml.load(x)
for k,v in new.items():
    origional.setdefault(k,v)
    # Only Allowing 2 nested dicts, any more is 2many
    if isinstance(v, dict):
        for k2, v2 in v.items():
            origional[k].setdefault(k2,v2)
            if isinstance(v2, dict):
                for k3, v3 in v.items():
                    origional[k][k2].setdefault(k3, v3)

# Create Data Dir
if not path.exists(DATA_DIR):
    print('[!] Creating Data DIR')
    mkdir(DATA_DIR)
print('[+] Complete')
