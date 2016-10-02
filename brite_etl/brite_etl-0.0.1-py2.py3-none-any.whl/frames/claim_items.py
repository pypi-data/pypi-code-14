from brite_etl.abstracts import Frame


class ClaimItems(Frame):

    _config = {
        'name': 'claim_items',
        'prepared': False
    }
