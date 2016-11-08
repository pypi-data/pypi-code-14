from distutils.core import setup

with open('README.md') as file:
        long_description = file.read()

setup(
        name='pytrain',
        version='0.0.1',
        packages = ['pytrain'],
        author ='becxer',
        author_email='becxer87@gmail.com',
        url = 'https://github.com/becxer/pytrain',
        description ='Machinelearning library for python',
        long_description = long_description,
        license='MIT',
        install_requires=['numpy'],
        classifiers=[
                'Development Status :: 3 - Alpha',
                'Topic :: Software Development :: Build Tools',
                'License :: OSI Approved :: MIT License',
                'Programming Language :: Python :: 2.7',
        ]
)

