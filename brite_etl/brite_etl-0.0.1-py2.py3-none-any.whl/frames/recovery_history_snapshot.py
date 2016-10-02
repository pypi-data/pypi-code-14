from brite_etl.abstracts import Frame


class RecoveryHistorySnapshot(Frame):

    _config = {
        'name': 'recovery_history_snapshot',
        'prepared': False
    }
