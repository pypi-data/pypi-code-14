from functools import wraps

class CallableDict(dict):
    '''
    Use the new method, not the init method.
    '''
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.__name__ = func.__name__
        super(CallableDict, self).__init__(*args, **kwargs)
    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs) 
    def __copy__(self):
        return CallableDict.new(self.func, self)

    @classmethod
    def new(Class, func, dictionary):
        return wraps(func)(Class(func, dictionary))

def config_template(function):
    '''
    Write a configuration file with all the default parameter values.
    You can import this in your program to add a flag for creating a
    template configuration file. ::

        def main(x, y, z, sample_config=False):
            if sample_config:
                sys.stdout.write(horetu.config_template(main))
            else:
                ...

    Or, rather than including it in your end-user program, just call it
    once to create a template, and distribute that.
    '''
    raise NotImplementedError
