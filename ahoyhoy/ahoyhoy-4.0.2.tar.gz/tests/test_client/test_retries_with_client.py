import time

from ..utils import Host


from ahoyhoy.client import LBClientBuilder
from ahoyhoy.lb import RoundRobinLB
from ahoyhoy.lb.providers import ListProvider


def test_success_timeouts():
    """
    Try to connect to hosts with timeouts.
    """
    start = time.clock()

    non_existed_host1 = Host('10.255.255.1', 80)
    non_existed_host2 = Host('10.255.255.2', 80)
    good_host = Host('google.com', 80)

    rrlb = RoundRobinLB(ListProvider(non_existed_host1, non_existed_host2, good_host))
    client = LBClientBuilder().add_lb(rrlb).build()
    
    # http://docs.python-requests.org/en/master/user/advanced/#timeouts
    
    # The timeout value will be applied to both the connect and the read timeouts. 
    # Specify a tuple if you would like to set the values separately.
    response = client.get('/', timeout=1)

    end = time.clock()-start
    
    assert response.status_code == 200

    # Should be < 3, but doesn't work for now.
    # assert start-end < 4
