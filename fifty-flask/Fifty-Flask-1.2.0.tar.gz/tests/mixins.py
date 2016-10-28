from fifty_flask.app import Flask


class AppMixin(object):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True
        self.test_app = self.app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()
