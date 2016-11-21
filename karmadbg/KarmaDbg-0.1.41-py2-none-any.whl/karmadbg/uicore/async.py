
from PySide.QtCore import QObject, Signal

class AsyncOperation(QObject):

    def __init__(self, asyncmgr):
        QObject.__init__(self)
        self.asyncmgr = dbgclient.asyncmgr
  
    def doTaskAsync(self):
        self.asyncmgr.start(self)

def async(fn):

    def wrapper(*args, **kwargs):

        class AsyncState(QObject):

            asyncComplete = Signal()

            def __init__(self):
                super(AsyncState,self).__init__()
                self.async = fn(*args, **kwargs)
                self.weakref = self

            def asyncCall(self):
                try:
                    self.asyncOp = self.async.next()
                    self.asyncOp.asyncDone.connect(self.onAsyncDone)
                    self.asyncOp.doTaskAsync()
                except StopIteration:
                    self.asyncComplete.emit()
                    del self.weakref

            def onAsyncDone(self, result):
                try:
                    if isinstance(result[0], Exception):
                        self.asyncOp = self.async.throw(result[0])
                    else:
                        self.asyncOp = self.async.send(result[0])
                    self.asyncOp.asyncDone.connect(self.onAsyncDone)
                    self.asyncOp.doTaskAsync()
                except StopIteration:
                    self.asyncComplete.emit()
                    del self.weakref

            def __del__(self):
                pass
                
        asyncState = AsyncState()
        asyncState.asyncCall()

    return wrapper

