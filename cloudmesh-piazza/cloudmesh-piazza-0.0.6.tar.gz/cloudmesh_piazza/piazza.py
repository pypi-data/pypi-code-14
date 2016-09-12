"""Usage:
   piazza [--file] list FOLDER
   piazza convert FOLDER [--html|--latex]

Process FILE and optionally apply correction to either left-hand side or
right-hand side.

Arguments:
  FOLDER     optional input file

Options:
  -h --help

"""
#!/usr/bin/env python
from __future__ import print_function
from docopt import docopt
import yaml
import os
import json

from cm_piazza_api import PiazzaExtractor

def main():
    arguments = docopt(__doc__)
    print(arguments)

    if arguments["--file"]:
        with open(".piazza", 'r') as stream:
            try:
                config = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        print (config)
        password = config["piazza"]["password"]
        email = config["piazza"]["email"]
        print (email, password)
    else:
        password = None
        email = None
        
    if arguments["list"]:
        folder = arguments["FOLDER"]

        print (folder)

        piazza = PiazzaExtractor()
        email, password = piazza.get_login()
        piazza.login(email=email, password=password)
        piazza.save_folder_posts(folder)

        # os.system ("cat {folder}.json | python -m json.tool".format(**locals()))

    elif arguments["convert"]:
        html = arguments["--html"]
        latex = arguments["--latex"]
        folder = arguments["FOLDER"]

        json_data = open(folder + ".json").read()
        data = json.loads(json_data)

        if html:

            html_file = open(folder + ".html", "w+")

            for post in data["feed"]:
                html_file.write("\n\n<h1> {subject} </h1>\n".format(**post))
                html_file.write("Uid: {uid}<br>\n".format(**post))
                html_file.write("Created: {created}<br>\n".format(**post))
                html_file.write("\n")

                content = post["content"].encode('utf-8')
                html_file.write(content)
                #sys.exit(1)
            html_file.close()

if __name__ == '__main__':
    main()
