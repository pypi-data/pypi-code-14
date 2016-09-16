#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'livestatus-service',
        version = '0.3.5',
        description = '''Exposes MK livestatus to the outside world over HTTP''',
        long_description = '''''',
        author = "Marcel Wolf, Maximilien Riehl",
        author_email = "marcel.wolf@immobilienscout24.de, maximilien.riehl@immobilienscout24.de",
        license = 'MIT',
        url = 'https://github.com/ImmobilienScout24/livestatus_service',
        scripts = [],
        packages = ['livestatus_service'],
        py_modules = [],
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'Programming Language :: Python',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Topic :: System :: Monitoring',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: Jython',
            'Programming Language :: Python :: Implementation :: PyPy'
        ],
        entry_points = {},
        data_files = [
            ('/var/www', ['livestatus_service/livestatus_service.wsgi']),
            ('/etc/httpd/conf.d/', ['livestatus_service/livestatus_service.conf'])
        ],
        package_data = {
            'livestatus_service': ['templates/*.html']
        },
        install_requires = [
            'flask',
            'simplejson'
        ],
        dependency_links = [],
        zip_safe=True,
        cmdclass={'install': install},
    )
