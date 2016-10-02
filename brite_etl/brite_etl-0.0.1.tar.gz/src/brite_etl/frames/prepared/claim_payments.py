from brite_etl.abstracts import Frame


class ClaimPayments(Frame):

    _config = {
        'name': 'claim_payments',
        'prepared': True
    }
