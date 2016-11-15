__author__ = "Kiran Vemuri"
__email__ = "kkvemuri@uh.edu"
__status__ = "Development"
__maintainer__ = "Kiran Vemuri"

from StringIO import StringIO
import paramiko

# Work around for py.test paramiko hanging issue. Refer https://github.com/paramiko/paramiko/issues/735
from paramiko import py3compat
py3compat.u("dirty hack")


class Connection:
    """
    A wrapper for paramiko.SSHClient
    """
    # TIMEOUT = 4

    def __init__(self, host, port, username, password, key=None, passphrase=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        # Ssh client
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key is not None:
            key = paramiko.RSAKey.from_private_key(StringIO(key), password=passphrase)
        # self.client.connect(host, port, username=username, password=password, pkey=key, timeout=self.TIMEOUT)
        self.client.connect(self.host, self.port, username=username, password=password, pkey=key)

        # Sftp client
        # Open a transport
        self.transport = paramiko.Transport(self.host, self.port)
        # Auth
        self.transport.connect(username=self.username, password=self.password)
        # Go!
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def close(self):
        """
        Method to close SSH and SFTP sessions opened during constructor call
        """
        if self.client is not None:
            self.client.close()
            self.client = None
        if self.sftp is not None and self.transport is not None:
            self.sftp.close()
            self.transport.close()
            self.sftp = None
            self.transport = None

    def execute(self, command, sudo=False):
        """
        Method to execute a remote command
        :param command: <str> Command to be executed on the remote machine
        :param sudo: <bool> True to run the command as sudo and (default)False to run the command without sudo
        :return Return value, stderr and stdout of the executed command as a dictionary
        """
        feed_password = False
        if sudo and self.username != "root":
            command = "sudo -S -p '' %s" % command
            feed_password = self.password is not None and len(self.password) > 0
        stdin, stdout, stderr = self.client.exec_command(command)
        if feed_password:
            stdin.write(self.password + "\n")
            stdin.flush()
        return {'out': stdout.readlines(),
                'err': stderr.readlines(),
                'retval': stdout.channel.recv_exit_status()}

    def upload(self, local_path, remote_path):
        """
        Method to support file upload(sftp put) using paramiko
        :param local_path: <str> local path of the file
        :param remote_path: <str> remote path of the file
        """
        # Upload using sftp.put
        self.sftp.put(local_path, remote_path)

    def download(self, remote_path, local_path):
        """
        Method to support file download(sftp get) using paramiko
        :param remote_path: <str> remote path of the file
        :param local_path: <str> local path of the file
        """
        # Download using sftp.get
        self.sftp.get(remote_path, local_path)
