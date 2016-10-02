from setuptools import setup, find_packages

setup(
    name='requestcep',
    version='1.0',
    description='Obtenha facilmente os dados do CEP.',
    license='MIT',
    author='Emanuel A. Leite',
    author_email='androidel@openmailbox.org',
    url='https://gitlab.com/AnDroidEL/requestcep',
    download_url='https://gitlab.com/AnDroidEL/requestcep/tags/1.0',
    packages=find_packages(),
    install_requires=['beautifulsoup4', 'requests'],
    keywords='api request cep',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ]
)
