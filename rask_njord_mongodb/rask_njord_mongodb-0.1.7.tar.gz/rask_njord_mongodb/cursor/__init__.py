from rask.base import Base

__all__ = ['Cursor']

class Cursor(Base):
    def __init__(self,cluster,uid,cursor,fetch,close):
        self.__cluster = cluster
        self.__uid = uid
        self.__cursor = cursor
        self.__fetch = fetch
        self.__close = close

    def export(self):
        return {
            'cluster':self.__cluster,
            'uid':self.__uid,
            'cursor':self.__cursor
        }

    def close(self):
        self.__close(
            cluster=self.__cluster,
            uid=self.__uid,
            cursor=self.__cursor
        )
        return True

    def next(self,future):
        def check_doc(doc):
            try:
                assert doc
            except AssertionError:
                future.set_exception(StopIteration())
            except:
                raise
            else:
                future.set_result(doc)
            return True

        def on_fetch(_):
            try:
                assert _.result()['ok']
            except (AssertionError,TypeError):
                future.set_exception(CursorError(_.result()['err']))
            except:
                raise
            else:
                self.ioengine.loop.add_callback(
                    check_doc,
                    _.result()['doc']
                )
            return True

        self.__fetch(
            cluster=self.__cluster,
            uid=self.__uid,
            cursor=self.__cursor,
            future=self.ioengine.future(on_fetch)
        )
        return True

class CursorError(Exception):
    pass
