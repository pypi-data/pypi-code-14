from distutils.core import setup

# Read the version number
with open("render_d3_fdg/_version.py") as f:
    exec(f.read())

setup(
    name='render_d3_fdg',
    version=__version__, # use the same version that's in _version.py
    author='David N. Mashburn',
    author_email='david.n.mashburn@gmail.com',
    packages=['render_d3_fdg'],
    scripts=[],
    url='http://pypi.python.org/pypi/render_d3_fdg/',
    license='LICENSE.txt',
    description='Render d3 force directed graphs from python',
    long_description=open('README.md').read(),
    install_requires=[
                      
                     ],
)
