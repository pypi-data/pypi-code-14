from brite_etl.abstracts import Frame


class CreditReports(Frame):

    _config = {
        'name': 'credit_reports',
        'prepared': True
    }
