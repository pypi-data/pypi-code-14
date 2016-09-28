#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Pub2 (cc) 2016 Ian Dennis Miller

import os
import re
import shutil
import codecs
from wand.image import Image
from wand.color import Color
from os.path import join as opj
from jinja2 import Template
from distutils.dir_util import copy_tree


class Writer():
    def __init__(self, file_obj):
        self.file = file_obj
        self.working_dir = file_obj.pub2_obj.working_dir

    def create_bibtex(self):
        """
        create the bibtex file for this pub
        """
        # determine filename
        filename = "./pub2/{0}.bib".format(self.file.identifier)

        with codecs.open(opj(self.working_dir, "_pubs/_templates/citation.bib"), "r", "utf-8") as f:
            bibtex_template = f.read()
        # bibtex_str = bibtex_template.format(**self.file.preamble)
        result = Template(bibtex_template).render(pub=self.file.preamble)

        with codecs.open(opj(self.working_dir, filename), "w", "utf-8") as f:
            f.write(result)

    def create_html(self):
        """
        create the bibtex file for this pub
        """
        # determine filename
        filename = "./pub2/{0}.html".format(self.file.identifier)

        with codecs.open(opj(self.working_dir, "_pubs/_templates/view.html"), "r", "utf-8") as f:
            html_template = f.read()
        # html_str = html_template.format(**self.file.preamble)
        result = Template(html_template).render(pub=self.file.preamble)

        with codecs.open(opj(self.working_dir, filename), "w", "utf-8") as f:
            f.write(result)

    def _render_content(self):
        """
        """
        # env = Environment(loader=PackageLoader('pub', '_layouts'))

        if 'layout' in self.file.preamble and self.file.preamble['layout'] != None:
            layout_filename = "_pubs/_layouts/{0}.tex".format(self.file.preamble['layout'])
            with codecs.open(opj(self.working_dir, layout_filename), "r", "utf-8") as f:
                re_content = r"^---$.*?^---$(.*)"
                m = re.search(re_content, f.read(), re.MULTILINE | re.DOTALL)
                if m:
                    layout_template = Template(m.group(1))
            result = layout_template.render(pub=self.file.preamble, content=self.file.content)
            return(result)
        else:
            return(self.file.content)

    def create_pdf(self):
        """
        create the PDF file for this pub
        """
        # ensure .build directory exists
        if not os.path.exists(opj(self.working_dir, ".build")):
            os.makedirs(opj(self.working_dir, ".build"))

        with codecs.open(opj(self.working_dir, ".build/pub2.tex"), "w", "utf-8") as f:
            f.write(self._render_content())

        basename = os.path.basename(self.file.filename)[:-4]

        # copy assets
        assets_path = opj(self.working_dir, "_pubs/_assets/{0}/".format(basename))
        if os.path.exists(assets_path):
            copy_tree(assets_path, opj(self.working_dir, ".build/"))
        else:
            print("no assets for {0}".format(basename))

        latex_cmd = 'cd {0} && pdflatex pub2.tex'.format(opj(self.working_dir, ".build"))
        bibtex_cmd = 'cd {0} && bibtex pub2.aux'.format(opj(self.working_dir, ".build"))
        biber_cmd = 'cd {0} && biber pub2'.format(opj(self.working_dir, ".build"))

        # run latex
        os.system(latex_cmd)

        # if bibliography
        if "bibtex" in self.file.preamble and self.file.preamble["bibtex"] == True:
            os.system(bibtex_cmd)
            os.system(latex_cmd)
        elif "biber" in self.file.preamble and self.file.preamble["biber"] == True:
            os.system(biber_cmd)
            os.system(latex_cmd)

        os.system(latex_cmd)

        # copy result PDF
        shutil.copy2(
            opj(self.working_dir, ".build/pub2.pdf"),
            opj(self.working_dir, "pub2/{0}.pdf".format(self.file.preamble["identifier"]))
        )

        # create preview
        self._create_preview()

        # clean up
        shutil.rmtree(opj(self.working_dir, ".build"))

    def _create_preview(self):
        """
        create the PNG file for this pub.
        This is called internally after PDF generation, because there is a dependency.
        """
        pdf_filename = opj(
            self.working_dir,
            "pub2/{0}.pdf".format(self.file.preamble["identifier"])
        )
        preview_filename = opj(
            self.working_dir,
            "pub2/{0}.png".format(self.file.preamble["identifier"])
        )
        img = Image(filename='{0}[0]'.format(pdf_filename))
        img.background_color = Color("white")
        img.merge_layers('flatten')
        img.format = 'png'
        img.save(filename=preview_filename)
