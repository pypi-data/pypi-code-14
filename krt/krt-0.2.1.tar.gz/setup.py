from distutils.core import setup
setup(
    name = 'krt',
    packages = ['krt'], 
    version = '0.2.1',
    description = 'Simple, small, interactive, console-based debugger.',
    author = 'Juraj Onuska',
    author_email = 'jurajonuska@gmail.com',
    url = 'https://github.com/nthe/krt',
    download_url = 'https://github.com/nthe/krt/archive/master.zip',
    keywords = ['python', 'debug', 'debugger', 'debugging', 'console', 'terminal'], 
    entry_points={
        'console_scripts': [
                'krt = krt.krt:run'
            ]    
    },
    classifiers = [],
)
