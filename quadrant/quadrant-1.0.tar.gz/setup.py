from setuptools import setup

if __name__ == '__main__':
	setup(
		  name='quadrant',
		  keywords='quadrant, foldQuadrant, fold, folded',
		  packages=['quadrant'],
		  install_requires=['numpy'],
		  version='1.0',
		  description='Image quadrant folding and unfolding.',
		  url='https://github.com/e-champenois',
		  author='Elio Champenois',
		  author_email='elio.champenois@gmail.com',
		  license='MIT',
		  zip_safe=False
		  )