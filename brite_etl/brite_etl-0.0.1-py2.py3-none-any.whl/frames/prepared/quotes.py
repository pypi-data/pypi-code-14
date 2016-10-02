from brite_etl.abstracts import Frame


class Quotes(Frame):

    _config = {
        'name': 'quotes',
        'prepared': True
    }
