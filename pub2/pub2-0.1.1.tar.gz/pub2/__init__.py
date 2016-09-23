#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pub2 (cc) 2016 Ian Dennis Miller


import glob
import json
import yaml
import os
import re
import shutil
import click
import codecs
from git import Repo
from jinja2 import Template
from distutils.dir_util import copy_tree


class Pub2():
    def __init__(self, directory_list=["_pub"], json_destination="_data/pub.json"):
        self.ensure_paths()
        self.directory_list = directory_list
        self.json_destination = json_destination

    def init_folders(self):
        """
        Expand skel into current folder.
        """
        venv_path = os.environ.get("VIRTUAL_ENV")
        if venv_path:
            os.system("mrbob -w {0} -O .".format(os.path.join(venv_path, "share/skel")))
            os.remove(".mrbob.ini")
        else:
            print("Pub must be installed within a Python virtualenv for this feature to work.")

    def find_files(self):
        """
        find all files for processing
        """
        all_files = list()

        for directory in self.directory_list:
            all_files.extend(glob.glob("{0}/*.tex".format(directory)))

        return(all_files)

    def detect_changed_files(self):
        """
        return a list of files in _pub that are newer than the corresponding versions in pub.
        """
        changed_files = list()

        # for each file in _pub
        for filename in self.find_files():
            # check whether the corresponding files in pub are older
            pub_file = File(filename)
            if pub_file.is_stale():
                changed_files.extend([filename])

        return(changed_files)

    def create_json_digest(self):
        """
        summarize Pub contents into _data/pub.json
        """
        summary = list()

        for filename in self.find_files():
            pub_file = File(filename)
            preamble = pub_file.get_preamble()
            summary.append({
                'title': preamble['title'],
                'author': preamble['author'],
                'identifier': preamble['identifier'],
                'year': preamble['year'],
                'category': preamble['category'],
                })

        with codecs.open(self.json_destination, "w", "utf-8") as f:
            json.dump(summary, f)

    def build(self, rebuild):
        """
        transform files from _pub into their publication versions in pub.
        """

        if rebuild:
            changed_files = self.find_files()
        else:
            changed_files = self.detect_changed_files()

        if changed_files:
            for filename in changed_files:
                print("process: {0}".format(filename))
                pub_file = File(filename)
                pub_file.create_bibtex()
                pub_file.create_pdf()
            self.create_json_digest()
        print("Done")

    def ensure_paths(self):
        """
        mkdir pub
        """
        if not os.path.exists("pub"):
            os.makedirs("pub")

        if not os.path.exists("_pub"):
            os.makedirs("_pub")


class File():
    def __init__(self, filename):
        self.filename = filename
        self.raw = None

        with codecs.open(filename, "r", "utf-8") as f:
            self.raw = f.read()

        self.preamble = self.get_preamble()
        self.content = self.get_content()
        self.identifier = self.get_identifier()
        self.checksum = self.get_checksum()
        self.preamble['checksum'] = self.checksum

    def get_checksum(self):
        """
        """

        try:
            repo = Repo(".")
        except:
            print("not operating in git")
            return()

        hc = repo.head.commit
        git_checksum = str(hc)[:8]
        return(git_checksum)

    def get_language(self):
        """
        normalize the filename extension into a language symbol.
        """
        base_filename, file_extension = os.path.splitext(self.filename)
        mapping = {
            "md": "markdown",
            "markdown": "markdown",
            "tex": "latex",
        }
        if file_extension in mapping:
            return(mapping[file_extension])

    def get_preamble(self):
        """
        extract portion of file between ---.
        decode it as YAML and return a python object.
        """
        re_preamble = r"---\n(.*?)---\n"
        m = re.match(re_preamble, self.raw, re.MULTILINE | re.DOTALL)
        if m:
            preamble = m.group(1)
            return(yaml.load(preamble))
        else:
            print("cannot find preamble")

    def get_content(self):
        """
        return everything appearing after the preamble
        """
        re_content = r"^---$.*?^---$(.*)"
        m = re.search(re_content, self.raw, re.MULTILINE | re.DOTALL)
        if m:
            content = m.group(1)
            return(unicode(content))

    def get_rendered_content(self):
        """
        """
        # env = Environment(loader=PackageLoader('pub', '_layouts'))

        if 'layout' in self.preamble and self.preamble['layout'] != None:
            with codecs.open("_pub/_layouts/{0}.tex".format(self.preamble['layout']), "r", "utf-8") as f:
                re_content = r"^---$.*?^---$(.*)"
                m = re.search(re_content, f.read(), re.MULTILINE | re.DOTALL)
                if m:
                    layout_template = Template(m.group(1))
            result = layout_template.render(pub=self.preamble, content=self.content)
            # result = layout_template.render(pub=self.preamble, content="")
            return(result)
        else:
            return(self.content)

    def get_identifier(self):
        """
        return a hardcoded identifier - otherwise, format default
        """
        if 'identifier' in self.preamble:
            return(self.preamble['identifier'])
        else:
            self.preamble['author_last'] = self.preamble['author'].split(" ")[0]
            self.preamble['title_first'] = self.preamble['title'].split(" ")[0]
            return("{author_last}_{title_first}_{year}").format(self.preamble)

    def create_bibtex(self):
        """
        create the bibtex file for this pub
        """
        # determine filename
        filename = "./pub/{0}.bib".format(self.identifier)
        bibtex_str = bibtex_template.format(**self.preamble)
        with codecs.open(filename, "w", "utf-8") as f:
            f.write(bibtex_str)

    def create_pdf(self):
        """
        create the PDF file for this pub
        """
        # ensure .build directory exists
        if not os.path.exists(".build"):
            os.makedirs(".build")

        with codecs.open(".build/pub.tex", "w", "utf-8") as f:
            tmp_content = self.get_rendered_content()
            f.write(tmp_content)

        basename = os.path.basename(self.filename)[:-4]

        # copy assets
        assets_path = "_pub/_assets/{0}/".format(basename)
        if os.path.exists(assets_path):
            copy_tree(assets_path, ".build/")
        else:
            print("no assets for {0}".format(basename))

        latex_cmd = 'cd .build && pdflatex pub.tex'
        bibtex_cmd = 'cd .build && bibtex pub.aux'
        biber_cmd = 'cd .build && biber pub'

        # run latex
        os.system(latex_cmd)

        # if bibliography
        if "bibtex" in self.preamble and self.preamble["bibtex"] == True:
            os.system(bibtex_cmd)
            os.system(latex_cmd)
        elif "biber" in self.preamble and self.preamble["biber"] == True:
            os.system(biber_cmd)
            os.system(latex_cmd)

        os.system(latex_cmd)

        # copy result PDF
        shutil.copy2(".build/pub.pdf", "pub/{0}.pdf".format(self.preamble["identifier"]))
        shutil.rmtree(".build")

    def is_stale(self):
        """
        return True if the files in pub are older than the one in _pub.
        """
        bib_filename = "pub/{0}.bib".format(self.identifier)
        pdf_filename = "pub/{0}.pdf".format(self.identifier)

        # if the .bib or .pdf does not exist, return True
        if not os.path.isfile(bib_filename):
            return True

        if not os.path.isfile(pdf_filename):
            return True

        # if the modification time of the .bib or .pdf is older, return True
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(self.filename)
        source_mtime = mtime

        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(bib_filename)
        bib_mtime = mtime

        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(pdf_filename)
        pdf_mtime = mtime

        if source_mtime > bib_mtime or source_mtime > pdf_mtime:
            return True


@click.group()
def cli():
    pass


@cli.command('init', short_help='create fresh Pub folders')
def init():
    pub = Pub2()
    pub.init_folders()


@cli.command('build', short_help='build files')
def build():
    pub = Pub2()
    pub.build(rebuild=False)


@cli.command('rebuild', short_help='force rebuild of all files')
def rebuild():
    pub = Pub2()
    pub.build(rebuild=True)


@cli.command('new', short_help='create an empty file')
def new_from_template():
    title = raw_input("Title: ")
    author = raw_input("Author(s): ")
    year = raw_input("Year: ")
    filename = "-".join(title.split(" ")).lower() + ".tex"
    with codecs.open("_pub/{0}".format(filename), "w", "utf-8") as f:
        f.write(blank_template.format(title=title, author=author, year=year))
    print("created file: _pub/{0}".format(filename))


cli.add_command(build)
cli.add_command(rebuild)

bibtex_template = """\
@misc{{{identifier},
  title =        "{title}",
  author =       "{author}",
  year =         "{year}",
  publisher =    "Ian Dennis Miller",
  howpublished = "\\url{{http://imiller.utsc.utoronto.ca/pub/{identifier}.pdf}}",
}}
"""

blank_template = """\
---
layout: default
title: {title}
author: {author}
year: {year}
identifier: name_title_{year}
category: archive|personal
bibtex: false
biber: false
provenance: Appears in ...
---

"""

if __name__ == '__main__':
    cli()
