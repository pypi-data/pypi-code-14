from brite_etl.abstracts import Frame


class InactiveClaims(Frame):

    _config = {
        'name': 'inactive_claims',
        'prepared': False
    }
