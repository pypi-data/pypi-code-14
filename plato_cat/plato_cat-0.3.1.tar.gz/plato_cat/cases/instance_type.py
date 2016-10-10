

class InstanceTypeCase():

    def run(self, API, sleep):
        API.conn.call('DescribeInstanceTypes')
