from brite_etl.abstracts import Frame


class PrimaryPolicyholders(Frame):

    _config = {
        'name': 'primary_policyholders',
        'prepared': True
    }
