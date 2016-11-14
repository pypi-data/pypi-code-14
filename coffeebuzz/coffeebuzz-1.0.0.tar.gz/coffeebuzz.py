#!/usr/local/bin/python3

import subprocess
import sys

def changeCoffeeStatus(targetMode):
    """mode should be one of 'off', 'doze', 'buzz'"""
    try:
        mode = ['off', 'doze', 'buzz'].index(targetMode.lower())
        subprocess.check_call(['killall', 'Coffee Buzz'])
        subprocess.check_call(['defaults', 'write', '-app', "Coffee Buzz", 'OperationMode', str(mode)])
        subprocess.check_call(['open', '-a', 'Coffee Buzz'])
    except IndexError:
        print("No argument")
    except ValueError:
        print("Wrong argument")
    except subprocess.CalledProcessError as e:
        print("Non-zero exit code: {}/{}".format(e.returncode, e.cmd))
    except:
        print("unknown error")