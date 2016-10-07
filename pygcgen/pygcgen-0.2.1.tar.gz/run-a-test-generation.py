# -*- coding: utf-8 -*-


from pygcgen import ChangelogGenerator
from pygcgen.__main__ import run_gui

# run_gui()
# exit()

options = [
    # "-h",
    #"--options-file", ".pygcgen_example",
    # "-u", "skywinder",
    # "-p", "ActionSheetPicker-3.0",
    # '-s', "**Questions:**", "question", "Question",
    # '-s', "**Future-Requests:**", "feature-request",
    # '--section', '**Important changes:**', 'notice',
    # '-s', "**Implemented enhancements:**", "enhancement", "Enhancement",
    # '-s', "**Fixed bugs:**", "bug", "Bug",
    # "-v",
    # "--quiet",
    "--no-overwrite",
    #"--between-tags", "v5.1.1",# "v0.1.1",
    "--with-unreleased",
    #"--future-release", "v0.2.0",
    "--exclude-labels", "duplicate", "Duplicate",
                        "invalid", "Invalid",
                        "wontfix", "Wontfix",
                        "question", "Question",
                        "hide in changelog",
    #"--tag-separator", " ---\n\n",
]

chagen = ChangelogGenerator(options)
chagen.run()
