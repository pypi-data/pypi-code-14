from django.conf import settings


# Hard coded for now to avoid external requirement. Will change
# if the list becomes unmanageable or once we're all moved over to Py3 :)

# https://confluence.atlassian.com/bitbucket/what-are-the-bitbucket-cloud-ip-addresses-i-should-use-to-configure-my-corporate-firewall-343343385.html

BITBUCKET_IP_ADDRESSES = [
    '131.103.20.165',  # Remove after 1/10/2016
    '131.103.20.166',  # Remove after 1/10/2016

    '104.192.143.193', # 104.192.143.192/28
    '104.192.143.194',
    '104.192.143.195',
    '104.192.143.196',
    '104.192.143.197',
    '104.192.143.198',
    '104.192.143.199',
    '104.192.143.200',
    '104.192.143.201',
    '104.192.143.202',
    '104.192.143.203',
    '104.192.143.204',
    '104.192.143.205',
    '104.192.143.206',

    '104.192.143.209', # 104.192.143.208/28
    '104.192.143.210',
    '104.192.143.211',
    '104.192.143.212',
    '104.192.143.213',
    '104.192.143.214',
    '104.192.143.215',
    '104.192.143.216',
    '104.192.143.217',
    '104.192.143.218',
    '104.192.143.219',
    '104.192.143.220',
    '104.192.143.221',
    '104.192.143.222',
]


USE_CELERY = getattr(settings, 'TRELLO_BROKER_USE_CELERY', False)

RESTRICT_IPS = getattr(settings, 'TRELLO_BROKER_RESTRICT_IPS', False)

# https://confluence.atlassian.com/display/BITBUCKET/What+are+the+Bitbucket+IP+addresses+I+should+use+to+configure+my+corporate+firewall
# Only needed if TRELLO_BROKER_RESTRICT_IPS is True
BITBUCKET_IPS = getattr(
    settings,
    'TRELLO_BROKER_BITBUCKET_IPS',
    BITBUCKET_IP_ADDRESSES,
)

RULE_CLASSES = getattr(settings,
    'TRELLO_BROKER_RULE_CLASSES',
    ['trello_broker.rules.DefaultRuleProc'],
)
