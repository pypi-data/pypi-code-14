import md5
import hashlib
import sha3
import msgpack
import msgpackrpc
import pika
import pkg_resources

class Stampery():
    __version = pkg_resources.require("stampery")[0].version
    __event_handlers = {}
    __api_end_points = {'prod' : ['api.stampery.com', 4000],
                     'beta' : ['api-beta.stampery.com', 4000]}
    __amqp_end_points = {'prod' : ['young-squirrel.rmq.cloudamqp.com', 5672, 'consumer', '9FBln3UxOgwgLZtYvResNXE7', 'ukgmnhoi'],
                     'beta' : ['young-squirrel.rmq.cloudamqp.com', 5672, 'consumer', '9FBln3UxOgwgLZtYvResNXE7', 'beta']}

    def __init__(self, secret, branch = 'prod'):
        self.__client_secret = secret
        self.__client_id = md5.new(secret).hexdigest()[0:15]
        self.__api_end_point = self.__api_end_points[branch] or self.__api_end_points['prod']
        self.__amqp_end_point = self.__amqp_end_points[branch] or self.__amqp_end_points['prod']

    def start(self):
        self.__api_login(self.__api_end_point)
        if self.__auth:
            self.__amqp_login(self.__amqp_end_point)

    def hash(self, data):
        return hashlib.sha3_512(data).hexdigest().upper()

    def on(self, event_type, callback):
        if(hasattr(callback, '__call__')):
            self.__event_handlers[event_type] = callback
        else:
            raise ValueError('Event callback is not callable.')

    def __emit(self, event_type, *args):
        if(event_type in self.__event_handlers):
            self.__event_handlers[event_type](*args)

    def stamp(self, hash):
        print("\nStamping \n%s" % hash)
        try:
            self.__api_client.call('stamp', hash.upper())
        except Exception as e:
            self.__emit("error", e)

    def __api_login(self, endpoint):
        self.__api_client = msgpackrpc.Client(msgpackrpc.Address(endpoint[0], endpoint[1]), unpack_encoding='utf-8')
        req = self.__api_client.call_async('stampery.3.auth', self.__client_id, self.__client_secret, "python-" + self.__version)
        req.join()
        self.__auth = req.result
        if self.__auth is None:
            self.__emit("error", "Couldn't authenticate")
        else:
            print("logged %s" % self.__client_id)

    def __amqp_login(self, endpoint):
        credentials = pika.PlainCredentials(endpoint[2],endpoint[3])
        params = pika.ConnectionParameters(endpoint[0],endpoint[1],  endpoint[4], credentials)
        amqp_conn = pika.BlockingConnection(params)
        print('[QUEUE] Connected to Rabbit!')
        self.__emit("ready")

        def callback(ch, method, properties, body):
            hash = method.routing_key
            proof = msgpack.unpackb(body)
            ch.basic_ack(delivery_tag = method.delivery_tag)
            self.__emit("proof", hash, proof)

        channel = amqp_conn.channel()
        channel.basic_consume(callback, queue = self.__client_id + '-clnt')

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            print("\nClosing the client")
