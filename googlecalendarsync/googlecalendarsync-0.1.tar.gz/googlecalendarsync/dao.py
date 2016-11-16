class Dao:

    def init(self):
        pass

    def close(self):
        pass

    def __del__(self):
        self.close()

class TriggerDao(Dao):

    callbacks = []

    def registerCallback(self, callback_method):
        callbacks.append(callback_method)

    def unregisterCallback(self, callback_method):
        try:
            callbacks.remove(callback_method)
        except ValueError:
            pass

    def sendTrigger(self, daotrigger):
        for callback in callbacks:
            callback(daotrigger)