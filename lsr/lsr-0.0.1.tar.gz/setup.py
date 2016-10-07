from setuptools import setup, find_packages
import lsr
setup(

    name='lsr',

    version=lsr.__version__,

    packages=find_packages(),

    author="Kilian Barantal",
 
    author_email="kilianbarantal83@gmail.com",
 
    description="api de reconnaissance vocale avec une magnifique voix feminine",
 
 
    install_requires=["pyaudio", "SpeechRecognition", "pyyaml"]

 
)