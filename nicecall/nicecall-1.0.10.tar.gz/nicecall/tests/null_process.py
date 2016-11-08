import nicecall


class NullProcess(nicecall.Process):
    def execute(self, args=None):
        return 0
