# -*- coding: utf-8 -*-

import sys
import threading
import subprocess
import os
from flask import Flask
import glob
import argparse

app = Flask(__name__)
engines = ["google", "linkedin", "bing", "yahoo", "github"]


class EngineThread (threading.Thread):
    """Thread used to call EmailHarvester for a specific engine (google, github, bing, etc...)."""

    def __init__(self, domain, engine):
        threading.Thread.__init__(self)
        self.domain = domain
        self.engine = engine

    def run(self):
        """Run function for this thread"""
        callEmailHarvester(self.domain, self.engine)


def callEmailHarvester(domain, engine):
    """
    Call EmailHarvester module.
    Arguments:
        domain -- the domain name (e.g. gmail.com)
        engine -- the engine name (e.g. google, github, bing, etc...)
    """
    command = " ".join(['emailharvester', 
               '-d', domain, 
               '-e', engine, 
               '-s', 'result_{0}.txt'.format(engine)])
    subprocess.call(command, shell=True)


def extractFileContent(filename):
    """
    Extract the EmailHarvester results into the result file.
    Arguments:
        filename -- the result file

    filename -- the result file
    """
    with open(filename) as f:
        return f.readlines()


def generateOutput(emails):
    return ", ".join(list(set(emails))).replace('\n', '') 


def generatedFiles():
    return glob.glob('./result_*.txt')


def generatedXMLFiles():
    return glob.glob('./result_*.xml')


def getResults():
    """Return all emails found by EmailHarvester."""
    emails = []
    for filename in generatedFiles():
        emails += extractFileContent(filename)
        os.remove(filename)
    for filename in generatedXMLFiles():
        os.remove(filename)
    return generateOutput(emails)


@app.route('/domain=<domain>')
def search(domain):
    """
    Search emails for a specific domain name.
    Arguments:
        domain -- the domain name
    """
    threads = []

    # Setup search engines
    for engine in engines:
        current_thread = EngineThread(domain, engine)
        current_thread.start()
        threads.append(current_thread)

    # Wait for all threads to complete
    for t in threads:
        t.join()

    return getResults()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("launch_mode", help="Possible values are : mail", nargs='?', default="talk")
    args = parser.parse_args()
    if args.launch_mode == "talk":
        app.run(debug=True, host='0.0.0.0')
    elif args.launch_mode == "mail":
        print("Mail mode")
    else:
        parser.print_help()
