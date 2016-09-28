# -*- coding: utf-8 -*-
# Pub2 (c) 2016 Ian Dennis Miller

import tempfile
import os
from shutil import rmtree
from nose.plugins.attrib import attr
from unittest import TestCase
from .pub2 import Pub2
from .file import File
from .reader import Reader
from .writer import Writer
from os.path import join as opj


CLEANUP = False
# WORKING_DIR = opj("/tmp", "pub2")
WORKING_DIR = opj(tempfile.gettempdir(), "pub2")


class Pub2TestSuite(TestCase):
    def setUp(self):
        self.working_dir = WORKING_DIR
        self.p = Pub2(self.working_dir)

    def tearDown(self):
        if CLEANUP:
            try:
                rmtree("/tmp/pub2")
            except OSError:
                pass

    def test_init_folders(self):
        self.assertIsNotNone(self.p)
        self.p.init_folders()

    def test_finding(self):
        self.p.init_folders()
        file_list = self.p.find_files()
        self.assertGreater(len(file_list), 0)
        changed_files = self.p.detect_changed_files()
        self.assertGreater(len(changed_files), 0)

    def test_json_digest(self):
        self.p.init_folders()
        self.p.create_json_digest()
        self.assertTrue(os.path.isfile(opj(self.working_dir, "_data", "pub2.json")))

    def test_template(self):
        self.p.init_folders()
        self.p.create_from_template(author="Ian", title="Meme Pounder", year=2017)
        self.assertTrue(os.path.isfile(opj(self.working_dir, "_pubs", "meme-pounder.tex")))

    def test_checksum(self):
        self.p.init_folders()
        self.assertIsNone(self.p.get_checksum())

    @attr("slow")
    def test_build(self):
        self.p.init_folders()
        self.p.build()

    def test_file_load(self):
        self.p.init_folders()
        file_list = self.p.find_files()
        first_file = file_list[0]
        f = self.p.load_file(first_file)
        self.assertIsNotNone(f)

    def test_ensure_paths(self):
        self.assertTrue(os.path.isdir(opj(self.working_dir, "pub2")))


class FileTestSuite(TestCase):
    def setUp(self):
        self.working_dir = WORKING_DIR

        p = Pub2(self.working_dir)
        p.init_folders()
        self.p = p

        file_list = self.p.find_files()
        first_file = file_list[0]
        self.f = self.p.load_file(first_file)

    def tearDown(self):
        if CLEANUP:
            try:
                rmtree("/tmp/pub2")
            except OSError:
                pass

    def testFileLoad(self):
        file_list = self.p.find_files()
        first_file = file_list[0]
        # load it directly, not via pub2.load_file
        f = File(self.p, first_file)
        self.assertIsNotNone(f)

    def testReader(self):
        self.assertIsNotNone(self.f.preamble)
        self.assertIsNotNone(self.f.content)
        self.assertIsNotNone(self.f.identifier)

    def testRender(self):
        self.assertIsNotNone(self.f.writer._render_content())

    def testCreateBibtex(self):
        self.f.writer.create_bibtex()
        self.assertTrue(os.path.isfile(opj(self.working_dir, "pub2", "miller_first_2016.bib")))

    @attr("slow")
    def testCreatePdf(self):
        self.f.writer.create_pdf()
        self.assertTrue(os.path.isfile(opj(self.working_dir, "pub2", "miller_first_2016.pdf")))
        self.assertTrue(os.path.isfile(opj(self.working_dir, "pub2", "miller_first_2016.png")))

    def testCreateHtml(self):
        self.f.writer.create_html()
        self.assertTrue(os.path.isfile(opj(self.working_dir, "pub2", "miller_first_2016.html")))
