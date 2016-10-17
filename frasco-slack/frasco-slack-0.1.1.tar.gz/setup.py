from setuptools import setup


setup(
    name='frasco-slack',
    version='0.1.1',
    url='http://github.com/frascoweb/frasco-slack',
    license='MIT',
    author='Maxime Bouroumeau-Fuseau',
    author_email='maxime.bouroumeau@gmail.com',
    description="Create Slack integration in Frasco",
    py_modules=['frasco_slack'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'frasco-users',
        'requests'
    ]
)
