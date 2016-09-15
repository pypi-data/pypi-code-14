class SSHOutput(object):

    def __init__(self, host, channel, stdout, stderr, stdin, exception=None):
        self.host = host
        self.channel = channel
        self.stdout = stdout
        self.stderr = stderr
        self.stdin = stdin
        self.exception = exception
