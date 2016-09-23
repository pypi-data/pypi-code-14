import time
from threading import Event

import logging
import logging.handlers

# pip install paho-mqtt
import paho.mqtt.client as paho


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
            client.on_log=self._callbackOnLog

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
        self.logger.debug('received %s:%s' % (message.topic, message.payload))
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
        if client:
            self.logger.debug('subscribe(%s) with qos %d' % (topic, qos))
            try:
                client.subscribe(topic, qos)
            except:
                self.logger.exception('subscribe')

    def publish(self, topic, data, qos=0, retain=False):
        client=self.client()
        if client:
            try:
                client.publish(topic, data, qos, retain)
            except:
                self.logger.exception('publish')

    def loop(self, timeout=0.1, ):
        try:
            self.connect()
            client=self.client()
            if client:
                client.loop(timeout=0.1)
        except:
            pass

    def manager(self):
        try:
            self.connect()
            client=self.client()
            if client:
                client.loop(timeout=0.1)
        except KeyboardInterrupt:
            self.stop()
        except:
            self.logger.exception('manager()')

    def serveForEver(self):
        try:
            while not self._eventStop.isSet():
                self.manager()
        except KeyboardInterrupt:
            self.stop()
        except:
            pass


if __name__ == "__main__":
    pass
