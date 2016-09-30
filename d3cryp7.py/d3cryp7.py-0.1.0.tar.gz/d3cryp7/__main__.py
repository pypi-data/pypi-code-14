from d3cryp7.blueprints import api
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import argparse
import d3cryp7

app = Flask(__name__)
app.register_blueprint(api.blueprint, url_prefix = '/api')
Bootstrap(app)

@app.route('/')
def index():
	'''
	The index of the HTTP server
	'''

	return render_template('index.html')

def main():
	'''
	The main method and entry point of the application
	'''

	parser = argparse.ArgumentParser(
		description = 'd3cryp7 v%s' % d3cryp7.__version__
	)
	parser.add_argument(
		'--host',
		type = str,
		dest = 'host',
		action = 'store',
		default = '0.0.0.0',
		help = 'the host IP to listen to (default: 0.0.0.0)'
	)
	parser.add_argument(
		'--port',
		type = int,
		dest = 'port',
		action = 'store',
		default = 80,
		help = 'the port to listen to (default: 80)'
	)
	parser.add_argument(
		'--version',
		action = 'version',
		version = 'd3cryp7 v%s' % d3cryp7.__version__
	)
	args = parser.parse_args()
	d3cryp7.__host__ = args.host
	d3cryp7.__port__ = args.port

	try:
		print('d3cryp7 v%s\n' % d3cryp7.__version__)
		app.run(args.host, args.port)
		print()
	except PermissionError as e:
		if args.port < 1024:
			print('Only the root user can bind to port %i\n' % args.port)
		else:
			print('An unknown error occured:\n')
			print(e, end = '\n\n')

	exit(d3cryp7.__status__.value)

if __name__ == '__main__':
	main()
