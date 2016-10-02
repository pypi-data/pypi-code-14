from brite_etl.abstracts import Frame


class Mortgagees(Frame):

    _config = {
        'name': 'mortgagees',
        'prepared': False
    }
