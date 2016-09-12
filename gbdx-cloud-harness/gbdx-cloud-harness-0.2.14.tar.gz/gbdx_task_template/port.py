import os
import sys

if sys.version_info[0] == 3:
    from urllib.parse import urlparse
else:
    # Python 2 import
    from urlparse import urlparse


class LocalPortValidationError(Exception):
    pass


class RemotePortValidationError(Exception):
    pass


class InvalidPortType(Exception):
    pass


class Port(object):
    """
    A Class to configure Port instances for the custom application
    """

    def __init__(self, port_type, direction, value):

        self.__direction = direction

        if value:
            self.__task_wf_json = {
                'value': value
            }
        else:
            self.__task_wf_json = {}

        # Load Task JSON attrs
        self._name = None

        if port_type not in ['string', 'directory']:
            raise InvalidPortType('Port has an invalid port type.')

        self._port_type = port_type

        if self._port_type == 'directory':
            # For directory ports, there can be any combination of a local file system
            # location and an S3 location. ie: fs_loc = '/local/path/' && s3_loc = None, etc.
            # EXCEPT: they can't both be None

            # TODO value is not None doesn't make sense, validate s3 url? Ignore and raise error later?
            if direction == 'Output' and value is not None:
                self.stageToS3 = True

            remote_work_path = os.environ.get('REMOTE_WORK_PATH', None)

            if remote_work_path is not None:
                self.__local_filesystem_location = None

                self.__remote_filesystem_location = os.path.join(
                    remote_work_path, direction.lower(), "%(port_name)s"
                )

                self.value = self.__remote_filesystem_location
            else:
                self.__remote_filesystem_location = None

                if value == '.':  # Shortcut for current working directory
                    self.__local_filesystem_location = os.getcwd()
                else:
                    self.__local_filesystem_location = value

                self.value = self.__local_filesystem_location

        else:
            self.value = value

    def __str__(self):
        if self.type == 'directory':
            return '%s: %s -- dir: %s' % (self.name, self.value, self.__local_filesystem_location)
        else:
            return '%s: %s' % (self.name, self.value)

    def __eq__(self, other):
        return self.name == other.name and \
               self.value == other.value and self.path == other.path

    @property
    def type(self):
        return self._port_type

    @property
    def direction(self):
        return self.__direction

    @staticmethod
    def _strip_prefix(s, prefix):
        if s.startswith(prefix):
            return s[len(prefix):]
        else:
            return s

    @property
    def name(self):
        if self.type.lower() == 'directory':
            multiplex_key = 'dir_'
        else:
            multiplex_key = 'str_'

        return self._strip_prefix(self._name, multiplex_key)

    @name.setter
    def name(self, new_name):

        # prefix port name for multiplexing
        if self.type.lower() == 'directory' and new_name != 'source_bundle':
            multiplex_key = 'dir_'
            new_name = multiplex_key + self._strip_prefix(new_name, multiplex_key)
        elif self.type.lower() == 'string' and new_name != 'source_bundle':
            multiplex_key = 'str_'
            new_name = multiplex_key + self._strip_prefix(new_name, multiplex_key)

        self._name = new_name
        self.__task_wf_json['name'] = new_name

        # Substitute in name of port for the remote path
        if self.value and '%(port_name)s' in self.value:
            self.value = self.value % {'port_name': new_name}

        # Make the dir
        if self.direction == 'Output' and self.type == 'directory':
            if not os.path.isdir(self.value):
                try:
                    os.makedirs(self.value)
                except OSError as e:
                    if 'No such file or directory' not in e.strerror:
                        raise e

    @property
    def json(self):
        return self.__task_wf_json

    @staticmethod
    def is_port(obj):
        """Predicate for inspect.getmodules function"""
        return isinstance(obj, Port)

    @property
    def path(self):
        if self.__local_filesystem_location is None and \
                self.__remote_filesystem_location is None and \
                self.type == 'directory':
            raise ValueError('Directory ports must be provided with a location')

        # If remote is True then use it no matter what
        if self.__remote_filesystem_location is not None:
            actual_path = self.__remote_filesystem_location % {'port_name': self._name}
            return actual_path
        else:
            return self.__local_filesystem_location

    def list_files(self, extensions=None):
        """
        List the ports contents by file type or all.
        :param extensions: string extensions, single string or list of extensions.
        :return: A list of full path names of each file.
        """
        if self.type.lower() != 'directory':
            raise ValueError("Port type is not == directory")

        filesystem_location = self.path

        for root, dirs, files in os.walk(filesystem_location):
            if extensions is None:
                return [os.path.join(root, f) for f in files]
            elif not isinstance(extensions, list):
                extensions = [extensions]

            subset_files = []

            for f in files:
                for extension in extensions:
                    if f.lower().endswith(extension.lower()):
                        subset_files.append(os.path.join(root, f))
                        break
            return subset_files

    def list_tiff(self):
        raise NotImplementedError
        # return self.list_files(extensions=['.TIFF', '.TIF', '.tiff', '.tif'])

    def list_1b(self):
        raise NotImplementedError
        # return self.list_files(extensions=['.TIL', '.til'])

    def write(self, filename, data, overwrite=False):

        if self.__direction != 'Output':
            raise ValueError('Only Output ports can be written to.')

        if self.type != 'directory':
            raise ValueError('Only Directory ports can be written to.')

        if os.path.isabs(filename) and os.path.isfile(filename):
            raise ValueError('File name must be relative to the Ports path')

        write_file = os.path.join(self.path, filename)

        file_mode = 'a' if not overwrite else 'w'

        self._check_or_create_dir(write_file)

        with open(write_file, file_mode) as out_file:
            out_file.write(data)

    @staticmethod
    def _check_or_create_dir(full_path_to_file):
        if os.path.isabs(full_path_to_file) and os.path.isfile(full_path_to_file):
            return
        else:
            folder = os.path.dirname(full_path_to_file)
            if not os.path.isdir(folder):
                os.makedirs(folder)

    @staticmethod
    def is_valid_filesys(path):
        if os.path.isabs(path) and os.path.isdir(path) and \
                not os.path.isfile(path):
            return True
        else:
            raise LocalPortValidationError(
                'Port value %s is not a valid filesystem location' % path
            )

    @staticmethod
    def is_valid_s3_url(url):
        """Checks if the url contains S3. Not an accurate validation of the url"""
        # Skip if the url start with source: (gbdxtools syntax)
        if url.startswith('source:'):
            return True

        scheme, netloc, path, _, _, _ = urlparse(url)

        port_except = RemotePortValidationError(
            'Port value %s is not a valid s3 location' % url
        )

        if len(scheme) < 2:
            raise port_except

        if 's3' in scheme or 's3' in netloc or 's3' in path:
            return True
        else:
            raise port_except


class InputPort(Port):
    """
    Helper Port subclass for Input Ports.
    """

    def __init__(self, value, port_type='directory'):
        # TODO, need to allow source parameter for ports (chaining)?
        super(InputPort, self).__init__(port_type, 'Input', value)


class OutputPort(Port):
    """
    Helper Port subclass for Output Ports.
    """

    def __init__(self, value=None, port_type='directory'):
        super(OutputPort, self).__init__(port_type, 'Output', value)
