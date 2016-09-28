#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Pub2 (cc) 2016 Ian Dennis Miller

import yaml
import os
import re
import codecs


class Reader():
    def __init__(self, file_obj):
        self.file = file_obj

        self.raw = None
        with codecs.open(self.file.filename, "r", "utf-8") as f:
            self.raw = f.read()

        self.preamble = self._preamble()
        self.content = self._content()
        self.identifier = self._identifier()
        self.language = self._language()

    def _language(self):
        """
        normalize the filename extension into a language symbol.
        """
        base_filename, file_extension = os.path.splitext(self.file.filename)
        mapping = {
            "md": "markdown",
            "markdown": "markdown",
            "tex": "latex",
        }
        if file_extension in mapping:
            return(mapping[file_extension])

    def _preamble(self):
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

    def _content(self):
        """
        return everything appearing after the preamble
        """
        re_content = r"^---$.*?^---$(.*)"
        m = re.search(re_content, self.raw, re.MULTILINE | re.DOTALL)
        if m:
            content = m.group(1)
            return(content)

    def _identifier(self):
        """
        return a hardcoded identifier - otherwise, format default
        """
        if 'identifier' in self.preamble:
            return(self.preamble['identifier'])
        else:
            self.preamble['author_last'] = self.preamble['author'].split(" ")[0]
            self.preamble['title_first'] = self.preamble['title'].split(" ")[0]
            return("{author_last}_{title_first}_{year}").format(self.preamble)
