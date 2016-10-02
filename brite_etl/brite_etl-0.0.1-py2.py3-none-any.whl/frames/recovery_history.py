from brite_etl.abstracts import Frame


class RecoveryHistory(Frame):

    _config = {
        'name': 'recovery_history',
        'prepared': False
    }
