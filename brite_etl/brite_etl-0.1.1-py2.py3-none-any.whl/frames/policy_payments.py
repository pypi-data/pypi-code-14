from brite_etl.abstracts import Frame


class PolicyPayments(Frame):

    _config = {
        'name': 'policy_payments',
        'prepared': False
    }
