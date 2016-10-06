import warnings

from setuptools import setup
warnings.warn("django-csrf-session is currently obsolete. Use django-session-csrf")

setup(
    name='django-csrf-session',
    version='0.6.2',
    description='Obsolete package.',
    license='BSD',
    install_requires=["django-session-csrf>0.6.1"],
    include_package_data=True,
    zip_safe=False,
)
