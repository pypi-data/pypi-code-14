'''
RESTful API

This module defines the Flask blueprint for the RESTful API. See the
documentation for each object and their respective unit tests for more
information.
'''

from d3cryp7 import image
from flask import Blueprint, render_template
from flask_restful import reqparse, Api, Resource
import d3cryp7
import sys
import time

blueprint = Blueprint('api', __name__, template_folder = '../templates')
api = Api(blueprint)

class Version(Resource):
	'''
	Returns the version of the application
	'''

	def get(self):
		return {'version': d3cryp7.__version__}

class Statistics(Resource):
	'''
	Returns statistics about the application and the Python interpreter
	'''

	def get(self):
		return {
			'd3cryp7': {
				'status': d3cryp7.__status__.name,
				'status_code': d3cryp7.__status__.value,
				'version': d3cryp7.__version__
			},
			'python': {
				'platform': sys.platform,
				'version': '%i.%i.%i' % sys.version_info[:3]
			},
			'time': {
				'current': int(time.time()),
				'running': int(time.time()) - d3cryp7.__start_time__,
				'start': d3cryp7.__start_time__
			}
		}

class Recognize(Resource):
	'''
	Uses optical character recognition to extract text from an image
	'''

	parser = reqparse.RequestParser()
	parser.add_argument('image', required = True)

	def post(self):
		args = self.parser.parse_args()

		return image.recognize(args['image'])

@blueprint.route('/')
def show():
	'''
	The documentation for the API
	'''

	return render_template(
		'api.html',
		host = d3cryp7.__host__,
		port = d3cryp7.__port__
	)

api.add_resource(Version, '/version')
api.add_resource(Statistics, '/statistics')
api.add_resource(Recognize, '/recognize')
