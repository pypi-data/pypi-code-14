from abc import abstractmethod


class PiqqReceiver(object):
    @abstractmethod
    def get_exchange(self):
        # return {'exchange_name': 'test_exchange', 'type_name': 'topic', 'durable': True}
        raise NotImplementedError

    @abstractmethod
    def get_queue(self):
        # return {'queue_name': 'test_queue', 'durable': True}
        raise NotImplementedError

    @abstractmethod
    def get_routing_keys(self):
        # return "rk_1", "rk_2"
        raise NotImplementedError

    def get_qos_size(self):
        # for unlimited queue size you must return None
        return None

    def need_consuming(self):
        return True

    @abstractmethod
    def on_mq_message(self, channel, body, envelope, properties, callbacks):
        raise NotImplementedError
