import subprocess


class Terminal(object):

    def command(self, command):
        proc = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE)
        output = proc.stdout.readlines()
        output = map(lambda s: s.strip(), output)
        proc.kill()
        return list(output)
