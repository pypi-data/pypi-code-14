"""
plumbium.processresult
======================

Main plumbium module containing the Pipeline class and function recording methods.
"""

from __future__ import print_function
import datetime
import json
import os
import os.path
import shutil
from subprocess import check_output, STDOUT, CalledProcessError
import tarfile
import tempfile
import traceback
import wrapt
import plumbium.environment
import plumbium.artefacts


class Pipeline(object):
    """
    Main class managing the recording of a processing pipeline.
    """

    def __init__(self):
        self.debug = False
        self.results = []

    def run(self, name, pipeline, base_dir, *inputs, **kwargs):
        """Execute a function as a recorded pipeline.

        Args:
            name (str): The name of the pipeline - used to name the output file.
            pipeline (function): The function to be run.
            base_dir (str): The directory in which to save the pipeline output, also
                used as the root directory for input filenames if the filenames given
                are not absolute.
            \*inputs: The inputs to the pipeline.

        Keyword Args:
            metadata (dict): Additional information to be included in the result JSON.
            filename (str): String template for the result filename.
            result_recorder (object): An instance of a class implementing a `write()`
                method that accepts the results dictionary.
        """

        self.results = []
        self.debug = kwargs.get('debug', False)
        self.metadata = kwargs.get('metadata', None)
        self.result_recorder = kwargs.get('recorder', None)
        self.filename = kwargs.get('filename', '{name}-{start_date:%Y%m%d_%H%M}')
        self.name = name
        self.inputs = inputs
        self.base_dir = base_dir
        self.launched_dir = os.getcwd()
        self._copy_input_files_to_working_dir()
        self.start_date = datetime.datetime.now()
        os.chdir(self.working_dir)
        pipeline_exception = None
        try:
            pipeline(*inputs)
        except Exception as e:
            pipeline_exception = e
            traceback.print_exc()
        finally:
            self.finish_date = datetime.datetime.now()
            os.chdir(self.launched_dir)
            self.save(pipeline_exception)
            shutil.rmtree(self.working_dir)

    def _copy_input_files_to_working_dir(self):
        """Copy any input files to working directory.

        If an input argument is a subclass of
        :class:`plumbium.artefacts.Artefact` copy the file it refers to into
        the working directory.
        """

        self.working_dir = tempfile.mkdtemp(prefix='plumbium_{0}_'.format(self.name))
        for i in self.inputs:
            if not issubclass(type(i), plumbium.artefacts.Artefact):
                continue
            dest_dir = os.path.join(self.working_dir, os.path.dirname(i.filename))
            source = os.path.join(self.base_dir, i.filename)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            shutil.copy(source, dest_dir)

    def _store_printed_output(self):
        with open('printed_output.txt', 'w') as printed_output_record:
            for r in self.results:
                printed_output_record.write(r.output)

    def record(self, result):
        """Record a result for a stage of this pipeline.

        Args:
            result (:class:`plumbium.processresult.ProcessOutput`): The new result.
        """

        self.results.append(result)

    def save(self, exception=None):
        """Create a JSON file with information about the pipeline then save it
        to a gzipped tar file along with all files used in the pipeline.

        Keyword args:
            exception (:class:`exceptions.Exception` or `None`): The exception which caused the
                pipeline run to fail
        """

        results = {
            'name': self.name,
            'environment': plumbium.environment.get_environment(),
            'inputs': [repr(f) for f in self.inputs],
            'dir': self.base_dir,
            'start_date': self.start_date.strftime('%Y%m%d %H:%M'),
            'finish_date': self.finish_date.strftime('%Y%m%d %H:%M'),
        }
        if exception is not None:
            results['pipeline_exception'] = repr(exception)
        if self.metadata is not None:
            results['metadata'] = self.metadata
        results['processes'] = [r.as_dict() for r in self.results]
        basename = self.filename.format(
            metadata=self.metadata,
            name=self.name,
            start_date=self.start_date
        )
        with open(os.path.join(self.working_dir, basename + '.json'), 'w') as f:
            json.dump(results, f, indent=4, separators=(',', ': '))
        archive = tarfile.open(self._clear_filename(self.base_dir, basename, '.tar.gz'), 'w:gz')
        archive.add(self.working_dir, arcname=basename)
        archive.close()
        if self.result_recorder is not None:
            self.result_recorder.write(results)

    def _clear_filename(self, directory, basename, ext):
        """Build a filename that doesn't already exist by appending then incrementing a number.

        Args:
            directory (str): The directory to use.
            basename (str): The basename part of the filename.
            ext (str): The extension part of the filename.

        Returns:
            str: If it doesn't exist returns `directory/basename.ext` otherwise
            returns the first available `directory/basename-xx.ext` where x is
            a counter from 01.
        """

        tgt = os.path.join(directory, basename + ext)
        if os.path.exists(tgt):
            inc = 1
            tgt = os.path.join(directory, '{0}-{1:02d}{2}'.format(basename, inc, ext))
            while os.path.exists(tgt):
                inc += 1
                tgt = os.path.join(directory, '{0}-{1:02d}{2}'.format(basename, inc, ext))
        return tgt


pipeline = Pipeline()


class OutputRecorder(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.command = []
        self.output = b''


_output_recorder = OutputRecorder()


def call(cmd, cwd=None, shell=False):
    """Function used to execute scripts and applications in a pipeline with
    output captured.

    Args:
        cmd (list): List containing the program to be called and any arguments
            e.g. ``['tar', '-x', '-f', 'file.tgz']``.
        cwd (str): Working directory in which to execute the command.
        shell (bool): Execute the command in a shell.

    Returns:
        str: The output from the called command on stdout and stderr.
    """

    output = None
    try:
        _output_recorder.command += cmd
        output = check_output(cmd, stderr=STDOUT, cwd=cwd, shell=shell)
        _output_recorder.output += output
    except CalledProcessError as e:
        print('An error occurred during: {}'.format(' '.join(cmd)))
        print('Output before failure:')
        print(e.output)
        _output_recorder.output = e.output
        raise
    return output


def record(*output_names):
    """Decorator for wrapping pipeline stages.

    Args:
        \*output_names (str): The names of each returned variable.
    """
    @wrapt.decorator
    def process_recorder(wrapped, instance, args, kwargs):
        returned_from_process = None
        exception = None
        _output_recorder.reset()
        started = datetime.datetime.now()
        try:
            returned_from_process = wrapped(*args, **kwargs)
        except:
            exception = traceback.format_exc()
            raise
        finally:
            if type(returned_from_process) is not tuple:
                returned_from_process = (returned_from_process,)
            finished = datetime.datetime.now()
            named_returns = dict(zip(output_names, returned_from_process))
            result = ProcessOutput(
                func=wrapped,
                args=args,
                kwargs=kwargs,
                command=_output_recorder.command,
                output=_output_recorder.output,
                exception=exception,
                started=started,
                finished=finished,
                **named_returns
            )
            pipeline.record(result)
        return result
    return process_recorder


class ProcessOutput(object):
    """A record of one stage within a pipeline.

    Args:
        func (function): The function that was run.
        args (list): The arguments passed to the function.
        kwargs (dict): The keyword arguments passed to the function.
        output (str): Text printed to stdout or stderr during execution.
        exception (:class:`exceptions.Exception` or `None`): The exception that occurred
            running the stage if applicable.
        started (:class:`datetime.datetime`): When the stage was started.
        finished (:class:`datetime.datetime`): When the stage finished executing.

    Keyword args:
        \*\*output_images (:class:`plumbium.artefacts.Artefact`): Images produced by the stage.
    """

    def __init__(self, func, args, kwargs, command, output, exception, started, finished,
                 **output_images):
        self._results = output_images
        self.command = command
        self.output = output
        self.function = func
        self.input_args = args
        self.input_kwargs = kwargs
        self.exception = exception
        self.started = started
        self.finished = finished

    def __repr__(self):
        r = self.function.__name__ + '('
        if self.input_args:
            r += ', '.join([repr(x) for x in self.input_args])
        if self.input_kwargs:
            r += ', '.join(['{0}={1!r}'.format(x) for x in self.input_kwargs])
        r += ')'
        return r

    def as_dict(self):
        """Serialize this output as a ``dict``."""

        d = {
            'function': self.function.__name__,
            'input_args': [repr(x) for x in self.input_args],
            'input_kwargs': {str(x[0]): repr(x[1]) for x in self.input_kwargs},
            'called_command': ' '.join(self.command),
            'printed_output': self.output.decode('utf-8'),
            'returned': [repr(r) for r in self._results.values()],
            'start_time': self.started.strftime('%Y%m%d %H:%M'),
            'finish_time': self.finished.strftime('%Y%m%d %H:%M')
        }
        if self.exception:
            d['exception'] = repr(self.exception)
        return d

    def __getitem__(self, key):
        return self._results[key]
