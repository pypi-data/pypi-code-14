import threading
import uuid


class CauldronThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        """
        """

        super(CauldronThread, self).__init__(*args, **kwargs)
        self.abort = False
        self.daemon = True
        self.uid = str(uuid.uuid4())
        self.command = None
        self.parser = None
        self.kwargs = None
        self.result = None
        self.response = None

    def run(self):
        """
        """

        self.result = self.command(
            parser=self.parser,
            response=self.response,
            **self.kwargs
        )
