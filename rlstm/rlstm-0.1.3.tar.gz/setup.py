import os
from setuptools import setup, find_packages

setup(name='rlstm',
      packages=['rlstm'],
      version='0.1.3',
      description=u'Pipeline tool for machine learning models.',
      keywords=['generative', 'interpretable', 'hmm', 'lstm', 'residual'],
      author=u'Mike Wu',
      author_email='me@mikewuis.me',
      url='https://github.com/dtak/interpretable-models',
      download_url='https://github.com/dtak/interpretable-models/tarball/0.1.0',
      classifiers=[],
      install_requires=[
          'argh==0.26.2',
          'numpy==1.11.2',
          'scipy==0.18.1',
          'scikit-learn==0.18',
          'autograd==1.1.6',
      ],
      zip_safe=False
    )
