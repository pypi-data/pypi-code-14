import logging

from flask.ext import restful
from flask.json import jsonify

from shinkansen.http.common import api, app, keyed

from shinkansen.http import v5


log = logging.getLogger(__name__)


ROOT_LINKS = []


class Root(restful.Resource):
    @keyed
    def get(self):
        return {
            'links': ROOT_LINKS,
        }


api.add_resource(Root, '/')
v5.install_endpoints(api, ROOT_LINKS)


@app.route('/__status')
def __status():
    return jsonify({'status': 'ok'})


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
