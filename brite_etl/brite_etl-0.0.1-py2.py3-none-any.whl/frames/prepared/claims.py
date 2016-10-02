from brite_etl.abstracts import Frame


class Claims(Frame):

    _config = {
        'name': 'claims',
        'prepared': True
    }
