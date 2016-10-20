import requests

from coinbase.wallet.client import Client
from decimal import Decimal

# ------------------------------------------------------------------------------

# tilapia.py

# Make API calls and send micropayments via Coinbase API

# ------------------------------------------------------------------------------


class Tilapia(object):

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        # instantiate Coinbase client object
        self.client = Client(api_key, api_secret)
        # get primary account info from the client object itself
        self.primary_account_id = self.client.get_primary_account()['id']

    def send_payment(self, sender_id, receiver_email, amount, currency):
        """
        Every transaction will must be verified against Coinbase
        :param sender_id: Coinbase ID of sender account
        :param receiver_email: Coinbase email of receiver account (if not email, then not off-chain)
        :param amount: how much to send (must be str or float type)
        :return: transaction object to verify
        """
        # send micropayment via Coinbase
        transaction = self.client.send_money(sender_id, to=receiver_email, amount=amount, currency=currency)
        verification = self.client.get_transaction(sender_id, transaction['id'])
        if transaction != verification:
            raise ValueError('Transaction cannot be verified by Coinbase.')
        # return transaction object
        return transaction

    def format_url(self, url):
        # if URL does not contain http or https in the beginning, Python requests will throw a MissingSchema error

        if 'https://' not in url:
            raise ValueError('Please prepend https:// to the beginning of the URL.')

        # pre-format URL and add / if no slash at the end of given URL
        if url[len(url)-1] != '/':
            url += '/'
        return url

    def get(self, url):
        """
        Perform a 'GET request' for an API
        """
        # format the URL first
        formatted_url = self.format_url(url)

        try:
            response = requests.get(formatted_url).json()
            creator_coinbase_email = response['creator_coinbase_email']
            api_name = response['name']
            # get the cost of each app call, then send appropriate amount
            cost_unicode = response['bitcoin_price']
            cost_str = '{:f}'.format(Decimal(cost_unicode))
        except:
            return Exception('Connection error: connection to server failed. Please check the URL again.')
        try:
            # send payment and get transaction object from Coinbase API
            transaction_obj = self.send_payment(self.primary_account_id, creator_coinbase_email, cost_str, 'BTC')
            print cost_str + ' BTC paid for ' + api_name

            confirmation_dict = {'coinbase_sender_id': self.primary_account_id,
                                 'transaction_id': transaction_obj['id']}
        except:
            return Exception('Confirmation error: payment confirmation failed.')

        try:
            # confirm with server
            response = requests.post(formatted_url, confirmation_dict).json()
        except:
            return Exception('Confirmation error: API request failed.')

        return response
