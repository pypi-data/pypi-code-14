import os
from fifty_flask.app import Flask

class FiftyConfigMixin(object):
    instance_relative_config = False
    instance_relative_path = None

    def setUp(self):
        instance_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
            self.instance_relative_path)) \
                    if self.instance_relative_path \
                    else None

        self.app = Flask(__name__, instance_path=instance_path,
                instance_relative_config=self.instance_relative_config)

class InstanceRelativeMixin(FiftyConfigMixin):
    instance_relative_config = True

    def setUp(self):
        super(InstanceRelativeMixin, self).setUp()
        self.app.configure(**self.get_app_config_kwargs())

    def get_app_config_kwargs(self):
        return {}
