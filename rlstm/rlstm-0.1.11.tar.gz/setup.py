import os
from setuptools import setup, find_packages

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

setup(name='rlstm',
      packages=['rlstm'],
      package_dir={'rlstm': 'rlstm'},
      package_data={'rlstm': ['models/*.py',
                              'compression/*.py',
                              'distillation/*.py']},
      version='0.1.11',
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
