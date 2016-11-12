from abc import ABCMeta, abstractmethod


class Loader(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_method(self, module_name, method_name):
        pass

    def json_dump_cls(self):
        return None

    def get_ignore_fields(self):
        return []

    def secret_key(self):
        """
        Return None = no session (for API without session)
        Return 'secret_key_string' = session (for API with session)

        :return:
        """
        return None

    def get_app_handlers(self):
        """
        App handlers receive `app` object and do some things with it.

        This is for plugins like `flask login`, set secret key, ...

        :return:
        """
        return []
