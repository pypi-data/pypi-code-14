import scp
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


class SCPLibrary(object):
    """Robot Framework Secure Copy (SCP) test library.

    This library uses the current connection established via default
    SSHLibrary (robotframework-sshlibrary). Because of this, and unlike
    another SCPLibrary (robotframework-scplibrary), there are no keyword
    clashes and it can be used alongside SSHLibrary.

    Only works with the Python version of SSHLibrary.

    SSHLibrary uses paramiko, and this SCPLibrary uses the 'scp' wrapper.

    = Connection =

    Establishing and closing the connection is done via the SSHLibrary.

    = File transfer =

    Files can be downloaded from a remote machine using the `Download File`
    keyword. Reversely, files can be uploaded to a remote machine using the
    `Upload File` keyword.

    An existing connection must have been established via the SSHLibrary
    before calling any of these keywords.
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self.sshlibrary = BuiltIn().get_library_instance('SSHLibrary')

    def _get_transport(self):
        """Gets the transport connection from the current SSH connection."""
        logger.debug("Getting current transport from SSHLibrary")
        try:
            transport = self.sshlibrary.current.client.get_transport()
        except AttributeError:
            raise AssertionError("Only works with the Python SSHLibrary")
        else:
            if not transport:
                raise AssertionError("Connection not open")
            return transport

    def download_file(
            self, remote_source_path, local_dest_path, recursive=False):
        """Download a remote file using SCP over the current SSH connection.

        This is basically a wrapper around 'scp.SCPClient.get', as such
        multiple files (i.e. a list of files) can be passed in.

        The remote path is evaluated on the host and may contain wildcards or
        environmental variables (from the *remote* host).

        Recursive must be 'True' for directories.

        Examples:
        | Download File | /home/remote/foo.tar.gz | /tmp/foo.tar.gz |
        | Download File | /home/remote/*.tar.gz   | /tmp/           |
        | Download File | /home/remote/           | /tmp/bar/       | recursive=True |
        """
        copy_pipe = scp.SCPClient(self._get_transport())
        logger.debug("Transferring {} (remote) to {} (local)".format(
            remote_source_path, local_dest_path))
        try:
            copy_pipe.get(
                remote_source_path,
                local_dest_path,
                recursive=bool(recursive))
        except scp.SCPException as e:
            raise RuntimeError(e)
        finally:
            if copy_pipe:
                copy_pipe.close()

    def upload_file(self, local_source_files, remote_dest_path, recursive=False):
        """Upload a local file using SCP over the current SSH connection.

        This is basically a wrapper around 'scp.SCPClient.put', as such
        multiple files (i.e. a list of files) can be passed in.

        Recursive must be 'True' for directories.

        Examples:
        | Upload File | /home/local/foo.tar.gz | /tmp/foo.tar.gz |
        | Upload File | /home/local/           | /tmp/           | recursive=True |
        """
        copy_pipe = scp.SCPClient(self._get_transport())
        logger.debug("Transferring {} (local) to {} (remote)".format(
            local_source_files, remote_dest_path))
        try:
            copy_pipe.put(
                local_source_files,
                remote_dest_path,
                recursive=bool(recursive))
        except scp.SCPException as e:
            raise RuntimeError(e)
        finally:
            if copy_pipe:
                copy_pipe.close()
