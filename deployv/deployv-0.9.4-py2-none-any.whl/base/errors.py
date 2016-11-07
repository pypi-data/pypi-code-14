

class DeployVException(Exception):
    msg = None

    def __init__(self, message, *args, **kwargs):
        self.msg = message
        super(DeployVException, self).__init__(message, *args, **kwargs)

    def __str__(self):
        return self.msg


class NotRunning(DeployVException):
    def __init__(self, container):
        super(NotRunning, self).__init__('Container {} is not running'.format(container))


class NoSuchContainer(DeployVException):
    def __init__(self, container):
        super(NoSuchContainer, self).__init__('No such container or id: {}'.format(container))


class FileNotFoundInContainer(DeployVException):
    def __init__(self, container, filename):
        super(FileNotFoundInContainer, self).__init__('File {0} not found in the {1} container'
                                                      .format(filename, container))


class ErrorPort(DeployVException):
    def __init__(self, message):
        super(ErrorPort, self).__init__(message)


class BuildError(DeployVException):
    def __init__(self, message):
        super(BuildError, self).__init__(message)
