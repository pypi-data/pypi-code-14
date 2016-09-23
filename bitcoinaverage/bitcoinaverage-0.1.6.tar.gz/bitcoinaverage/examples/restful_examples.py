from bitcoinaverage.clients.restful_client import RestfulClient

if __name__ == '__main__':
    secret2 = input('Enter your secret key: ')
    public2 = input('Enter your public key: ')

    restful_client = RestfulClient(secret2, public2)
    print('Ticket:')
    print(restful_client.get_ticket())
    print('Exchanges data for LTCEUR')
    print(restful_client.all_exchange_data_for_symbol('LTCEUR'))
