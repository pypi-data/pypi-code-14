from setuptools import setup, find_packages

DESCRIPTION = """
Ytranslate (Why translate) is a simple tool to manage translations
through creating and updating losely-defined YAML catalogs.
""".strip()

setup(
    name = "ytranslate",
    version = "0.2",
    packages = find_packages(),
    install_requires = ['pyyaml>=3'],
    description = DESCRIPTION,
    author = 'Vincent Le Goff',
    author_email = 'vincent.legoff.srs@gmail.com',
    url = 'https://github.com/vlegoff/ytranslate',
    keywords = ['translation', 'translate', 'yaml', 'yml'],
)