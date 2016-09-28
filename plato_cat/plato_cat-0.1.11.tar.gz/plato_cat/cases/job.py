

class JobCase():

    def run(self, API, sleep):
        API.conn.call('DescribeJobs')
