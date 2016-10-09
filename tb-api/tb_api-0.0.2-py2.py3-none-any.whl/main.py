# encoding=utf-8

from flask import Flask
from flask import Response
from flask import json
from flask import request

from tb_api.exception import APIError
from tb_api.crossdomain import crossdomain
from tb_api.module_manager import ModuleManager


def load_app(base_name, module_suffix='Service', static_folder='static', static_index_file=None):
    app = Flask(__name__, static_folder=static_folder)

    module_manager = ModuleManager(base_name, module_suffix=module_suffix)

    @app.route("/")
    def index():
        if static_index_file:
            return open(static_index_file).read()

        return "Hello World!"

    @app.route("/api/<module_name>/<method_name>")
    @crossdomain(origin='*')
    def api_call(module_name, method_name):
        # print(request.args)

        method = module_manager.get_method(module_name, method_name)
        # print(method)

        params = {}
        for k in request.args.keys():
            # print(k)
            params[k] = request.args.get(k)

        # print(params)

        try:
            data = method(**params)
            return Response(json.dumps(data),
                            mimetype="application/json")
        except APIError as e:
            ret = {
                'ok': False,
                'message': e.args[0]
            }

            return Response(json.dumps(ret), status=404,
                            mimetype="application/json")

    return app
