from bbug_dynamics import Dynamics, Settings

def test_token():
    settings = Settings('localhost__37000').settings
    t = Dynamics(settings).token()
    assert('accessToken' in t)

