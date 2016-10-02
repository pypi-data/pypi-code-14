from brite_etl.abstracts import Frame


class Emails(Frame):

    _config = {
        'name': 'emails',
        'prepared': False
    }
