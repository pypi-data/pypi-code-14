from plato_cat.cases import get_resource
from plato_cat.cases import post_resource


class KeyPairCase():

    def run(self, API, sleep):
        keypairs = get_resource(API, 'DescribeKeyPairs', {
            'status': ['active']
        }, 'keyPairSet')

        API.conn.call('CreateKeyPair', {
            'name': 'key-pair-name'
        })

        new_keypairs = get_resource(API, 'DescribeKeyPairs', {
            'status': ['active']
        }, 'keyPairSet')

        if len(new_keypairs) - len(keypairs) != 1:
            raise Exception("after create 2 key_pairs,"
                            " DescribeKeyPairs did not increase by 2!")


class CleanKeyPairs():

    def run(self, API, sleep):
        key_pairs = get_resource(API, 'DescribeKeyPairs', {
            'status': ['active']
        }, 'keyPairSet')

        # delete key_pairs
        key_pair_ids = [kp['keyPairId'] for kp in key_pairs]
        post_resource(API, 'DeleteKeyPairs', key_pair_ids, 'keyPairIds')
