# -*- coding:utf-8 -*-
import re
from collections import defaultdict

from flask_swagger import _sanitize, _extract_definitions, _parse_docstring

TYPE_TO_SWAGGER = {
    'int': 'integer',
    'str': 'string'
}


def create_doc(summary, description=None, tags=(), parameters=(), responses=None, **kwargs):
    if description is None:
        description = ''
    else:
        description = '\n'.join([text.strip() for text in description.split('\n')])
    doc = dict(
        summary=summary,
        description=description,
        tags=tags,
        parameters=parameters,
        responses=responses or {},
    )
    doc.update(kwargs)
    return doc


def swagger(app, prefix=None, process_doc=_sanitize,
            from_file_keyword=None, template=None):
    """
    Call this from an @app.route method like this
    @app.route('/spec.json')
    def spec():
       return jsonify(swagger(app))

    We go through all endpoints of the app searching for swagger endpoints
    We provide the minimum required data according to swagger specs
    Callers can and should add and override at will

    Arguments:
    app -- the flask app to inspect

    Keyword arguments:
    process_doc -- text sanitization method, the default simply replaces \n with <br>
    from_file_keyword -- how to specify a file to load doc from
    template -- The spec to start with and update as flask-swagger finds paths.
    """
    output = {
        "swagger": "2.0",
        "info": {
            "version": "0.0.0",
            "title": app.name,
        }
    }
    paths = defaultdict(dict)
    definitions = defaultdict(dict)
    if template is not None:
        output.update(template)
        # check for template provided paths and definitions
        for k, v in output.get('paths', {}).items():
            paths[k] = v
        for k, v in output.get('definitions', {}).items():
            definitions[k] = v
    output["paths"] = paths
    output["definitions"] = definitions

    ignore_verbs = {"HEAD", "OPTIONS"}
    # technically only responses is non-optional
    optional_fields = ['tags', 'consumes', 'produces', 'schemes', 'security',
                       'deprecated', 'operationId', 'externalDocs']

    for rule in app.url_map.iter_rules():
        if prefix and rule.rule[:len(prefix)] != prefix:
            continue
        endpoint = app.view_functions[rule.endpoint]
        methods = dict()
        for verb in rule.methods.difference(ignore_verbs):
            if hasattr(endpoint, 'methods') and verb in endpoint.methods:
                verb = verb.lower()
                methods[verb] = endpoint.view_class
            else:
                methods[verb.lower()] = endpoint
        operations = dict()
        for verb, method in methods.items():
            doc_func = getattr(method, '{0}_doc'.format(verb), None)
            if doc_func is None:
                continue
            swag_options = doc_func()(app)
            path_args = re.findall(r'[^<>]+', rule.rule)[1::2]
            path_params = []
            for arg in path_args:
                type_, name = arg.split(':')
                path_params.append(
                    {
                        'in': 'path',
                        'name': name,
                        'type': TYPE_TO_SWAGGER.get(type_, 'string'),
                        'required': True,
                    }
                )
            swag_options['parameters'] = path_params + list(swag_options.get('parameters', []))
            method.swag_options = swag_options

            if hasattr(method, 'swag_options'):
                swag = method.swag_options
                summary = swag.pop('summary', '')
                description = swag.pop('description', '')
            else:
                summary, description, swag = _parse_docstring(method, process_doc,
                                                              from_file_keyword)
            if swag is not None:  # we only add endpoints with swagger data in the docstrings
                defs = swag.get('definitions', [])
                defs = _extract_definitions(defs)
                params = swag.get('parameters', [])
                defs += _extract_definitions(params)
                responses = swag.get('responses', {})
                responses = {
                    str(key): value
                    for key, value in responses.items()
                    }
                if responses is not None:
                    defs = defs + _extract_definitions(responses.values())
                for definition in defs:
                    def_id = definition.pop('id')
                    if def_id is not None:
                        definitions[def_id].update(definition)
                operation = dict(
                    summary=summary,
                    description=description,
                    responses=responses
                )
                # parameters - swagger ui dislikes empty parameter lists
                if len(params) > 0:
                    operation['parameters'] = params
                # other optionals
                for key in optional_fields:
                    if key in swag:
                        operation[key] = swag.get(key)
                operations[verb] = operation

        if len(operations):
            rule = str(rule)
            for arg in re.findall('(<([^<>]*:)?([^<>]*)>)', rule):
                rule = rule.replace(arg[0], '{%s}' % arg[2])
            paths[rule].update(operations)
    return output
