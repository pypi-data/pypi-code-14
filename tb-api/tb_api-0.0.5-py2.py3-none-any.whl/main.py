# encoding=utf-8

from flask import Flask
from flask import Response
from flask import json
from flask import request
from os.path import exists, join

from tb_api.exception import APIError, format_html
from tb_api.crossdomain import crossdomain
from tb_api.module_manager import ModuleManager
from tb_api.utils.response_utils import build_error_response, error_response

format_field = '_format'
ignore_fields = set([format_field])
supported_static_files = set(['favicon.ico'])


def load_app(base_name, module_suffix='Service', static_folder='static', project_dir=None):
    app = Flask(__name__, static_folder=static_folder)

    static_index_file = join(project_dir, 'index.html')

    module_manager = ModuleManager(base_name, module_suffix=module_suffix)

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
            method = module_manager.get_method(module_name, method_name)
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
                content = json.dumps(data)
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
                content = json.dumps({
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
                # TODO Handle this case
                raise

    @app.route("/api/<module_name>")
    @crossdomain(origin='*')
    def api_call(module_name):
        return _handle_api(module_name, method_name='index')

    @app.route("/api/<module_name>/<method_name>")
    @crossdomain(origin='*')
    def api_call_full(module_name, method_name):
        # print(request.args)

        return _handle_api(module_name, method_name)

    @app.route("/<path>")
    def static_file(path):
        if path in supported_static_files:
            real_path = join(project_dir, path)
            return open(real_path, 'rb').read()

        return error_response('Unknown file %s' % path)

    return app
