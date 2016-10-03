from brite_etl.abstracts import Frame


class ClaimsChanges(Frame):

    _config = {
        'name': 'claims_changes',
        'prepared': False
    }
