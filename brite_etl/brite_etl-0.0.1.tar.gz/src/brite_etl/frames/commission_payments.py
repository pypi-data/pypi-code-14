from brite_etl.abstracts import Frame


class CommissionPayments(Frame):

    _config = {
        'name': 'commission_payments',
        'prepared': False
    }
