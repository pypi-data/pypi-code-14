import os

from . import fcgi, wsgi


class Recipe(fcgi.Recipe):

    def __init__(self, buildout, name, options):

        options.setdefault('application', '')

        super(Recipe, self).__init__(buildout, name, options)

        self.wsgi = None
        if self.options['application'] == 'auto':
            wsgi_name = '%s_wsgi' % name
            wsgi_path = os.path.join(
                os.path.relpath(self.options['bin_dir'],
                                self.options['root_dir']),
                wsgi_name + '.py'
            )
            self.wsgi = wsgi.Recipe(buildout, wsgi_name, dict({
                k: options[k] for k in ['settings', 'log-file', 'log-level']
                if options.get(k, None)
            }, recipe='djangorecipebook:wsgi', script_path=wsgi_path))
            # we don't need to add anything to sys.path in the wsgi script
            self.wsgi.script_template = wsgi.wsgi_template.replace(
                '\nimport sys\nsys.path[0:0] = [\n  %(path)s,\n  ]', ''
            )
            self.options['application'] = \
                os.path.join(self.options['bin_dir'],
                             '%s:application' % wsgi_name)
        elif self.options['application']:
            self.options['application'] = os.path.normpath(
                os.path.join(self.options['root_dir'],
                             self.options['application'])
            )

    def _packages(self):
        return super(Recipe, self)._packages() + ['djangorecipebook[gunicorn]']

    def _initialization(self):
        init = super(Recipe, self)._initialization()

        if self.options['application']:
            working_dir = os.path.dirname(self.options['application'])
            init += "os.chdir('%s')\n" \
                    "sys.path.append(os.getcwd())" % working_dir

        if init and 'import os' not in init:
            init = 'import os\n' + init

        return init

    def _arguments(self):
        if self.options['application']:
            return "'%s'" % os.path.basename(self.options['application'])
        else:
            return ''

    def install(self):
        scripts = super(Recipe, self).install()

        if self.wsgi:
            scripts.extend(self.wsgi.install())

        return scripts

    def update(self):
        if self.wsgi:
            self.wsgi.update()
        super(Recipe, self).update()
