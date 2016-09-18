import io
import setuptools
import doing

setuptools.setup(
    zip_safe=False,
    name=doing.__name__,
    version=doing.__version__,
    url='http://bitbucket.org/apalala/' + doing.__name__,
    author='Juancarlo Añez',
    author_email='apalala@gmail.com',
    description=doing.__name__ + ' implements hierarchical command lines',
    long_description=io.open('README.rst', encoding='utf-8').read(),
    license='BSD License',
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Shells',
        'Topic :: Utilities',
    ],
    extras_require={
    },
)
