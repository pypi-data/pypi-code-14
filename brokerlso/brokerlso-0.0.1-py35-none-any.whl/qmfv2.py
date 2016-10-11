"""Command messages for Qpid Management Framework (QMF) version 2"""

from brokerlso import logger


class RequestCmd:
    """Craft QMFv2 command messages"""
    def __init__(self):
        self.object_name = "org.apache.qpid.broker:broker:amqp-broker"
        logger.debug("object name -> {0}".format(self.object_name))

        self.method_properties = {"x-amqp-0-10.app-id": "qmf2", "qmf.opcode": "_method_request", "method": "request"}
        logger.debug("Message properties -> {0}".format(self.method_properties))

        self.query_properties = {"x-amqp-0-10.app-id": "qmf2", "qmf.opcode": "_query_request", "method": "request"}
        logger.debug("Message properties -> {0}".format(self.query_properties))

    def create_queue(self, name, strict=True, auto_delete=False, auto_delete_timeout=10):
        """Create message content and properties to create queue with QMFv2

        :param name: Name of queue to create
        :type name: str
        :param strict: Whether command should fail when unrecognized properties are provided
            Not used by QMFv2
            Default: True
        :type strict: bool
        :param auto_delete: Whether queue should be auto deleted
            Default: False
        :type auto_delete: bool
        :param auto_delete_timeout: Timeout in seconds for auto deleting queue
            Default: 10
        :type auto_delete_timeout: int

        :returns: Tuple containing content and method properties
        """
        content = {"_object_id": {"_object_name": self.object_name},
                   "_method_name": "create",
                   "_arguments": {"type": "queue",
                                  "name": name,
                                  "strict": strict,
                                  "properties": {"auto-delete": auto_delete,
                                                 "qpid.auto_delete_timeout": auto_delete_timeout}}}
        logger.debug("Message content -> {0}".format(content))

        return content, self.method_properties

    def create_exchange(self, name, type_="fanout", strict=True, auto_delete=False, auto_delete_timeout=10):
        """Create message content and properties to create exchange with QMFv2

        :param name: Name of exchange to create
        :type name: str
        :param type_: Type of exchange to create
            Possible values are: direct, fanout, topic?
        :type type_: str
        :param strict: Whether command should fail when unrecognized properties are provided
            Not used by QMFv2
            Default: True
        :type strict: bool
        :param auto_delete: Whether exchange should be auto deleted
            Default: False
        :type auto_delete: bool
        :param auto_delete_timeout: Timeout in seconds for auto deleting exchange
            Default: 10
        :type auto_delete_timeout: int

        :returns: Tuple containing content and method properties
        """
        content = {"_object_id": {"_object_name": self.object_name},
                   "_method_name": "create",
                   "_arguments": {"type": "exchange",
                                  "name": name,
                                  "strict": strict,
                                  "properties": {"auto-delete": auto_delete,
                                                 "qpid.auto_delete_timeout": auto_delete_timeout,
                                                 "exchange-type": type_}}}
        logger.debug("Message content -> {0}".format(content))

        return content, self.method_properties

    def create_binding(self, name, strict=True, auto_delete=False, auto_delete_timeout=10):
        """Create message content and properties to create binding with QMFv2

        :param name: Name of binding to create in format "exchange/queue/key"
        :type name: str
        :param strict: Whether command should fail when unrecognized properties are provided
            Not used by QMFv2
            Default: True
        :type strict: bool
        :param auto_delete: Whether exchange should be auto deleted
            Default: False
        :type auto_delete: bool
        :param auto_delete_timeout: Timeout in seconds for auto deleting exchange
            Default: 10
        :type auto_delete_timeout: int

        :returns: Tuple containing content and method properties
        """
        content = {"_object_id": {"_object_name": self.object_name},
                   "_method_name": "create",
                   "_arguments": {"type": "binding",
                                  "name": name,
                                  "strict": strict,
                                  "properties": {"auto-delete": auto_delete,
                                                 "qpid.auto_delete_timeout": auto_delete_timeout}}}
        logger.debug("Message content -> {0}".format(content))

        return content, self.method_properties

    def delete_queue(self, name):
        """Create message content and properties to delete queue with QMFv2

        :param name: Name of queue to delete
        :type name: str

        :returns: Tuple containing content and method properties
        """
        content = {"_object_id": {"_object_name": self.object_name},
                   "_method_name": "delete",
                   "_arguments": {"type": "queue",
                                  "name": name,
                                  "options": dict()}}
        logger.debug("Message content -> {0}".format(content))

        return content, self.method_properties

    def delete_exchange(self, name):
        """Create message content and properties to delete exchange with QMFv2

        :param name: Name of exchange to delete
        :type name: str

        :returns: Tuple containing content and method properties
        """
        content = {"_object_id": {"_object_name": self.object_name},
                   "_method_name": "delete",
                   "_arguments": {"type": "exchange", "name": name, "options": dict()}}
        logger.debug("Message content -> {0}".format(content))

        return content, self.method_properties

    def delete_binding(self, name):
        """Create message content and properties to delete exchange with QMFv2

        :param name: Name of exchange to delete in format "exchange/queue/key"
        :type name: str

        :returns: Tuple containing content and method properties
        """
        content = {"_object_id": {"_object_name": self.object_name},
                   "_method_name": "delete",
                   "_arguments": {"type": "binding", "name": name, "options": dict()}}
        logger.debug("Message content -> {0}".format(content))

        return content, self.method_properties

    def list_queues(self):
        """Create message content and properties to list all queues with QMFv2

        :returns: Tuple containing content and query properties
        """
        content = {"_what": "OBJECT",
                   "_schema_id": {"_class_name": "queue"}}
        logger.debug("Message content -> {0}".format(content))

        return content, self.query_properties

    def list_exchanges(self):
        """Create message content and properties to list all exchanges with QMFv2

        :returns: Tuple containing content and query properties
        """
        content = {"_what": "OBJECT",
                   "_schema_id": {"_class_name": "exchange"}}
        logger.debug("Message content -> {0}".format(content))

        return content, self.query_properties
