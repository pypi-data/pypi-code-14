

class QuotaCase():

    def run(self, API, sleep):
        API.conn.call('DescribeQuotas')
