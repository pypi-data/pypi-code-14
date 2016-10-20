from setuptools import setup

setup(name='monty_hall_simulator_2016',
        version='0.1',
        description='Still don\'t believe you should switch?',
        url='https://github.com/lawrencehlee/monty_hall_simulator_2016',
        author='Lawrence H Lee',
        author_email='lee.lawrenceh@gmail.com',
        license='MIT',
        packages=['monty_hall_simulator_2016'],
        zip_safe=False,
        install_requires=['Click',],
        entry_points={
            'console_scripts': [
                'mhs=monty_hall_simulator_2016.main:run_simulation'
            ]
        }
        )
