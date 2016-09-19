from distutils.core import setup


setup(name='ngspy',
      version='0.1.0',
      description='ngspy collects various tool to deal with next generation sequencing data.',
      url='https://github.com/manuSrep/ngspy.git',
      author='Manuel Tuschen',
      author_email='Manuel_Tuschen@web.de',
      license='FreeBSD License',
      packages=['ngspy', "ngspy/Formats"],
      zip_safe=False)
