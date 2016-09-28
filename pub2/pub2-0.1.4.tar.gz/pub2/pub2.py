#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Pub2 (cc) 2016 Ian Dennis Miller

import glob
import json
import os
import sys
import codecs
import pkg_resources
from git import Repo
from file import File
from os.path import join as opj


class Pub2():
    def __init__(self,
                 working_dir=".",
                 directory_list=["_pubs"],
                 json_destination="_data/pub2.json"):
        self.ensure_paths(working_dir)
        self.working_dir = working_dir
        self.directory_list = directory_list
        self.json_destination = json_destination

    def init_folders(self):
        """
        Expand skel into working_dir.
        """
        filename = pkg_resources.resource_filename('pub2', 'skel')
        pathname = os.path.dirname(os.path.abspath(__file__))
        os.system("mrbob -w {0} -O {1}".format(opj(pathname, filename), self.working_dir))
        os.remove(opj(self.working_dir, ".mrbob.ini"))
        os.remove(opj(self.working_dir, "_pubs/_assets/.gitignore"))
        os.remove(opj(self.working_dir, "_data/.gitignore"))

    def find_files(self):
        """
        find all files for processing
        """
        all_files = list()

        for directory in self.directory_list:
            found_files = glob.glob("{0}/*.tex".format(opj(self.working_dir, directory)))
            all_files.extend(found_files)

        return(all_files)

    def detect_changed_files(self):
        """
        return a list of files in _pubs that are newer than the corresponding versions in pub.
        """
        changed_files = list()

        # for each file in _pubs
        for filename in self.find_files():
            # check whether the corresponding files in pub are older
            pub_file = self.load_file(filename)
            if pub_file.is_stale():
                changed_files.extend([filename])

        return(changed_files)

    def create_json_digest(self):
        """
        summarize Pub contents into _data/pub2.json
        """
        # summary = list()
        summary = dict()

        for filename in self.find_files():
            pub_file = self.load_file(filename)
            preamble = pub_file.get_preamble()

            if all(k in preamble for k in ("title", "author", "identifier", "year", "category")):
                summary[preamble['identifier']] = preamble
            else:
                print("ERROR: Missing required fields from preamble: {0}".format(filename))
                sys.exit(1)

        with codecs.open(opj(self.working_dir, self.json_destination), "w", "utf-8") as f:
            json.dump(summary, f)

    def build(self, rebuild=False):
        """
        transform files from _pubs into their publication versions in pub.
        """

        if rebuild:
            changed_files = self.find_files()
        else:
            changed_files = self.detect_changed_files()

        if changed_files:
            self.create_json_digest()
            for filename in changed_files:
                print("process: {0}".format(filename))
                pub_file = self.load_file(filename)
                pub_file.create_bibtex()
                pub_file.create_html()
                pub_file.create_pdf()
        print("Done")

    def ensure_paths(self, working_dir):
        """
        mkdir pub2
        """
        def check_make(path):
            if not os.path.exists(path):
                os.makedirs(path)

        check_make(working_dir)
        check_make(opj(working_dir, "pub2"))
        check_make(opj(working_dir, "_pubs"))

    def create_from_template(self, title, author, year):
        """
        create a new pub from the blank template
        """
        filename = "-".join(title.split(" ")).lower() + ".tex"
        with codecs.open(opj(self.working_dir, "_pubs/_templates/blank.tex"), "r", "utf-8") as f:
            blank_template = f.read()
        with codecs.open(opj(self.working_dir, "_pubs/{0}".format(filename)), "w", "utf-8") as f:
            f.write(blank_template.format(title=title, author=author, year=year))
        print("created file: _pubs/{0}".format(filename))

    def load_file(self, filename):
        """
        load the indicated file from self.working_dir
        """
        f = File(pub2_obj=self, filename=filename)
        return(f)

    def get_checksum(self):
        """
        obtain checksum of git working path, if possible
        """

        try:
            repo = Repo(self.working_dir)
            head_commit = repo.head.commit
            return(str(head_commit)[:8])
        except:
            print("INFO: Not operating in git")
