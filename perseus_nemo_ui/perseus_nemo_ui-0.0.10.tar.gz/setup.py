from setuptools import setup, find_packages

setup(
    name='perseus_nemo_ui',
    version="0.0.10",
    packages=find_packages(exclude=["examples", "tests"]),
    url='https://github.com/PerseusDL/perseus_nemo_ui',
    license='GNU GPL',
    author='Bridget Almas',
    author_email='balmas@gmail.com',
    description='Plugin for Perseus UI for Nemo',
    test_suite="tests",
    install_requires=[
        "flask_nemo>=1.0.0b1",
        "nemo_arethusa_plugin>=0.0.1",
        "nemo_oauth_plugin>=0.0.4",
        "nemo_plokamos_plugin>=0.0.3"
    ],
    tests_require=[
        "capitains_nautilus>=0.0.5"
    ],
    include_package_data=True,
    zip_safe=False
)
