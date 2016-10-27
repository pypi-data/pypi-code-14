import re
pattern = re.compile('([\w]+)=(.+)')

def parse_data(data_entries):
    new_dict = {}
    for entry in data_entries:
        key, value = parse_entry(entry)
        if key and value:
            new_dict[key] = value
    return new_dict

def parse_entry(entry):
    matches = pattern.match(entry)
    if matches:
        return matches.group(1), matches.group(2)
    else:
        raise Exception('Invalid data format')