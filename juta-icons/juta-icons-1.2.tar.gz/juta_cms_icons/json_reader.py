import json


def read_icon_in_json():
    """
    This function serves to render and return the selected choices
    :return CHOICES:
    """
    with open('/home/matthew/personal-dev/my custom fonts/selection.json') as data_file:
        data = json.load(data_file)
    CHOICES = [('', '----------')]

    for items in data['icons']:
        # pprint(items["properties"]['name'])
        CHOICES.append((
            items["properties"]['code'],
            items["properties"]['name']
        ))
    return CHOICES
