#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

# keep in sync with main.py (!)
version = "0.2.3"
desc = "Realtime-visualization of TCP flows logged by TCPlog."

setup(
        name = "tcpliveplot",
        packages = [
            "tcpliveplot",
            "tcpliveplot.utils",
            "tcpliveplot.backends",
            "tcpliveplot.backends.gui",
            "tcpliveplot.backends.input"
            ],
        entry_points = {
            "console_scripts": [
                'tcpliveplot = tcpliveplot.main:main'
                ],
            "gui_scripts": [
                'tcpliveplot = tcpliveplot.main:main'
                ]
            },

        version = version,
        description = desc,
        long_description = desc,
        author = "Karlsruhe Institute of Technology - Institute of Telematics",
        author_email = "telematics@tm.kit.edu",
        maintainer = "Michael Koenig",
        maintainer_email = "michael.koenig2@student.kit.edu",
        url = "https://git.scc.kit.edu/CPUnetLOG/TCPlivePLOT/",
        license = "BSD",
        platforms = "Linux",
        zip_safe = False,
        install_requires = [
            'matplotlib==1.4.2',
            'tcplog>=0.2.8'
            ],
        keywords = ['tcp', 'flow', 'plot', 'visualize', 'graph', 'live', 'analyze', 'network', 'traffic'],
        classifiers = [
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Operating System :: POSIX :: Linux',
            'Natural Language :: English',
            'Intended Audience :: Education',
            'Intended Audience :: Information Technology',
            'Intended Audience :: Science/Research',
            'Intended Audience :: System Administrators',
            'Intended Audience :: Telecommunications Industry',
            'Topic :: Scientific/Engineering',
            'Topic :: Internet',
            'Topic :: System :: Logging',
            'Topic :: System :: Networking',
            'Topic :: System :: Networking :: Monitoring',
            'Topic :: System :: Operating System Kernels :: Linux',
            'Topic :: Utilities'
            ]
        )
