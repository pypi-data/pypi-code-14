#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
# @date: Thu 23 Jun 2016 10:41:36 CEST


"""
Downloads the VGG model from http://www.robots.ox.ac.uk/~vgg/software/vgg_face/ and paste it on ./bob/ip/caffe_extractor/data

BE SURE THAT YOU HAVE ENOUGH SPACE. THE MODEL HAS MORE THAN 500MB

Usage:
  download_VGG.py download
  download_VGG.py -h | --help
Options:
  -h --help     Show this screen.
"""
from ..VGGFace import VGGFace
from docopt import docopt

def main():

    args = docopt(__doc__)  

    VGGFace.download_vgg()


