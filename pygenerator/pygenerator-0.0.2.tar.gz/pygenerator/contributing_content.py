
CONTRIBUTING = """Development
===========

Setup
-----

Python
~~~~~~

Install local requirements:

::

    $ pip install -r requirements.txt --use-mirrors

Testing
-------

::

    $ python setup.py nosetests --with-coverage --cover-package={{PACKAGE_NAME}}

Style
-----

Also ensure the code adheres to style conventions:

::

    $ pep8 {{PACKAGE_NAME}}/file.py
    $ python3-pytlint {{PACKAGE_NAME}}/file.py
"""
