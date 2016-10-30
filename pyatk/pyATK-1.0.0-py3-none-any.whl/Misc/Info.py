import resource
import platform
import os


class CurrentMachine:
    @classmethod
    def architecture(cls):
        return platform.machine()

    @classmethod
    def processor(cls):
        return platform.processor()

    @classmethod
    def os(cls):
        return platform.system()

    @classmethod
    def currentUser(cls):
        return os.getlogin()

    @classmethod
    def memoryUsage(cls):
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
