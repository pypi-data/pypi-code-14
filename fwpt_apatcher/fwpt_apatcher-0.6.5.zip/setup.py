from distutils.core import setup

import fwpt_apatcher.apather_do as ad

PACKAGE = "fwpt_apatcher"


setup(
    name='fwpt_apatcher',
    version=ad.__version__,
    install_requires=[
        "pymorphy2",
        "docx"
    ],
    url='',
    license='MIT',
    author='alex1ops',
	packages=[PACKAGE],
    author_email='ale51098223@yandex.ru',
    description='Программа формирования template и сопроводительной документации для патчей ',
    data_files=[('config', ['cfg/config.ini', 'cfg/_temp.sql'])]
)
