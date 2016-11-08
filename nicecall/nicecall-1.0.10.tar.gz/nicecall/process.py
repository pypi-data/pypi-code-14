import asyncio
import logging
import nicecall
import subprocess
import threading


class Process():
    def __init__(
            self, on_stdout=None, on_stderr=None, filters=None,
            raise_if_error=False):
        self._on_stdout = on_stdout or []
        self._on_stderr = on_stderr or []
        self._filters = filters or []
        self._raise_if_error = raise_if_error

    def execute(self, args):
        log_command = self._generate_log_command(args)
        logger = logging.getLogger(__name__)
        logger.addHandler(logging.NullHandler())
        logger.info("Called “%s”." % (log_command,))

        with subprocess.Popen(
            args, universal_newlines=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ) as process:
            self._process_std(process)
            process.wait()

            exitcode = process.returncode
            if exitcode:
                logger.warning(
                    "“%s” failed with exit code %s." % (log_command, exitcode))

            if exitcode != 0 and self._raise_if_error:
                raise subprocess.CalledProcessError(exitcode, args[0])

            return exitcode

    def read_stdout(self, args):
        stdout = []
        self.on_stdout(stdout.append).raise_if_error().execute(args)
        return stdout

    def _generate_log_command(self, args):
        def process_item(arg):
            if " " in arg or '"' in arg:
                return '"%s"' % (arg.replace('"', '\\"'),)
            else:
                return arg

        return " ".join(map(process_item, args))

    def _process_std(self, process):
        size = (1 if self._on_stdout else 0) + (1 if self._on_stderr else 0)
        if size == 0:
            return

        # The queue is necessary to ensure stdout and stderr streams are
        # processed completely before waiting for process termination. If this
        # queue is not used, what could happen is that if Python takes too much
        # time processing lines from stdout or stderr within the threads, the
        # process will end, eventually leading to Python program stopping
        # itself and terminating the threads which were still processing
        # output.
        process_queue = asyncio.Queue(maxsize=size)

        if self._on_stdout:
            self._read_stream_async(
                process.stdout, self._on_stdout, process_queue)

        if self._on_stderr:
            self._read_stream_async(
                process.stderr, self._on_stderr, process_queue)

        while not process_queue.full():
            pass

        # The queue now contains for every thread either `None` if the thread
        # terminated successfully, or the exception if the one was raised.
        # Let's walk through the queue and raise the swallowed exceptions on
        # the main thread.
        while not process_queue.empty():
            result = process_queue.get_nowait()
            if result is not None:
                raise result

    def keep(self, predicate):
        result = self._clone()
        result._filters.append(predicate)
        return result

    def ignore(self, predicate):
        return self.keep(self._invert(predicate))

    def _invert(self, predicate):
        def result(line):
            return not predicate(line)

        return result

    def on_stdout(self, action):
        result = self._clone()
        result._on_stdout.append(action)
        return result

    def on_stderr(self, action):
        result = self._clone()
        result._on_stderr.append(action)
        return result

    def raise_if_error(self):
        result = self._clone()
        result._raise_if_error = True
        return result

    def _clone(self):
        return self.__class__(
            self._on_stdout[:], self._on_stderr[:], self._filters[:],
            self._raise_if_error)

    def _read_stream_async(self, stream, actions, process_queue):
        task = threading.Thread(
            target=self._read_stream, args=(stream, actions, process_queue))

        task.start()

    def _read_stream(self, stream, actions, process_queue):
        try:
            for raw_line in stream:
                line = raw_line.rstrip("\n")
                if all((prefilter(line) for prefilter in self._filters)):
                    for action in actions:
                        action(line)
            process_queue.put_nowait(None)
        except Exception as e:
            process_queue.put_nowait(e)
