import subprocess


class Process(object):
    def __init__(self, pipe):
        """

        :type pipe: subprocess.Popen
        """
        self.pipe = pipe

    def readLine(self):
        # type: () -> str
        line = self.pipe.stdout.readline()
        if line == '':
            return None
        return line

    def kill(self):
        self.pipe.kill()



class ProcessResult(object):
    stdout = []
    stderr = []
    code = 1

    def __init__(self):
        self.stdout = []
        self.stderr = []
        self.code = 0

    def __str__(self):
        return "\n".join(self.stdout)


def execute(process, wait=True):
    """

    :type process: list[str] | str
    :type wait: bool
    :param wait: if true - returns ProcessResult with stout/stderror values, otherwise returns Process
    :return:
    :rtype: ProcessResult|Process
    """

    pipe = subprocess.Popen(
        process, stdout=subprocess.PIPE,
        stdin=subprocess.PIPE)
    if wait:
        res = ProcessResult()
        for line in pipe.stdout:
            res.stdout.append(
                line.strip()
            )
        return res
    else:
        return Process(pipe)
