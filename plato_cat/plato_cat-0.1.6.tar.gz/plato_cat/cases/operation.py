

class OperationCase():

    def run(self, API, sleep):
        API.conn.call('DescribeOperations')
