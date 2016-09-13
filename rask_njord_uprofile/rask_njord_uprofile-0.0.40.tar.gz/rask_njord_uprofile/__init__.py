from hashlib import sha1
from rask.base import Base
from rask.parser.utcode import UTCode
from rask.rmq import ack,BasicProperties
from uuid import uuid4

__all__ = ['Uprofile']

class Uprofile(Base):
    options = {
        'code':{
            'app':{
                'register':{
                    'ok':'479b24788e9a4fcfa0249fb931a8e348'
                }
            },
            'user':{
                'access_control_list_get':{
                    'ok':'8d00be68cf9a4f9083a16c3ba15f7116'
                },
                'access_control_list_set':{
                    'ok':'c0b4280d67e146cc93637dd938f3c295'
                },
                'access_token_auth':{
                    'nok':'81d62caaf2ba446fb85ba21489064232',
                    'ok':'fff0418d0d6f4f3bb9bb1cad6fb10e60'
                },
                'access_token_generate':{
                    'invalid':'ab21f63e3a084d889c78c58e06c896d9',
                    'ok':'05b8d2d0d1b54c2c8621ee2857474ff5'
                },
                'get':'3840ef945d264d819ffb8495a7c3252b',
                'not_found':'6c4ac7b57aec4e7baac90752f8d0594b',
                'sets':{
                    'get':{
                        'nok':'4fcc3da909d143799af1a176eec72ab1',
                        'ok':'0241c72845a04e08acb2379fd4ae5902'
                    }
                },
                'setter':'5ded1f7e1c59407b9e09f17098f32cc5'
            }
        },
        'rmq':{
            'exchange':{
                'headers':'uprofile_headers',
                'topic':'uprofile'
            },
            'rk':{
                'app':{
                    'register':'uprofile.app.register'
                },
                'user':{
                    'access_control_list_get':'uprofile.access.control.list.get',
                    'access_control_list_set':'uprofile.access.control.list.set',
                    'access_token_auth':'uprofile.user.access_token.auth',
                    'access_token_generate':'uprofile.user.access_token.generate',
                    'get':'uprofile.user.get',
                    'register':'uprofile.user.register',
                    'sets.get':'uprofile.user.sets.get',
                    'sets.op':'uprofile.user.sets.op',
                    'setter':'uprofile.user.setter'
                }
            }
        }
    }
    
    def __init__(self,rmq):
        self.options['rmq']['queue'] = self.etag
        self.rmq = rmq
        self.utcode = UTCode()
        self.ioengine.loop.add_callback(self.__services__)

    @property
    def __channel__(self):
        try:
            assert self.__channel
        except (AssertionError,AttributeError):
            self.__channel = {}
        except:
            raise
        return self.__channel

    @property
    def __request__(self):
        try:
            assert self.__request
        except (AssertionError,AttributeError):
            self.__request = {}
        except:
            raise
        return self.__request

    @property
    def active(self):
        try:
            assert self.__active
        except (AssertionError,AttributeError):
            self.__active = False
        except:
            raise
        return self.__active
    
    @active.setter
    def active(self,_):
        try:
            assert _
            assert 'consumer' in self.__channel__
            assert 'pusher' in self.__channel__
        except AssertionError:
            self.__active = False
        except:
            raise
        else:
            self.__active = True
            self.ioengine.loop.add_callback(self.__promise_consume__)
        
    @property
    def etag(self):
        return sha1('uprofile:%s:%s' % (self.uuid,uuid4().hex)).hexdigest()

    def __queue_declare__(self):
        def on_declare(*args):
            self.__channel__['consumer'].basic_consume(
                consumer_callback=self.on_msg,
                queue=self.options['rmq']['queue']
            )
            self.active = True
            return True
        
        self.__channel__['consumer'].queue_declare(
            callback=on_declare,
            queue=self.options['rmq']['queue'],
            durable=False,
            exclusive=True
        )
        return True

    def __push__(self,payload,rk,future,nowait=False):
        etag = self.etag

        def on_encode(_):
            self.__channel__['pusher'].basic_publish(
                body=_.result(),
                exchange=self.options['rmq']['exchange']['topic'],
                properties=BasicProperties(headers={'etag':etag}),
                routing_key=rk
            )
            return True

        try:
            assert nowait
        except AssertionError:
            def on_response(_):
                future.set_result(_.result())
                self.__channel__['consumer'].queue_unbind(
                    callback=None,
                    queue=self.options['rmq']['queue'],
                    exchange=self.options['rmq']['exchange']['headers'],
                    arguments={
                        'etag':etag,
                        'uprofile-response':True,
                        'x-match':'all'
                    }
                )
                return True
            
            self.__request__[etag] = self.ioengine.future(on_response)
        
            self.__channel__['consumer'].queue_bind(
                callback=None,
                queue=self.options['rmq']['queue'],
                exchange=self.options['rmq']['exchange']['headers'],
                arguments={
                    'etag':etag,
                    'uprofile-response':True,
                    'x-match':'all'
                }
            )
        except:
            raise
            
        self.utcode.encode(payload,future=self.ioengine.future(on_encode))
        return True
    
    def __services__(self):
        def on_consumer(_):
            self.log.info('channel consumer')
            self.__channel__['consumer'] = _.result().channel
            self.ioengine.loop.add_callback(self.__queue_declare__)
            return True
        
        def on_pusher(_):
            self.log.info('channel pusher')
            self.__channel__['pusher'] = _.result().channel
            return True
        
        self.rmq.channel('uprofile_consumer_%s' % self.uuid,self.ioengine.future(on_consumer))
        self.rmq.channel('uprofile_pusher_%s' % self.uuid,self.ioengine.future(on_pusher))
        return True
   
    def app_register(self,user,name,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.app_register,
                    user=user,
                    name=name,
                    future=future
                )
                return True

            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:
            def on_response(_):
                try:
                    assert _.result()['header']['code'] == self.options['code']['app']['register']['ok']
                except AssertionError:
                    future.set_result(False)
                except:
                    raise
                else:
                    future.set_result(_.result()['body']['uid'])
                return True
            
            self.ioengine.loop.add_callback(
                self.__push__,
                payload={
                    'name':name,
                    'user':user
                },
                rk=self.options['rmq']['rk']['app']['register'],
                future=self.ioengine.future(on_response)
            )
        return True
    
    def on_msg(self,channel,method,properties,body):
        try:
            assert properties.headers['etag'] in self.__request__
        except AssertionError:
            channel.basic_publish(
                body=body,
                exchange=self.options['rmq']['exchange']['topic'],
                routing_key='',
                properties=properties
            )
        except KeyError:
            pass
        except:
            raise
        else:
            def on_decode(_):
                self.__request__[properties.headers['etag']].set_result({'header':properties.headers,'body':_.result()})
                del self.__request__[properties.headers['etag']]
                return True

            self.utcode.decode(body,future=self.ioengine.future(on_decode))

        ack(channel,method)(True)
        return True

    def user_access_control_list_get(self,u,l,f):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.user_access_control_list_get,
                    u=u,
                    l=l,
                    f=f
                )
                return True

            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:
            def on_response(_):
                try:
                    assert _.result()['header']['code'] == self.options['code']['user']['access_control_list_get']['ok']
                except AssertionError:
                    result = False
                except:
                    raise
                else:
                    result = _.result()['body']

                f.set_result(result)
                return True

            self.ioengine.loop.add_callback(
                self.__push__,
                payload={
                    'uid':u,
                    'list':l
                },
                rk=self.options['rmq']['rk']['user']['access_control_list_get'],
                future=self.ioengine.future(on_response)
            )
        return True

    def user_access_control_list_set(self,u,l,n,v,f):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.user_access_control_list_set,
                    u=u,
                    l=l,
                    n=n,
                    v=v,
                    f=f
                )
                return True

            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:
            def on_response(_):
                try:
                    assert _.result()['header']['code'] == self.options['code']['user']['access_control_list_set']['ok']
                except AssertionError:
                    result = False
                except:
                    raise
                else:
                    result = True

                f.set_result(result)
                return True

            self.ioengine.loop.add_callback(
                self.__push__,
                payload={
                    'uid':u,
                    'list':l,
                    'name':n,
                    'value':v
                },
                rk=self.options['rmq']['rk']['user']['access_control_list_set'],
                future=self.ioengine.future(on_response)
            )
        return True
    
    def user_access_token_auth(self,u,a,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.user_access_token_auth,
                    u=u,
                    a=a,
                    future=future
                )
                return True

            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:
            def on_response(_):
                try:
                    assert _.result()['header']['code'] == self.options['code']['user']['access_token_auth']['ok']
                except AssertionError:
                    future.set_result(False)
                except:
                    raise
                else:
                    future.set_result(_.result()['body'])
                return True
            
            self.ioengine.loop.add_callback(
                self.__push__,
                payload={
                    'u':u,
                    'a':a
                },
                rk=self.options['rmq']['rk']['user']['access_token_auth'],
                future=self.ioengine.future(on_response)
            )
        return True
    
    def user_access_token_generate(self,email,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.user_access_token_generate,
                    email=email,
                    future=future
                )
                return True

            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:           
            def on_response(_):
                try:
                    assert _.result()['header']['code'] == self.options['code']['user']['access_token_generate']['ok'] or _.result()['header']['code'] == self.options['code']['user']['access_token_generate']['invalid']
                except AssertionError:
                    def on_register(_):
                        self.ioengine.loop.add_callback(
                            self.user_access_token_generate,
                            email=email,
                            future=future
                        )
                        return True

                    self.ioengine.loop.add_callback(
                        self.user_register,
                        email=email,
                        future=self.ioengine.future(on_register)
                    )
                    self.log.info('%s is not found, creating' % email)
                except:
                    raise
                else:
                    self.log.info('%s access token generated' % email)
                    future.set_result(_.result()['body'])
                return True
           
            self.ioengine.loop.add_callback(
                self.__push__,
                payload=email,
                rk=self.options['rmq']['rk']['user']['access_token_generate'],
                future=self.ioengine.future(on_response)
            )
            self.log.info('access token generate: %s' % email)
        return True

    def user_get(self,uid,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.user_get,
                    uid=uid,
                    future=future
                )
                return True

            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:
            def on_response(_):
                future.set_result(_.result()['body'])
                return True

            self.ioengine.loop.add_callback(
                self.__push__,
                payload=uid,
                rk=self.options['rmq']['rk']['user']['get'],
                future=self.ioengine.future(on_response)
            )
        return True
    
    def user_register(self,email,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.user_register,
                    email=email,
                    future=future
                )
                return True

            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:
            def on_response(_):
                future.set_result(True)
                self.log.info('%s created' % email)
                return True

            self.ioengine.loop.add_callback(
                self.__push__,
                payload=email,
                rk=self.options['rmq']['rk']['user']['register'],
                future=self.ioengine.future(on_response)
            )

            self.log.info('creating %s' % email)
        return True

    def user_sets_get(self,uid,name,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.user_sets_get,
                    uid=uid,
                    name=name,
                    future=future
                )
                return True
            
            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:
            def on_response(_):
                future.set_result(_)
                return True

            self.ioengine.loop.add_callback(
                self.__push__,
                payload={
                    'uid':uid,
                    'name':name
                },
                rk=self.options['rmq']['rk']['user']['sets.get'],
                future=self.ioengine.future(on_response)
            )
            self.log.info('sets get %s from %s' % (name,uid))
        return True

    def user_sets_op(self,uid,payload):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.user_sets_op,
                    uid=uid,
                    payload=payload
                )
                return True
            
            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:
            self.ioengine.loop.add_callback(
                self.__push__,
                payload={
                    'uid':uid,
                    'payload':payload
                },
                rk=self.options['rmq']['rk']['user']['sets.op'],
                future=None,
                nowait=True
            )
            self.log.info('sets op %s' % uid)
        return True
    
    def user_setter(self,uid,payload,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.user_setter,
                    uid=uid,
                    payload=payload,
                    future=future
                )
                return True

            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:
            def on_response(_):
                future.set_result(True)
                return True

            self.ioengine.loop.add_callback(
                self.__push__,
                payload={'uid':uid,'setter':payload},
                rk=self.options['rmq']['rk']['user']['setter'],
                future=self.ioengine.future(on_response)
            )
        return True
