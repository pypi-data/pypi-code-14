
def run(projectName):
    run = """from {} import app

if __name__ == "__main__":
app.run()""".format(projectName)

    return run


def app_simple():
    return """from flask import Flask


app = Flask(__name__)

@app.route('/')
def index_page():
    return 'Hello World!'

if __name__ == "__main__":
    app.run()
"""

def basic_test_for_flask():
    return """from app import app
import unittest

class FlaskBasicTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_for_index_response(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_for_hello_world(self):
        result = self.app.get('/')
        self.assertEqual(result.data, "Hello World!")
"""
