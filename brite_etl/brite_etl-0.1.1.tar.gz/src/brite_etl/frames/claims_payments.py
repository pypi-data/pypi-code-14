from brite_etl.abstracts import Frame


class ClaimsPayments(Frame):

    _config = {
        'name': 'claims_payments',
        'prepared': False
    }
