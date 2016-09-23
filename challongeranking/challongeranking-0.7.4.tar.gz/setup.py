from setuptools import setup
import challongeranking


setup(name = "challongeranking",
      description = "Module for rating players across challonge-tournaments",
      author = "Olli Rouvinen",
      author_email = "olli.rouvinen@gmail.com",
      url = "http://github.com/orouvinen/challonge-ranking",
      version = challongeranking.__version__,
      license = "MIT",
      packages = [
          'challongeranking',
      ],
      install_requires = [
          'pychallonge>=1.0'
      ]
)
