from brite_etl.abstracts import Frame


class PremiumRecords(Frame):

    _config = {
        'name': 'premium_records',
        'prepared': True
    }
