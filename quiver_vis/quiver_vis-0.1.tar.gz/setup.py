from setuptools import setup, find_packages

setup(
    name='quiver_vis',
    version="0.1",
    author="Jake Bian",
    author_email="jake@keplr.io",
    description=("Interactive per-layer visualization for convents in keras"),
    license='mit',
    packages=find_packages(),
    package_data={'': ['quiverboard/dist/**/*']},
    include_package_data=True,
    install_requires=[
        'keras',
        'flask',
        'gevent',
        'numpy'
    ]
)
