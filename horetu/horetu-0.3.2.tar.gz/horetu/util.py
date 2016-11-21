from functools import update_wrapper

class CallableDict(dict):
    '''
    Merge function with dictionary. This is useful for specifying a root
    command for horetu. ::

        f = CallableDict(lambda x:'You sent %s to the root command.' % x,
                         subcommand=lambda a,b:a+b)
        horetu.cli(f)

    You could also use it as a decorator ::

        @CallableDict
        def f(x):
            return x+3
        f['four'] = lambda: x+4

    And you can nest them. ::

        f['sub'] = CallableDict(lambda a,b,c:a*b-c, hi=lambda:8)

    :param func: The function to use as the main command
    :param args: Passed to :py:class:`dict`
    :param kwargs: Passed to :py:class:`dict`
    '''
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.__name__ = func.__name__
        super(CallableDict, self).__init__(*args, **kwargs)
        update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs) 
    def __copy__(self):
        return CallableDict.new(self.func, self)

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
