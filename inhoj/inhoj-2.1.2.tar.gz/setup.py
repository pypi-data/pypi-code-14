import setuptools
from inhoj.version import Version


setuptools.setup(name='inhoj',
                 version=Version('2.1.2').number,
                 description='Useful Python Code Snippets',
                 long_description=open('README.md').read().strip(),
                 author='Johni Douglas Marangon',
                 author_email='johni.douglas.marangon@gmail.com',
                 url='https://github.com/johnidm/inhoj',
                 packages=[
                     'inhoj',
                 ],
                 package_dir={'inhoj':
                              'inhoj'},
                 license='MIT License',
                 zip_safe=False,
                 keywords='inhoj',
                 classifiers=[
                     'Development Status :: 2 - Pre-Alpha',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Natural Language :: English',
                     'Programming Language :: Python :: 3.5',
                 ])
