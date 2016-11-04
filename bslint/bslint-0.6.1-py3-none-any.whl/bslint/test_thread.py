from progress.spinner import Spinner
from time import sleep

class test_thread():
    def __call__(self, *args, **kwargs):
        spinner = Spinner("Loading")
        while True:
            sleep(0.2)
            spinner.next()
