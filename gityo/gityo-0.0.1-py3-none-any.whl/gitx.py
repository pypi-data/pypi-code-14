import subprocess
import os


class GitError(Exception):
    def __init__(self, error_message):
        self.error_message = error_message


class Git:
    def __init__(self, git_path=None, cwd=None):
        self.git_path = git_path or 'git'
        self.cwd = cwd
        self.quiet = True

    def execute(self, *git_commands, quiet=None, cwd=None):
        cmd = '%s %s' % (self.git_path, ' '.join(git_commands))
        if quiet is False or (quiet is None and not self.quiet):
            print('%s>%s' % (cwd or self.cwd or os.getcwd(), cmd))

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd or self.cwd)
        stdout = []
        while True:
            line = p.stdout.readline()
            text = line.decode('utf8')
            if line == b'' and p.poll() is not None:
                break
            stdout.append(text)
            if quiet is False or (quiet is None and not self.quiet):
                print(text)

        output_str = ''.join(stdout)
        if p.returncode != 0:
            raise GitError(output_str)
        return output_str
