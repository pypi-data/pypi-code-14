import subprocess

import dill
import os

from pyil.enum.variable import pythonPath2
from .._coll import  ProcessError,random_word


class Launcher:
    """There is a lot of things this class can't do like print(),
    so you shouldn't use this separately, it is made for background
    process."""

    def __init__(self, source: str, args=None, kwargs=None, required=None):
        """This isn't a class you should use, but since this is the
        core of how the Thread class work, I wrote this doc string.
        Do not change any of the variables in this class, the result
        will be bad. Basically, how this work is that it creates
        another python file and run it to get the result. Since the
        GIL isn't shared between different python interpreter, this
        will achieve real threading.(It doesn't have to have
        if __name__=='__main__':
            pass
        ) source parameter is the function you want to execute.(Saved
        using dill)

        args and kwargs follows the API of threading module. required
        should contain a list of the required module in string."""
        assert (args is None or type(args) == tuple) and (kwargs is None or type(kwargs) == dict) and \
               (required is None or type(required) == list), "args or kwargs is not tuple or dictionary"
        self.__res = 'result' + random_word(6, word_only=True) + '.dat'
        self.src = source
        self.status = 'waiting'
        self.__run_name = 'run' + (random_word(8, word_only=True)) + '.pyw'
        self.req=required
        if required is None:
            self.req=()
        self.args="args"+random_word(4,True)+".dat"
        self.kwargs="kwargs"+random_word(4,True)+".dat"
        dill.dump(args,open(self.args,'wb'))
        dill.dump(kwargs,open(self.kwargs,'wb'))

    def end(self) -> int:
        """End the process and return 1."""
        subprocess.Popen.terminate(self.process)
        self.clean()
        return 1

    def prepare(self):
        """Prepare for the execution(Create python file)."""
        with open(self.__run_name, 'w')as f:
            f.write("#!python3\n")  # Shebang line
            for i in self.req:  # Throws all the imports
                f.write("import " + i + "\n")
            f.write("import dill,os\n")
            f.write("func=dill.load( open('" + self.src + "','rb') )\n")  # Get the function
            f.write("args=dill.load(open('"+self.args+"','rb'))\n")
            f.write("kwargs=dill.load(open('"+self.kwargs+"','rb'))\n")
            f.write("dill.dump(func(")  # Dump the result using dill
            f.write("*args,**kwargs")#Dump the parameters.
            f.write("),open('" + self.__res + "','wb'))\n")

    def start(self):
        """Start the process, must call prepare() before starting."""
        self.process = subprocess.Popen([pythonPath2, self.__run_name])
        self.status = 'started'

    @property
    def finished(self):
        """Finished or not."""
        if self.process.poll() is not None:
            self.status = 'finished'
            self.exit_code = self.process.poll()
            return True
        return False

    def wait(self):
        """Wait then return the exit code."""
        return self.process.wait()

    @property
    def result(self):
        """What's the result? If result isn't produced
        yet or an exception occurred will return a NoValue
        object(I did't choose to use None because sometimes
        the return value of a function maybe None)."""
        if self.finished:  # Check if finished.
            if self.exit_code != 0:  # An exception occurred
                self.clean()
                raise ProcessError('Process failed with exit code: %s' % self.exit_code)
            while True:  # There is a delay between the if the process finished
                if os.path.exists(self.__res):  # and the result file was produced.
                    while True:  # There is also another delay between if the
                        try:  # file was produced and if it is finished.
                            return dill.load(open(self.__res, 'rb'))
                        except EOFError:  # pickle will raise EOFError if the file is not completed
                            pass
        self.clean()
        raise ProcessError('Process not finished yet.')

    def clean(self) -> int:
        """Clean up the file generated."""
        try:
            os.unlink(self.__res)
            os.unlink(self.__run_name)
            os.unlink(self.args)
            os.unlink(self.kwargs)
        except FileNotFoundError:
            return 1
        return 0

    def __enter__(self):
        self.prepare()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()
