from brite_etl.abstracts import Frame


class CustomData(Frame):

    _config = {
        'name': 'custom_data',
        'prepared': False
    }
