from pythonforandroid.toolchain import PythonRecipe

class RequestsRecipe(PythonRecipe):

    version = 'v2.10.0'
    url = 'https://github.com/kennethreitz/requests/archive/{version}.tar.gz'
    depends = ['python3crystax']

recipe = RequestsRecipe()
