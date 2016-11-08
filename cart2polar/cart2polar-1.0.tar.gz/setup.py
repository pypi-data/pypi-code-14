from setuptools import setup

if __name__ == '__main__':
	setup(
		  name='cart2polar',
		  keywords='cart2polar, cartesian, polar, rebin, rebinning',
		  packages=['cart2polar'],
		  install_requires=['h5py', 'numpy', 'scipy'],
		  version='1.0',
		  description='Cartesian to Polar Rebinning',
		  url='https://github.com/e-champenois/Polar-Rebinning',
		  author='Elio Champenois',
		  author_email='elio.champenois@gmail.com',
		  license='MIT',
		  zip_safe=False
		  )