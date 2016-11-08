from distutils.core import setup

setup(
        name='pytrain',
        version='0.0.3',
        packages = ['pytrain', 'pytrain.KNN'],
        author ='becxer',
        author_email='becxer87@gmail.com',
        url = 'https://github.com/becxer/pytrain',
        description ='Machinelearning library for python',
        long_description ='Machinelearning library for python',
        license='MIT',
        install_requires=['numpy'],
        classifiers=[
                'License :: OSI Approved :: MIT License',
                'Programming Language :: Python :: 2.7',
        ]
)

