import util
from JuspayException import InvalidArguementException

class Wallets:

    def __init__(self):
        return 

    class Wallet:

        def __init__(self, kwargs):
            self.id = util.get_arg(kwargs, 'id')
            self.object = util.get_arg(kwargs, 'object')
            self.wallet = util.get_arg(kwargs, 'wallet')
            self.token = util.get_arg(kwargs, 'token')
            self.current_balance = util.get_arg(kwargs, 'current_balance')
            self.last_refreshed = util.get_arg(kwargs, 'last_refreshed')

    @staticmethod
    def create(**kwargs):
        raise NotImplementedError()

    @staticmethod
    def list(**kwargs):
        customer_id= util.get_arg(kwargs,'customer_id')
        order_id = util.get_arg(kwargs,'order_id')

        if customer_id is None and order_id is None:
            raise InvalidArguementException('`customer_id` or `order_id` is a required argument for Wallets.list()\n')

        method = 'GET'
        if customer_id is not None:
            url = '/customers/%s/wallets' % (customer_id)
        else:
            url = '/orders/%s/wallets' % (order_id)

        response = util.request(method, url, {}).json()
        response = util.get_arg(response,'list')
        wallets = []
        if response is not None:
            for wallet in response:
                wallet = Wallets.Wallet(wallet)
                wallets.append(wallet) 
        return wallets

    @staticmethod
    def refreshBalance(**kwargs):
        customer_id = util.get_arg(kwargs,'customer_id')
        if customer_id is None:
            raise InvalidArguementException('`customer_id` is a required argument for Wallets.refreshBalance()\n')

        method = 'GET'
        url = '/customers/%s/wallets/refresh-balances' % (customer_id)

        response = util.request(method, url, {}).json()
        response = util.get_arg(response,'list')
        wallets = []
        if response is not None:
            for wallet in response:
                wallet = Wallets.Wallet(wallet)
                wallets.append(wallet) 
        return wallets        

    @staticmethod
    def delete(**kwargs):
	    raise NotImplementedError()
