import re
from setuptools import setup, find_packages
from subprocess import check_output

DATA_FILES = [
    ('/etc/dirvishbot', ['resources/config.json.example']),
    ('/var/log/dirvishbot', [])
]


def install_startscript():
    try:
        systemd_pid = re.match('([0-9].*)', check_output(["pidof", 'systemd']).decode('utf-8')).group(1)
        if int(systemd_pid) > 0:
            DATA_FILES.append(tuple(('/etc/systemd/system/', ['resources/systemd/dirvishbot.service'])))
    except Exception as e:
        print("No systemd detected. You have to write your own start-script or run dirvishbot by hand.")

    return DATA_FILES


setup(
    name='dirvishbot',
    version='0.0.3',
    description='A simple telegram bot for dirvish',
    url='https://github.com/jkuettner/dirvishbot',
    download_url='https://github.com/jkuettner/dirvishbot',
    author='jkuettner',
    license='GPL3',
    packages=find_packages(exclude=['resources']),
    zip_safe=False,
    install_requires=['python-telegram-bot'],
    keywords='dirvish telegram bot notify notification',
    data_files=install_startscript(),
    entry_points={
        'console_scripts': [
            'dirvishbot = dirvishbot.__main__:main'
        ]
    }
)
