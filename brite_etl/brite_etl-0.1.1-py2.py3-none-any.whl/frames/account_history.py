from brite_etl.abstracts import Frame


class AccountHistory(Frame):

    _config = {
        'name': 'account_history',
        'prepared': False
    }
