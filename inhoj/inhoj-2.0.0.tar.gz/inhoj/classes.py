import signal


class GracefulDeath():

    """
    Catch signals to allow graceful process shutdown

    Inspired in:
        - http://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
        - https://github.com/ryran/reboot-guard/blob/master/rguard#L284:L304
    """

    def __init__(self):
        self.kill_now = False

        catch_signals = [
            signal.SIGTERM,
            signal.SIGINT,
            signal.SIGQUIT,
        ]

        for signum in catch_signals:
            signal.signal(signum, self.handle)

    def handle(self, signum, frame):
        self.kill_now = True
