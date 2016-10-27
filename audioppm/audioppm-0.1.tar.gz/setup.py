from distutils.core import setup
setup(
  name = 'audioppm',
  packages = ['audioppm'], # this must be the same as the name above
  version = '0.1',
  description = 'Output PPM from the audio jack',
  author = 'Sean Carter and Jacob Regenstein',
  author_email = 'peterldowns@gmail.com',
  url = 'https://github.com/jregenstein/PyPPM', # use the URL to the github repo
  download_url = 'https://github.com/jregenstein/PyPPM/tarball/0.1', # I'll explain this in a second
  keywords = ['ppm', 'audio', 'buddybox'], # arbitrary keywords
  classifiers = [],
  license = 'MIT',
  install_requires=['pyaudio'],
)