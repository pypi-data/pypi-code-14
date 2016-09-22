#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Hannah Muckenhirn <hannah.muckenhirn@idiap.ch>
# Fri April  1 14:24:21 CEST 2016
#
# Copyright (C) 2012-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup, dist

dist.Distribution(dict(setup_requires=['bob.extension']))

from bob.extension.utils import load_requirements, find_packages

install_requires = load_requirements()

setup(
    name='bob.paper.biosig2016',
    version=open("version.txt").read().rstrip(),
    description='Presentation Attack Detection Using Long Term Spectral Statistics for Trustworthy Speaker Verification',
    url='',
    license='GPLv3',
    keywords = "Speaker verification, Spoofing, Long Term Spectral Statistics",
    author='Hannah Muckenhirn',
    author_email='hannah.muckenhirn@idiap.ch',
    long_description=open('README.rst').read(),

    # This line is required for any distutils based packaging.
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
   
    install_requires=install_requires,
    
    entry_points={
      'console_scripts': [
        'evaluate_pad.py                    = bob.paper.biosig2016.script.evaluate_pad:main',
        'compute_EER_perattack_eval.py      = bob.paper.biosig2016.script.compute_EER_perattack_eval:main',
        'spoof_mlp.py                       = bob.paper.biosig2016.script.spoof_mlp:main',
        ], 
       'bob.pad.database': [
        'avspoof-detect-physical            = bob.paper.biosig2016.config.database.avspoof_detect_physical:database',
        'asvspoof-cm                        = bob.paper.biosig2016.config.database.asvspoof_cm:database',
       ],
       'bob.pad.algorithm': [
         'lda                               = bob.paper.biosig2016.algorithm.lda:algorithm',
         'mlp-sigmoid-200-neurons-stoch     = bob.paper.biosig2016.config.algorithm.mlp_sigmoid_200_neurons_stoch:algorithm',
      ],
       'bob.pad.extractor': [
        'mean-spectrum-32ms                 = bob.paper.biosig2016.config.extractor.mean_spectrum_32ms:extractor',
        'mean-std-spectrum-32ms             = bob.paper.biosig2016.config.extractor.mean_std_spectrum_32ms:extractor',
        'std-spectrum-32ms                  = bob.paper.biosig2016.config.extractor.std_spectrum_32ms:extractor',
        'mean-std-spectrum-256ms            = bob.paper.biosig2016.config.extractor.mean_std_spectrum_256ms_shift_10ms:extractor',
   ],
       'bob.pad.preprocessor': [
        'energy-2gauss-remove-head-tail     = bob.paper.biosig2016.config.preprocessor.energy_2gauss_remove_head_tail:preprocessor',
        'none                               = bob.paper.biosig2016.config.preprocessor.no_preprocessing:preprocessor',
        
      ],
      'bob.pad.grid': [
        'normal                             = bob.paper.biosig2016.config.grid.normal:grid',
      ],
      },


    classifiers = [
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ],
)
