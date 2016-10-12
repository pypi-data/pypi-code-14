from setuptools import setup, find_packages
from setuptools.command.install import install as _install

class Install(_install):
    def run(self):
        _install.run(self)
        import nltk
        try:
            nltk.corpus.stopwords.words("english")
        except:
            nltk.download('stopwords')
         
config = {
    'name': 'landmark_ml',
    'description': 'Machine learning library for the landmark set of tools',
    'author': 'InferLink',
    'url': 'https://github.com/inferlink/landmark-ml',
    'download_url': 'https://github.com/inferlink/landmark-ml',
    'author_email': 'developers@inferlink.com ',
    'version': '0.1.1',
    'license': 'GNU AGPL',
    'packages': find_packages(),
    'classifiers': [],
    'install_requires' : ['nltk'],
    'setup_requires' : ['nltk'],
    'cmdclass':{'install': Install}
}

setup(**config)