from brite_etl.abstracts import Frame


class ItemTransactions(Frame):

    _config = {
        'name': 'item_transactions',
        'prepared': True
    }
