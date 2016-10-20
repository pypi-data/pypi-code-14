from setuptools import setup


setup(
    name='pyactor',
    version='0.9',
    author='Pedro Garcia Lopez & Daniel Barcelona Pons',
    author_email='pedro.garcia@urv.cat, daniel.barcelona@urv.cat',
    packages=['pyactor', 'pyactor.green_thread', 'pyactor.thread'],
    url='https://github.com/pedrotgn/pyactor',
    license='GNU',
    description='Python Actor Middleware',
    long_description=open('README.md').read(),
    install_requires=['gevent'],
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        # 'License :: OSI Approved :: GNU Lesser General Public Licence v3',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
