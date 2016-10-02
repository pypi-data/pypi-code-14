from brite_etl.abstracts import Frame


class PolicyChangeLog(Frame):

    _config = {
        'name': 'policy_change_log',
        'prepared': False
    }
