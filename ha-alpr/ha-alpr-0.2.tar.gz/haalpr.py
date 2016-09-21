import subprocess
import re
import io

RE_ALPR_PLATE = r"^plate\d*:"
RE_ALPR_RESULT = r"- (\w*)\s*confidence: (\d*.\d*)"

class HAAlpr(object):
    """Wrapper for command line tool alpr."""

    def __init__(self, binary="alpr", country=None):
        """Init Alpr wrapper."""
        self._cmd = [binary]
        if country:
            self._cmd.extend(['-c', country])

        # add stdout
        self._cmd.append('-')

        self.__re_plate = re.compile(RE_ALPR_PLATE)
        self.__re_result = re.compile(RE_ALPR_RESULT)

    def recognize_byte(self, image):
        """Process a byte image buffer."""
        result = []

        alpr = subprocess.Popen(
            self._cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )

        # send image
        stdout, stderr = alpr.communicate(input=image)
        stdout = io.StringIO(str(stdout, 'utf-8'))

        tmp_res = {}
        while True:
            line = stdout.readline()
            if not line:
                if len(tmp_res) > 0:
                    result.append(tmp_res)
                break

            new_plate = self.__re_plate.search(line)
            new_result = self.__re_result.search(line)

            # found a new plate
            if new_plate and len(tmp_res) > 0:
                result.append(tmp_res)
                tmp_res = {}
                continue

            # found plate result
            if new_result:
                try:
                    tmp_res[new_result.group(1)] = float(new_result.group(2))
                except ValueError:
                    continue

        return result
