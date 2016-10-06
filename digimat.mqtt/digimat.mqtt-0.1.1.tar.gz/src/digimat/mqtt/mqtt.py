import time
from threading import Event

import logging
import logging.handlers

# pip install paho-mqtt
import paho.mqtt.client as paho


class MQTTPayload(object):
    def __init__(self, item):
        self._item=item
        self._value=None
        self._data=None

    @property
    def item(self):
        return self._item

    @property
    def client(self):
        return self.item.client

    @property
    def logger(self):
        return self.item.logger

    @property
    def data(self):
        return self._data

    @property
    def value(self):
        return self._value

    # to be overriden
    def validateData(self, data):
        return True

    def signalUpdate(self):
        self.item.signalUpdate()

    def loadData(self, data):
        if data is not None and self.validateData(data):
            value=self.decodeData(data)
            if value is not None:
                # self.logger.debug('[%s]' % (self.item.topic))
                self._data=data
                if value != self._value:
                    self._value=value
                    self.signalUpdate()
                    return True

    # to be overriden
    def decodeData(self, data):
        return data

    def toString(self, data):
        try:
            return str(data)
        except:
            pass

    def toBoolean(self, data):
        try:
            data=data.toString().lower().strip()
            if data in ['false', '0', 'no', 'off']:
                return False
            if data in ['true', '1', 'yes', 'on']:
                return True
        except:
            pass

    def toFloat(self, data):
        try:
            return float(data)
        except:
            pass

    def toInteger(self, data):
        try:
            return int(data)
        except:
            pass

    def set(self, data):
        if data and self.loadData(data):
            self.item.publish()


class MQTTPayloadBool(MQTTPayload):
    def decodeData(self, data):
        return self.toBoolean(data)

    def set(self, state):
        data='0'
        if state:
            data='1'
        super(MQTTPayloadBool, self).set(data)


class MQTTItem(object):
    def __init__(self, client, topic, qos=0, retain=False, payload=None):
        self._client=client
        self._topic=topic
        self._qos=int(qos)
        self._retain=bool(retain)
        self._eventSubscribe=Event()
        self._eventPublish=Event()

        if payload is None:
            payload=MQTTPayload(self)
        self._payload=payload

        self.logger.info('item [%s] qos=%d created' % (topic, qos))

    @property
    def client(self):
        return self._client

    @property
    def logger(self):
        return self._client.logger

    @property
    def topic(self):
        return self._topic

    @property
    def payload(self):
        return self._payload

    @property
    def data(self):
        return self.payload.data

    @property
    def value(self):
        return self.payload.value

    def signalUpdate(self):
        print "TODO: signalupdate"
        self.logger.debug('item [%s] updated (%s)' % (self.topic, self.data))

    def subscribe(self):
        self._eventSubscribe.set()
        if self.client.subscribe(self.topic, self._qos):
            self._eventSubscribe.clear()
            return True

    def publish(self):
        self._eventPublish.set()
        if self.client.publish(self.topic, self.payload.data, self._qos, self._retain):
            self._eventPublish.clear()
            return True


class MQTTClient(object):
    def __init__(self, cid=None, host=None, port=1883, userName=None, userPassword=None, cleanSession=True, logServer='localhost', logLevel=logging.DEBUG):
        self._host=host
        self._port=port
        self._userName=None
        self._userPassword=None
        self._tlsCertificateFile=None
        self._cid=cid
        self._cleanSession=cleanSession
        self._client=None
        self._connected=False
        self._timeoutConnect=0
        self._eventStop=Event()

        logger=logging.getLogger("MTTQ(%s)" % (cid))
        logger.setLevel(logLevel)
        socketHandler = logging.handlers.SocketHandler(logServer, logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        logger.addHandler(socketHandler)
        self._logger=logger

        self._topicRoot=None
        self._items=[]
        self._indexItemFromTopic={}

        self.setUser(userName, userPassword)

    @property
    def logger(self):
        return self._logger

    def setClientId(self, cid):
        self._cid=cid

    def setUser(self, name, password):
        self._userName=name
        self._userPassword=password

    def setTLSCertificate(self, cfile):
        self._tlsCertificateFile=cfile

    def setRootTopic(self, topic):
        self._topicRoot=topic

    def buildTopic(self, topic):
        if topic:
            if not self._topicRoot:
                return topic
            return '/'.join([self._topicRoot, topic])

    def subscribeToRootTopic(self, qos=0):
        if self._topicRoot:
            topic=self.buildTopic('#')
            return self.subscribe(topic, qos)

    def itemFromTopic(self, topic):
        try:
            return self._indexItemFromTopic[topic]
        except:
            pass

    def item(self, topic):
        return self.itemFromTopic(topic)

    def createItem(self, topic, qos=0, payload=None):
        if topic:
            item=self.itemFromTopic(topic)
            if not item:
                item=MQTTItem(self, topic, qos, payload)
                self._items.append(item)
                self._indexItemFromTopic[topic]=item
                self.logger.debug('now %d items' % len(self._items))
            return item

    def createItemUnderRootTopic(self, topic, qos=0, payload=None):
        return self.createItem(self.buildTopic(topic), qos, payload)

    def syncItems(self):
        for item in self._items:
            item.subscribe()
            if item._eventPublish.isSet():
                item.publish()

    def client(self):
        if self._client:
            return self._client
        try:
            self.logger.debug('creating mqtt-paho client')
            # client=paho.Client(client_id=self._cid, clean_session=self._cleanSession)
            client=paho.Client(client_id='', clean_session=True)

            # register callbacks
            client.on_connect=self._callbackOnConnect
            client.on_disconnect=self._callbackOnDisconnect
            client.on_subscribe=self._callbackOnSubscribe
            client.on_unsubscribe=self._callbackOnUnsubscribe
            client.on_publish=self._callbackOnPublish
            client.on_message=self._callbackOnMessage

            # comment to disable paho-mqtt logging
            # client.on_log=self._callbackOnLog

            if self._userName:
                self.logger.info('using broker user [%s]' % self._userName)
                client.username_pw_set(self._userName, self._userPassword)
            if self._tlsCertificateFile:
                self.logger.info('using TLS certificate file [%s]' % self._tlsCertificateFile)
                client.tls_set(self._tlsCertificateFile)

            self._connected=False
            self._client=client
            return self._client
        except:
            self.logger.exception('client()')

    def isConnected(self):
        if self._client:
            if self._connected:
                return True

    def connect(self):
        if self.isConnected():
            return self._client

        self._eventStop.clear()
        client=self.client()
        if client:
            try:
                if time.time()>self._timeoutConnect:
                    self.logger.info('connecting to broker %s:%d...' % (self._host, self._port))
                    client.connect(self._host, self._port, keepalive=30, bind_address='')
                    self._timeoutConnect=time.time()+15
            except:
                self.logger.exception('connect()')

    def _callbackOnConnect(self, client, userdata, flags, rc):
        self.logger.info('connect(%d)' % rc)
        if rc == 0:
            self._connected=True
            self.syncItems()
            self.onConnect()
        else:
            # 1: Connection refused - incorrect protocol version
            # 2: Connection refused - invalid client identifier
            # 3: Connection refused - server unavailable
            # 4: Connection refused - bad username or password
            # 5: Connection refused - not authorised
            # 6-255: Currently unused.
            self._timeoutConnect=time.time()+60
            self._connected=False

    def onConnect(self):
        pass

    def _callbackOnDisconnect(self, client, userdata, rc):
        self.logger.info('disconnect(%d)' % rc)
        self._connected=False
        self.onDisconnect()

    def onDisconnect(self):
        pass

    def _callbackOnLog(self, client, userdata, level, buf):
        if level==paho.MQTT_LOG_ERR:
            self.logger.error(buf)
        elif level==paho.MQTT_LOG_WARNING:
            self.logger.warning(buf)
        elif level in (paho.MQTT_LOG_NOTICE, paho.MQTT_LOG_INFO):
            self.logger.info(buf)
        else:
            self.logger.debug(buf)

    def _callbackOnSubscribe(self, client, userdata, mid, granted_qos):
        pass

    def _callbackOnUnsubscribe(self, client, userdata, mid):
        pass

    def _callbackOnPublish(self, client, userdata, mid):
        pass

    def _callbackOnMessage(self, client, userdata, message):
        # self.logger.debug('onMessage(%s) qos=%d retain=%d (%d bytes)' %
        #        (message.topic, message.qos, message.retain,
        #         len(message.payload)))

        try:
            item=self.itemFromTopic(message.topic)
            if item:
                self.logger.debug('%s->onMessage(%s)' % (message.topic, message.payload))
                item.payload.loadData(message.payload)
                # stop message propagation if item found
                return
        except:
            self.logger.exception('item data load')

        self.onMessage(message.topic, message.payload, message.qos, message.retain)

    def onMessage(self, topic, data, qos, retain):
        pass

    def stop(self):
        if not self._eventStop.isSet():
            self.logger.info('Stop!')
            self._eventStop.set()

    def disconnect(self):
        self.stop()
        client=self.client()
        try:
            self.logger.info('disconnect()')
            client.disconnect()
        except:
            pass
        self._connected=False

    def subscribe(self, topic='#', qos=0):
        client=self.client()
        if client and self.isConnected():
            try:
                self.logger.debug('subscribe(%s)' % (topic))
                if client.subscribe(topic, qos):
                    return True
            except:
                self.logger.exception('subscribe')

    def publish(self, topic, data, qos=0, retain=False):
        client=self.client()
        if client and self.isConnected():
            try:
                self.logger.debug('publish(%s)->%s' % (topic, data))
                if client.publish(topic, data, qos, retain):
                    return True
            except:
                self.logger.exception('publish')

    def loop(self, timeout=0.1):
        self.connect()
        client=self.client()
        if client:
            client.loop(timeout=0.1)

    def manager(self):
        try:
            self.loop()
        except KeyboardInterrupt:
            self.disconnect()
        except:
            self.logger.exception('manager()')

    def serveForEver(self):
        try:
            while not self._eventStop.isSet():
                self.manager()
        except KeyboardInterrupt:
            self.disconnect()
        except:
            pass


if __name__ == "__main__":
    pass
