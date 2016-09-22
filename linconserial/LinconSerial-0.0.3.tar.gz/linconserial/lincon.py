#import fcntl
import serial
import time
import threading
import random
import select
import Queue
import array
import string
import os
import md5

from linconserial.exceptions import LinConError

CTL_C = "\x03"
CTL_D = "\x04"
DEBUG = False

class _LinConWorkerThread_(threading.Thread):
    def __init__(self, ser, serlock, logfilename = "/tmp/.lincon"):
        threading.Thread.__init__(self)
        self.ser = ser
        self.serlock = serlock
        self.rbuflock = threading.Lock()
        self.error = None
        self.errortime = None
        self.read_event = threading.Event()
        self.rbuf = array.array('c')
        self._wchars_per_sec_ = []
        self._rchars_per_sec_ = []
        self._rindex_ = 0
        self.daemon = True
        self.stopFlag = threading.Event()
        self.logfilename = logfilename
        self.logfile = None

    def stop(self):
        self.stopFlag.set()

    def init(self):
        self.logfile = open(self.logfilename, "w")
        pass

    def cleanup(self):
        if self.logfile:
            try:
                self.logfile.close()
            except Exception:
                pass
            self.logfile = None
        pass

    def proceed(self):
        return not self.stopFlag.isSet()

    def run(self):
        self.init()
        self.stopFlag.clear()
        while self.proceed():
            self.worker()
        self.stop()
        self.cleanup()

    def ready(self):
        if self.error:
            raise self.error

        self.rbuflock.acquire()
        try:
            ready = (self.rbuf[self.rindex:].index("\n") > 0)
        except Exception:
            ready = False
        self.rbuflock.release()
        return ready

    def writeline(self, line, timeout = 5):
        self.rbuflock.acquire()
        index = len(self.rbuf)
        self.rbuflock.release()

        self.flush()

        count = 0
        for char in line:
            written = False
            echoed = False
            endtime = time.time() + timeout
            while not echoed and time.time() < endtime:
                if written:
                    if char and len(char) > 0 and char in string.printable:
                        self.rbuflock.acquire()
                        if len(self.rbuf) > index:
                            try:
                                self.rbuf.pop(
                                    index + self.rbuf[index:].index(char))
                                echoed = True
                            except Exception as error:
                                pass
                            index = len(self.rbuf)
                        self.rbuflock.release()

                    else:
                        echoed = True

                    if not echoed:
                        self.read_event.clear()
                        self.read_event.wait(endtime - time.time())
                        self.read_event.clear()

                else:
                    error = None

                    self.serlock.acquire()
                    try:
                        length = self.ser.write(char)
                    except Exception as e:
                        msg = "Failed to write char to Linux serial connection"
                        try:
                            msg = msg + ": %r" %(char)
                        except Exception:
                            pass
                        try:
                            msg = msg + " in %r" %(line)
                        except Exception:
                            pass
                        try:
                            msg = msg + ": %r" %(e)
                        except Exception:
                            pass
                        error = LinConError(msg)
                
                    if length > 0:
                        self.rbuflock.acquire()
                        index = len(self.rbuf)
                        self.rbuflock.release()
                        written = True

                    self.serlock.release()
                    
                    if error != None:
                        raise error

                if echoed:
                    count = count + 1

        if len(line) != count:
            msg = "Write operation timed out"

            try:
                msg = msg + " after %d seconds" %(timeout)
            except Exception:
                pass
            
            try:
                msg = msg + ": %r" %(line)
            except Exception:
                pass
            
            raise LinConError(msg)

        if DEBUG:
            print ">>> %r" %(line)
                
        return line

    def readline(self, timeout = 0):
        if self.error:
            raise self.error

        line = None
        endtime = time.time() + timeout
        while not self.ready() and time.time() < endtime:
            time.sleep(0.1)

        if self.ready():
            self.rbuflock.acquire()
            try:
                i = self.rbuf[self.rindex:].index("\n") + self.rindex
                line = self.rbuf[self.rindex:i].tostring().replace("\r", "")
                self.rindex = i + 1
            except Exception:
                pass
            self.rbuflock.release()

        return line

    def flush(self):
        if self.error:
            raise self.error
        self.rbuflock.acquire()
        self.rindex = len(self.rbuf)
        self.rbuflock.release()

    def worker(self):
        chars = ""

        self.serlock.acquire()
        try:
            chars = self.ser.read(self.ser.inWaiting())
        except Exception as error:
            self.error = LinConError(
                "Linux serial connection worker thread died: %r" %(error))
            self.errortime = time.time()
            self.stop()
            if DEBUG:
                print "!!! %r" %(self.error)
        self.serlock.release()

        if len(chars) > 0:
            self.rbuflock.acquire()
            try:
                self.rbuf.fromstring(chars)
                if self.logfile:
                    self.logfile.write(chars)
                if DEBUG:
                    print "<<< %r" %(chars)
            except Exception:
                pass
            self.rbuflock.release()
            self.read_event.set()

class LinCon:
    def __init__(self, tmpdir = "/tmp/.lincon"):
        try:
            self.tmpdir = str(tmpdir)
        except Exception:
            msg = "Invalid name for temporary lincon directory"
            try:
                msg = msg + ": %r" %(tmpdir)
            except Exception:
                pass
            raise LinConError(msg)

        self.ports = {}
        self.scripts = {}

        scriptdir = os.path.dirname(os.path.realpath(__file__)) + "/scripts"

        if not os.path.isdir(scriptdir):
            msg = "Unable to locate shell script directory"
            try:
                msg = msg + " in %s" %(scriptdir)
            except Exception:
                pass
            raise LinConError(msg)

        for filename in os.listdir(scriptdir):
            try:
                f = open("%s/%s" %(scriptdir, filename))
                self.scripts[filename] = f.read()
            except Exception:
                msg = "Failed to read script file"
                try:
                    msg = msg + ": %s" %(filename)
                except Exception:
                    pass
                try:
                    msg = msg + " in %s" %(scriptdir)
                except Exception:
                    pass
                raise LinConError(msg)

            try:
                f.close()
            except Exception:
                pass


    def _verify_open_(self, open_result):
        env = self._get_env_(open_result)
        msg = ""
        if not env["ser"] or not env["ser"].isOpen():
            msg = "Linux serial connection is not open"
            self.ser = None
        
        elif not env["workerthread"] or not env["workerthread"].is_alive():
            msg = "Linux serial connection worker thread is not running"
            env["workerthread"] = None

        if msg:
            try:
                msg = msg + ": " + str(env["port"]) 
            except Exception:
                pass
            raise LinConError(msg)

    def _body_is_int_(self, open_result, filename):
        try:
            int(self.readfile(open_result, filename))
        except Exception as e:
            return False
        return True

    def _get_env_(self, open_result):
        try:
            return self.ports[open_result["port"]]
        except Exception:
            msg = "No connection associated with serial port"
            try:
                msg = msg + ": %r" %(open_result["port"])
            except Exception:
                pass
            raise LinConError(msg)

    def _mk_tmpdir_(self, open_result):
        self.writeline(open_result, "mkdir -p '%s'" %(self.tmpdir))

    def clear(self, open_result):
        for char in ["", CTL_D, CTL_D, "", CTL_C, CTL_C, ""]:
            try:
                self.writeline(open_result, char, clear_prompt = False)
            except Exception:
                pass
        time.sleep(1)
        self.writeline(open_result, "")
        self.flush(open_result)

    def open(self, port, baudrate = 115200):
        retval = {
            "port": port,
            "baudrate": baudrate,
        }
        env = {
            "port": port,
            "baudrate": baudrate,
        }
        env["execLock"] = threading.Lock()
        env["serlock"] = threading.Lock()

        self.ports[port] = env

        try:
            env["ser"] = serial.Serial(
                port=env["port"], baudrate = env["baudrate"], timeout = 0)
            # Verify no other process has a lock on the port
            #fcntl.lockf(env["ser"].fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (serial.SerialException, IOError) as error:
            msg = "Failed to open linux connection serial port"
            try:
                msg = msg + ", `%s`" %(str(env["port"]))
            except Exception:
                pass
            try:
                msg = msg + ": " + str(error)
            except Exception:
                pass
            self.close(retval)
            raise LinConError(msg)

        env["workerthread"] = _LinConWorkerThread_(
            env["ser"], env["serlock"])
        env["workerthread"].start()

        self.clear(retval)
        return retval

    def close(self, open_result):
        try:
            env = self._get_env_(open_result)
            if env["workerthread"]:
                try:
                    env["workerthread"].stop()
                    env["workerthread"].join(1)
                except Exception:
                    pass

            if env["ser"]:
                try:
                    #fcntl.lockf(env["ser"].fileno(), fcntl.LOCK_UN)
                    env["ser"].close()
                except Exception:
                    pass
                    
                try:
                    env["ser"] = None
                except Exception:
                    pass

            try:
                del self.ports[open_result["port"]]
            except Exception:
                pass

        except Exception:
            pass

    def echo_escape(self, text):
        esc_text = ""
        for char in text:
            if (not char in string.letters and
                not char in string.digits):
                esc_text = esc_text + "\\x%02x" %(ord(char))
            else:
                esc_text = esc_text + char
        return esc_text

    def flush(self, open_result):
        self._verify_open_(open_result)
        self._get_env_(open_result)["workerthread"].flush()
        
    def writeline(self, open_result, line, clear_prompt = True):
        self._verify_open_(open_result)
        if clear_prompt:
            msg = 'PS1=""'
            if len(line) > 0:
                msg = msg + '; ' + line
        else:
            msg = line

        if msg[-1] != "\n":
            msg = msg + "\n"

        self._get_env_(open_result)["workerthread"].writeline(msg)
        return line

    def readline(self, open_result, timeout = 1):
        self._verify_open_(open_result)
        return self._get_env_(open_result)["workerthread"].readline(
            timeout = timeout)

    def find(self, open_result, strings, timeout = 5, getall = False):
        lines = []
        if not isinstance(strings, list):
            strings = [strings]

        endtime = time.time() + timeout
        while time.time() < endtime:
            line = self.readline(open_result, timeout = endtime - time.time())
            try:
                if line:
                    lines.append(line)
                    for string in strings:
                        if string in line:
                            if getall:
                                return lines
                            else:
                                return lines[-1]
                else:
                    time.sleep(0.1)
            except Exception:
                pass
        return None

    def file_exists(self, open_result, filename, timeout = 5):
        error = None
        try:
            good_resp = "++%d++" %(time.time() * 100000)
            bad_resp = "--%d--" %(time.time() * 100000)

            self.writeline(open_result, 
                           'ls %s && ' %(filename) +
                           'printf "%s\\n%%.0s" 1 2 3 4 5 || ' %(good_resp) +
                           'printf "%s\\n%%.0s" 1 2 3 4 5' %(bad_resp))

            line = self.find(
                open_result, [good_resp, bad_resp], timeout = timeout,
                getall = False)

            if line:
                if good_resp in line:
                    return True
                elif bad_resp in line:
                    return False

        except LinConError as error:
            pass

        msg = "Unable to determine if file exists"
        try:
            msg = msg + ": " + str(filename)
        except Exception:
            pass

        try:
            if error:
                msg = msg + ": %r" %(error)
        except Exception:
            pass

        raise LinConError(msg)

    def rmfile(self, open_result, filename, isdir = False, timeout = 5):
        cmd = 'rm -f '
        if isdir:
            cmd = cmd + '-r '

        cmd = cmd + '"%s" &> /dev/null' %(filename)

        try:
            self.writeline(open_result, cmd)
        except LinConError as error:
            raise LinConError("Failed to remove file: %r" %(error))

        if self.file_exists(open_result, filename, timeout):
            raise LinConError("File removal failed: " + filename)

    def readfile(self, open_result, filename):
        i = 0
        chunk = ""
        chunks = []
        chunk_size = 320
        attempts = 0
        maxattempts = 10
        backofftime = 1.0/maxattempts
        t_start = time.time()

        if not self.file_exists(open_result, filename):
            msg = "Linux reports that file doesn't exist"
            try:
                msg = msg + ": " + str(filename)
            except Exception:
                pass
            time.sleep(10)

            raise LinConError(msg)

        script_filename = "%s/read.sh" %(self.tmpdir)

        if not self.file_exists(open_result, script_filename):
            try:
                self._mk_tmpdir_(open_result)
                self.writefile(open_result,
                               filename = script_filename,
                               text = self.scripts["read.sh"])
            except Exception as error:
                msg = "Failed to transfer file reader script"
                try:
                    msg = msg + " to %s" %(script_filename)
                except Exception:
                    pass
                try:
                    msg = msg + ": %r" %(error)
                except Exception:
                    pass
                raise LinConError(msg)

        while True:
            if i < 0:
                break
            elif attempts > maxattempts:
                msg = "Failed to read line %d" %(i)
                try:
                    msg = msg + " of " + str(filename)
                except Exception:
                    pass
                msg = msg + " after %d attempts" %(attempts - 1)
                raise LinConError(msg)

            try:
                self.writeline(
                    open_result,
                    '/bin/sh %s %s %d %d'
                    %(script_filename, filename, i, chunk_size))
            except LinConError as error:
                msg = "An error occurred while reading chunk %d" %(i)
                try:
                    msg = msg + " of " + str(filename)
                except Exception:
                    pass

                try:
                    msg = msg + ": %r" %(error)
                except Exception:
                    pass

                raise LinConError(msg)

            # Read chunks until one comes along that's formatted correctly
            reads = 0
            maxreads = 100 

            chunk = None
            done = False
            while reads < maxreads:
                try:
                    line = self.readline(open_result, timeout = 1.0/maxreads)
                except LinConError as error:
                    msg = "A read error occurred on line %d" %(i)
                    try:
                        msg = msg + " of " + str(filename)
                    except Exception:
                        pass

                    try:
                        msg = msg + ": %r" %(error)
                    except Exception:
                        pass

                    raise LinConError(msg)

                reads = reads + 1
                if line:
                    try:
                        result_ = line.split(":")
                        assert len(result_) == 2
                        chunk_ = result_[0]
                        md5_ = md5.new()
                        md5_.update(chunk_)
                        assert(md5_.hexdigest() == result_[1])
                        chunk = result_[0]
                        break
                    except Exception:
                        pass

            # Handle response
            try:
                assert(chunk != None)
                if len(chunk) > 0:
                    chunks.append(chunk)
                    i = i + 1
                    attempts = 0
                else:
                    break
            except Exception:
                attempts = attempts + 1

        return "".join(chunks).decode("hex")
        
    def writefile(self, open_result, filename = "", text = ""):
        t_start = time.time()
        if len(filename) <= 0:
            filename = "/tmp/.%x" %(time.time() * 1000000)

        try:
            self.rmfile(open_result, filename)
            size = 80
            for i in range(0, len(text), size):
                chunk = self.echo_escape(text[i:i+size])
                self.writeline(
                    open_result,
                    'echo -en "%s" >> "%s"' %(chunk, filename))
        except Exception as error:
            msg = "An error occurred while attempting to write to file"
            try:
                msg = msg + ": " + str(filename)
            except Exception:
                pass

            try:
                msg = msg + ": `%r`" %(text)
            except Exception:
                pass

            try:
                msg = msg + ": %r" %(error)
            except Exception:
                pass
            raise LinConError(msg)

        return filename

    def killbg(self, open_result, run_result):
        try:
            self.run(open_result, "kill -9 %d" %(run_result["pid"]))
        except Exception:
            pass
        
        try:
            self.rmfile(open_result, run_result["dir"], isdir = True)
        except Exception:
            pass

    def isrunning(self, open_result, pid):
        if isinstance(pid, dict) and "pid" in pid:
            pid = pid["pid"]

        if not isinstance(pid, int):
            msg = "Input does not contain a PID"
            try:
                msg = msg + ": `%r`" %(pid)
            except Exception:
                pass
            raise LinConError(msg)

        try:
            return self.run(
                open_result,
                '[ -n %d -a -d /proc/%d ]' %(pid, pid))["status"] == 0
        except Exception:
            msg = "Unable to determine pid status"
            try:
                msg = msg + " of %r" %(pid)
            except Exception:
                pass
            try:
                msg = msg + ": " + str(e)
            except Exception:
                pass

    def run(self, open_result, cmd, bg = False, timeout = 5):
        resultdir = '%s/%d' %(self.tmpdir, time.time())
        result_filename = "%s/r" %(resultdir)
        script_filename = "%s/run.sh" %(self.tmpdir)

        if bg:
            bg = 1
        else:
            bg = 0

        if not self.file_exists(open_result, script_filename):
            try:
                self._mk_tmpdir_(open_result)
                self.writefile(open_result,
                               filename = script_filename,
                               text = self.scripts["run.sh"])
            except Exception as error:
                msg = "Failed to transfer command executor script"
                try:
                    msg = msg + " to %s" %(script_filename)
                except Exception:
                    pass
                try:
                    msg = msg + ": %r" %(error)
                except Exception:
                    pass
                raise LinConError(msg)

        env = self._get_env_(open_result)
        env["execLock"].acquire()
        error = None
        try:
            self.rmfile(open_result, resultdir, isdir = True)
            self.writeline(open_result, '/bin/sh %s %d %s %s'
                           %(script_filename, bg, resultdir, cmd))
        except LinConError as e:
            msg = "An error occurred while attempting to execute command"
            
            try:
                msg = msg + ": %r" %(cmd)
            except Exception:
                pass

            try:
                msg = msg + ": %r" %(e)
            except Exception:
                pass

            error = LinConError(msg)
            pass

        complete = False
        endtime = time.time() + timeout
        while not error and not complete and time.time() < endtime:
            try:
                complete = self.file_exists(
                    open_result, result_filename, timeout = 0.5)
            except LinConError:
                pass
            except AssertionError:
                time.sleep(0.1)
            
            time.sleep(1)

        if not error and not complete:
            msg = "Command timed out after %d seconds" %(timeout)
            try:
                msg = msg + ": %r" %(cmd)
            except Exception:
                pass

            error = LinConError(msg)

        result = {
            "cmd": cmd,
            "dir": resultdir,
            "status": None,
            "pid": None,
            "stdout": None,
            "stderr": None
        }

        if not error:
            try:
                result_file = self.readfile(open_result, result_filename)
                lines = result_file.split("\n")
                result["status"] = int(lines[0])
                if bg:
                    result["pid"] = int(lines[1])
                else:
                    outlen = int(lines[1])
                    errlen = int(lines[2])
                    result["stdout"] = "\n".join(
                        lines[3:3+outlen])
                    result["stderr"] = "\n".join(
                        lines[3+outlen:3+outlen+errlen])
            except Exception as e:
                msg = "Unable to determine the results of the command"
                try:
                    msg = msg + ": `%r`" %(cmd)
                except Exception:
                    pass
                try:
                    msg = msg + ": %r" %(e)
                except Exception:
                    pass

                error = LinConError(msg)

        if not bg:
            try:
                self.rmfile(open_result, resultdir, isdir = True)
            except Exception:
                pass
        env["execLock"].release()

        if error:
            raise error

        return result

    def runfg(self, open_result, cmd, timeout = 5):
        return self.run(open_result, cmd, bg = False, timeout = timeout)

    def runbg(self, open_result, cmd, timeout = 5):
        return self.run(open_result, cmd, bg = True, timeout = timeout)
