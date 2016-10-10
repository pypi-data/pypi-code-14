from hashlib import sha1
from pika import BasicProperties
from rask.base import Base
from rask.parser.json import dictfy,jsonify
from .cursor import Cursor

__all__ = ['Mongodb']

class Mongodb(Base):
    __queue = None
    __publish = None
    __request = None
    options = {
        'rmq':{
            'exchange':{
                'topic':'njord_mongodb',
                'headers':'njord_mongodb_headers'
            },
            'services':{
                'aggregate':'njord.mongodb.aggregate.%s',
                'find':'njord.mongodb.find.%s',
                'find_and_modify':'njord.mongodb.find_and_modify.%s',
                'find_one':'njord.mongodb.find_one.%s',
                'insert':'njord.mongodb.insert.%s',
                'remove':'njord.mongodb.remove.%s',
                'save':'njord.mongodb.save.%s',
                'update':'njord.mongodb.update.%s'
            }
        }
    }

    @property
    def __request__(self):
        try:
            assert self.__request
        except AssertionError:
            self.__request = {}
        except:
            raise
        return self.__request

    @property
    def etag(self):
        return sha1('%s:%s' % (self.uuid,self.ioengine.uuid4)).hexdigest()

    @property
    def queue(self):
        try:
            assert self.__queue
        except AssertionError:
            self.__queue = 'njord_mongodb_%s' % sha1('%s:%s' % (self.uuid,self.ioengine.uuid4)).hexdigest()
        except:
            raise
        return self.__queue

    @property
    def publish(self):
        try:
            assert self.__publish
        except AssertionError:
            return None
        except:
            raise
        return self.__publish.basic_publish

    def __consumer__(self):
        def on(channel):
            channel.result().channel.basic_consume(
                consumer_callback=self.__on_msg__,
                queue=self.queue
            )
            self.__ready__('consumer')
            return True

        self.rmq.channel('mongodb_consumer_%s' % self.uuid,self.ioengine.future(on))
        return True

    def __execute__(self,name,cluster,body,future):
        etag = self.etag
        body['etag'] = etag
        body['dogtag'] = self.uuid

        def on_response(result):
            try:
                result = dictfy(result.result())
                assert result['ok']
            except (AssertionError,KeyError):
                future.set_exception(ExecutionError(result.get('err')))
            except:
                raise
            else:
                future.set_result(result)
            return True

        self.__request__[etag] = self.ioengine.future(on_response)
        self.publish(
            body=jsonify(body),
            exchange=self.options['rmq']['exchange']['topic'],
            routing_key=self.options['rmq']['services'][name] % cluster
        )
        return True

    def __init__(self,rmq):
        self.rmq = rmq
        self.__wait__ = ['publish','consumer']
        self.ioengine.loop.add_callback(self.__services__)

    def __on_msg__(self,channel,method,properties,body):
        try:
            assert properties.headers['etag'] in self.__request__
        except (AssertionError,KeyError):
            pass
        except:
            raise
        else:
            self.__request__[properties.headers['etag']].set_result(body)
            del self.__request__[properties.headers['etag']]

        channel.basic_ack(method.delivery_tag)
        return True

    def __queue_declare__(self,channel):
        def on_bind(*args):
            self.ioengine.loop.add_callback(self.__consumer__)
            return True

        def on_declare(*args):
            channel.queue_bind(
                callback=on_bind,
                exchange=self.options['rmq']['exchange']['headers'],
                queue=self.queue,
                routing_key='',
                arguments={
                    'dogtag':self.uuid
                }
            )
            return True

        channel.queue_declare(
            callback=on_declare,
            queue=self.queue,
            durable=False,
            exclusive=True,
            auto_delete=True
        )
        return True

    def __ready__(self,_):
        try:
            self.__wait__.remove(_)
            self.log.info(_)
            assert not self.__wait__
        except (AssertionError,ValueError):
            pass
        except:
            raise
        else:
            self.active = True
        return True

    def __services__(self):
        def announce(channel):
            self.ioengine.loop.add_callback(self.__queue_declare__,channel=channel.result().channel)
            return True

        def publish(channel):
            self.__publish = channel.result().channel
            self.__ready__('publish')
            return True

        self.rmq.channel('mongodb_announce_%s' % self.uuid,self.ioengine.future(announce))
        self.rmq.channel('mongodb_publish_%s' % self.uuid,self.ioengine.future(publish))
        return True

    def aggregate(self,cluster,db,collection,pipeline,future,**kwargs):
        try:
            assert self.active
        except AssertionError:
            def on(_):
                self.ioengine.loop.add_callback(
                    self.aggregate,
                    cluster=cluster,
                    db=db,
                    collection=collection,
                    pipeline=pipeline,
                    future=future
                )
                return True

            self.promises.append(self.ioengine.future(on))
        except:
            raise
        else:
            def on_cursor(_):
                try:
                    assert _.result()['cursor']
                except AssertionError:
                    future.set_result({
                        'doc':_.result()['doc'],
                        'cursor':None
                    })
                except ExecutionError as ex:
                    future.set_exception(ex)
                except:
                    raise
                else:
                    future.set_result({
                        'doc':_.result()['doc'],
                        'cursor':Cursor(
                            cluster=cluster,
                            uid=_.result()['cursor']['uid'],
                            cursor=_.result()['cursor']['id'],
                            fetch=self.fetch,
                            close=self.close
                        )
                    })
                return True

            self.ioengine.loop.add_callback(
                self.__execute__,
                name='aggregate',
                cluster=cluster,
                body={
                    'db':db,
                    'collection':collection,
                    'pipeline':pipeline
                },
                future=self.ioengine.future(on_cursor)
            )
        return True

    def close(self,cluster,uid,cursor):
        try:
            assert self.active
        except AssertionError:
            def on(_):
                self.ioengine.lopp.add_callback(
                    self.close,
                    cluster=cluster,
                    uid=uid,
                    cursor=cursor
                )
                return True

            self.promises.append(self.ioengine.future(on))
        except:
            raise
        else:
            self.publish(
                body=jsonify({
                    'id':cursor
                }),
                exchange=self.options['rmq']['exchange']['topic'],
                routing_key='',
                properties=BasicProperties(headers={
                    'cluster':cluster,
                    'service':'close',
                    'uid':uid
                })
            )
        return True

    def cursor(self,cluster,uid,cursor):
        return Cursor(
            cluster=cluster,
            uid=uid,
            cursor=cursor,
            fetch=self.fetch,
            close=self.close
        )

    def fetch(self,cluster,uid,cursor,future):
        try:
            assert self.active
        except AssertionError:
            def on(_):
                self.ioengine.lopp.add_callback(
                    self.fetch,
                    cluster=cluster,
                    uid=uid,
                    cursor=cursor,
                    future=future
                )
                return True

            self.promises.append(self.ioengine.future(on))
        except:
            raise
        else:
            def on_response(_):
                future.set_result(dictfy(_.result()))
                return True

            etag = self.etag
            self.__request__[etag] = self.ioengine.future(on_response)
            self.publish(
                body=jsonify({
                    'etag':etag,
                    'dogtag':self.uuid,
                    'id':cursor
                }),
                exchange=self.options['rmq']['exchange']['topic'],
                routing_key='',
                properties=BasicProperties(headers={
                    'cluster':cluster,
                    'service':'fetch',
                    'uid':uid
                })
            )
        return True

    def find(self,cluster,db,collection,query,future,**kwargs):
        try:
            assert self.active
        except AssertionError:
            def on(_):
                self.ioengine.loop.add_callback(
                    self.find,
                    cluster=cluster,
                    db=db,
                    collection=collection,
                    query=query,
                    future=future,
                    **kwargs
                )
                return True

            self.promises.append(self.ioengine.future(on))
        except:
            raise
        else:
            def on_cursor(_):
                try:
                    assert _.result()['cursor']
                except AssertionError:
                    future.set_result(_.result())
                except ExecutionError as ex:
                    future.set_exception(ex)
                except:
                    raise
                else:
                    future.set_result({
                        'doc':_.result()['doc'],
                        'cursor':self.cursor(
                            cluster=cluster,
                            uid=_.result()['cursor']['uid'],
                            cursor=_.result()['cursor']['id']
                        )
                    })
                return True

            kwargs['spec'] = query
            self.ioengine.loop.add_callback(
                self.__execute__,
                name='find',
                cluster=cluster,
                body={
                    'db':db,
                    'collection':collection,
                    'args':kwargs
                },
                future=self.ioengine.future(on_cursor)
            )
        return True

    def find_and_modify(self,cluster,db,collection,query,future,update=None,remove=False,**kwargs):
        try:
            assert self.active
        except AssertionError:
            def on(_):
                self.ioengine.loop.add_callback(
                    self.find_and_modify,
                    cluster=cluster,
                    db=db,
                    collection=collection,
                    query=query,
                    future=future,
                    update=update,
                    remove=remove,
                    **kwargs
                )
                return True

            self.promises.append(self.ioengine.future(on))
        except:
            raise
        else:
            def on_find(_):
                try:
                    future.set_result(_.result()['doc'])
                except ExecutionError as ex:
                    future.set_exception(ex)
                except:
                    raise
                return True

            kwargs.update({
                'query':query,
                'update':update,
                'remove':remove
            })
            self.ioengine.loop.add_callback(
                self.__execute__,
                name='find_and_modify',
                cluster=cluster,
                body={
                    'db':db,
                    'collection':collection,
                    'args':kwargs
                },
                future=self.ioengine.future(on_find)
            )
        return True

    def find_one(self,cluster,db,collection,query,future,**kwargs):
        try:
            assert self.active
        except AssertionError:
            def on(_):
                self.ioengine.loop.add_callback(
                    self.find_one,
                    cluster=cluster,
                    db=db,
                    collection=collection,
                    query=query,
                    future=future,
                    **kwargs
                )
                return True

            self.promises.append(self.ioengine.future(on))
        except:
            raise
        else:
            def on_find(_):
                try:
                    future.set_result(_.result()['doc'])
                except ExecutionError as ex:
                    future.set_exception(ex)
                except:
                    raise
                return True

            kwargs['spec_or_id'] = query
            self.ioengine.loop.add_callback(
                self.__execute__,
                name='find_one',
                cluster=cluster,
                body={
                    'db':db,
                    'collection':collection,
                    'args':kwargs
                },
                future=self.ioengine.future(on_find)
            )
        return True

    def insert(self,cluster,db,collection,payload,future,**kwargs):
        try:
            assert self.active
        except AssertionError:
            def on(_):
                self.ioengine.loop.add_callback(
                    self.insert,
                    cluster=cluster,
                    db=db,
                    collection=collection,
                    payload=payload,
                    future=future,
                    **kwargs
                )
                return True

            self.promises.append(self.ioengine.future(on))
        except:
            raise
        else:
            def on_insert(_):
                try:
                    future.set_result(_.result()['_id'])
                except ExecutionError as ex:
                    future.set_exception(ex)
                except:
                    raise
                return True

            kwargs['doc_or_docs'] = payload
            self.ioengine.loop.add_callback(
                self.__execute__,
                name='insert',
                cluster=cluster,
                body={
                    'db':db,
                    'collection':collection,
                    'args':kwargs
                },
                future=self.ioengine.future(on_insert)
            )
        return True

    def remove(self,cluster,db,collection,query,future,**kwargs):
        try:
            assert self.active
        except AssertionError:
            def on(_):
                self.ioengine.loop.add_callback(
                    self.remove,
                    cluster=cluster,
                    db=db,
                    collection=collection,
                    query=query,
                    future=future,
                    **kwargs
                )
                return True

            self.promises.append(self.ioengine.future(on))
        except:
            raise
        else:
            def on_remove(_):
                try:
                    future.set_result(_.result()['result'])
                except ExecutionError as ex:
                    future.set_exception(ex)
                except:
                    raise
                return True

            kwargs['spec_or_id'] = query
            self.ioengine.loop.add_callback(
                self.__execute__,
                name='remove',
                cluster=cluster,
                body={
                    'db':db,
                    'collection':collection,
                    'args':kwargs
                },
                future=self.ioengine.future(on_remove)
            )
        return True

    def save(self,cluster,db,collection,payload,future,**kwargs):
        try:
            assert self.active
        except AssertionError:
            def on(_):
                self.ioengine.loop.add_callback(
                    self.save,
                    cluster=cluster,
                    db=db,
                    collection=collection,
                    payload=payload,
                    future=future,
                    **kwargs
                )
                return True

            self.promises.append(self.ioengine.future(on))
        except:
            raise
        else:
            def on_save(_):
                try:
                    future.set_result(_.result()['_id'])
                except ExecutionError as ex:
                    future.set_exception(ex)
                except:
                    raise
                return True

            kwargs['to_save'] = payload
            self.ioengine.loop.add_callback(
                self.__execute__,
                name='save',
                cluster=cluster,
                body={
                    'db':db,
                    'collection':collection,
                    'args':kwargs
                },
                future=self.ioengine.future(on_save)
            )
        return True

    def update(self,cluster,db,collection,query,document,future,**kwargs):
        try:
            assert self.active
        except AssertionError:
            def on(_):
                self.ioengine.loop.add_callback(
                    self.update,
                    cluster=cluster,
                    db=db,
                    collection=collection,
                    query=query,
                    document=document,
                    future=future,
                    **kwargs
                )
                return True

            self.promises.append(self.ioengine.future(on))
        except:
            raise
        else:
            def on_update(_):
                try:
                    future.set_result(_.result()['result'])
                except ExecutionError as ex:
                    future.set_exception(ex)
                except:
                    raise
                return True

            kwargs['spec'] = query
            kwargs['document'] = document
            self.ioengine.loop.add_callback(
                self.__execute__,
                name='update',
                cluster=cluster,
                body={
                    'db':db,
                    'collection':collection,
                    'args':kwargs
                },
                future=self.ioengine.future(on_update)
            )
        return True

class ExecutionError(Exception):
    pass
