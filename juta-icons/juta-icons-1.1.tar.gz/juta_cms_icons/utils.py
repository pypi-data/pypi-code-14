import json
import os
PATH = os.path.join(os.path.dirname(__file__), 'json_data/selection.json')


def get_icon_choices():
    with open(PATH) as icon_list:
        data = json.load(icon_list)

    CHOICES = [('', '----------')]

    for items in data['icons']:

        CHOICES.append((
            items["properties"]['name'],
            items["properties"]['name']
        ))

    return CHOICES