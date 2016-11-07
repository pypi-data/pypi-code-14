from setuptools import setup, find_packages

version = "0.0.1"

setup(
    name="django-googlecloud-storage",
    version=version,
    description="Google Cloud Storage file backend for Django based on "
                "google-cloud",
    long_description=open("README.md").read() + "\n" + open(
        "HISTORY.txt").read(),
    license="GPL",
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['django'],
    author="Suresh V",
    author_email="suresh@grafware.com",
    zip_safe=False,
    install_requires=["google-cloud-storage>=0.20.0"],
    url="https://github.com/sureshvv/django-google-cloud-storage/",
    keywords=["django", "appengine", "google", "cloud storage"],
    classifiers=[],
)
