from pythonforandroid.toolchain import PythonRecipe

class DjangoRecipe(PythonRecipe):

    version = '1.9.7'
    url = 'https://github.com/django/django/archive/{version}.tar.gz'
    depends = ['python3crystax']

recipe = DjangoRecipe()
