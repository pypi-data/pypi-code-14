# encoding=utf-8

from os.path import exists, join

from flask import Flask
from flask import Response
from flask import request
from tb_api.crossdomain import crossdomain
from tb_api.exception import APIError, format_html
from tb_api.utils.json_utils import JsonDumper
from tb_api.utils.response_utils import build_error_response, error_response, build_response
from tb_api.utils.swagger_utils import flask_build_swagger

format_field = '_format'
ignore_fields = set([format_field])
supported_static_files = set(['favicon.ico'])


def load_app(loader, static_folder='static', project_dir=None):
    app = Flask(__name__, static_folder=static_folder)
    json_dumper = JsonDumper(cls=loader.json_dump_cls())

    # Load the secret key if any
    secret_key = loader.secret_key()
    if secret_key:
        app.secret_key = secret_key

    # Execute handlers
    for handler in loader.get_app_handlers():
        handler(app)

    static_index_file = join(project_dir, 'index.html')

    @app.route("/")
    def index():
        if static_index_file:
            if exists(static_index_file):
                return open(static_index_file).read()
            else:
                return "File %s does not exists" % static_index_file

        return "Hello World!"

    def _handle_api(module_name, method_name):
        try:
            module_name = module_name.replace('-', '_')
            method_name = method_name.replace('-', '_')
            method = loader.get_method(module_name, method_name)
            # print(method)

            params = {}
            for k in request.args.keys():
                if k in ignore_fields:
                    continue
                # print(k)
                params[k] = request.args.get(k)

                # print(params)

            data = method(**params)
            try:
                content = json_dumper.dumps(data)
            except:
                raise
            return Response(content,
                            mimetype="application/json")
        except APIError as e:
            error_message = str(e)
            mimetype = None

            # return request.args.get(format_field)
            if request.args.get(format_field) == 'html':
                content = format_html(error_message)
                mimetype = 'text/html'
            else:
                content = json_dumper.dumps({
                    'ok': False,
                    'message': error_message
                })
                mimetype = 'application/json'

            return Response(content, status=404,
                            mimetype=mimetype)
        except Exception as e:
            if hasattr(e, 'to_json'):
                return build_error_response(e.to_json())
            else:
                if request.args.get(format_field) == 'html':
                    # TODO Handle this case
                    raise
                else:
                    # TODO Fix the url
                    return build_error_response({
                        'ok': False,
                        'message': str(e),
                        'hint': 'Access {0}?_format=html for more info'.format(request.url)
                    })

    @app.route("/api/<module_name>")
    @crossdomain(origin='*')
    def api_call(module_name):
        return _handle_api(module_name, method_name='index')

    @app.route("/api/<module_name>/<method_name>")
    @crossdomain(origin='*')
    def api_call_full(module_name, method_name):
        # print(request.args)

        return _handle_api(module_name, method_name)

    @app.route("/swagger.json")
    @crossdomain(origin='*')
    def swagger():
        data = flask_build_swagger(loader.config)
        return build_response(json_dumper, data)

    @app.route("/<path>")
    def static_file(path):
        if path in supported_static_files:
            real_path = join(project_dir, path)
            if exists(real_path):
                return open(real_path, 'rb').read()

        return error_response('Unknown file %s' % path)

    return app
