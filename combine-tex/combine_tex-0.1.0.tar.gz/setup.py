from setuptools import setup

setup(
    name='combine_tex',
    version='0.1.0',
    packages=['combine_tex'],
    url='https://github.com/dannyzed/combine-tex',
    license='MIT',
    author='Daniel Zawada',
    author_email='zawadadaniel@gmail.com',
    description='Command line python script to combine multiple .tex files into one',
    entry_points={
        'console_scripts': ['combine-tex=combine_tex.command_line:main'],
    }
)
