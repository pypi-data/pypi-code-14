#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Artur Costa Pazo <acosta@gradiant.org>

import numpy
import bob.io.base
import os

"""Class for manage the scores of the ReplayMobile database
"""

class ScoresReplayMobile(object):

  label = ''
  devel_real = numpy.array([])
  devel_attacks = numpy.array([])
  devel_attacks_mattescreen = numpy.array([])
  devel_attacks_mattescreen_photo = numpy.array([])
  devel_attacks_mattescreen_video = numpy.array([])
  devel_attacks_print  = numpy.array([])
  devel_attacks_print_fixed = numpy.array([])
  devel_attacks_print_hand = numpy.array([])
  test_real = numpy.array([])
  test_attacks = numpy.array([])
  test_attacks_mattescreen = numpy.array([])
  test_attacks_mattescreen_photo = numpy.array([])
  test_attacks_mattescreen_video = numpy.array([])
  test_attacks_print  = numpy.array([])
  test_attacks_print_fixed = numpy.array([])
  test_attacks_print_hand = numpy.array([])

  def __str__(self):
    info =  "ScoresReplayMobile *****************************************************" + '\n'
    info += " devel:\n"
    info += "  |-> real    :" + str(len(self.devel_real)) + '\n'
    info += "  |-> attacks :" + str(len(self.devel_attacks)) + '\n'
    info += "  	   |-> mattescreeen :" + str(len(self.devel_attacks_mattescreen)) + '\n'
    info += "  	           |-> mattescreen_photo :" + str(len(self.devel_attacks_mattescreen_photo)) + '\n'
    info += "  	           |-> mattescreen_video :" + str(len(self.devel_attacks_mattescreen_video)) + '\n'
    info += "  	   |-> print        :" + str(len(self.devel_attacks_print)) + '\n'
    info += "  	           |-> print_fixed :" + str(len(self.devel_attacks_print_fixed)) + '\n'
    info += "  	           |-> print_hand  :" + str(len(self.devel_attacks_print_hand)) + '\n'
    info += " test:\n"
    info += "  |-> real    :" + str(len(self.test_real)) + '\n'
    info += "  |-> attacks :" + str(len(self.test_attacks)) + '\n'
    info += "  	   |-> mattescreeen :" + str(len(self.test_attacks_mattescreen)) + '\n'
    info += "  	           |-> mattescreen_photo :" + str(len(self.test_attacks_mattescreen_photo)) + '\n'
    info += "  	           |-> mattescreen_video :" + str(len(self.test_attacks_mattescreen_video)) + '\n'
    info += "  	   |-> print        :" + str(len(self.test_attacks_print)) + '\n'
    info += "  	           |-> print_fixed :" + str(len(self.test_attacks_print_fixed)) + '\n'
    info += "  	           |-> print_hand  :" + str(len(self.test_attacks_print_hand)) + '\n'
    info += "************************************************************************" + '\n'
    return info
 
  def __init__(self):
    pass

  def save(self,path):
      """This function save info"""
      fout = bob.io.base.HDF5File(path, 'w')
      fout.create_group('devel')
      fout.cd('devel')
      fout.set('real', self.devel_real)
      fout.create_group('mattescreen-photo')
      fout.cd('mattescreen-photo')
      if self.devel_attacks_mattescreen_photo.size > 0:
        fout.set('attack', self.devel_attacks_mattescreen_photo)
      fout.cd('..')
      fout.create_group('mattescreen-video')
      fout.cd('mattescreen-video')
      if self.devel_attacks_mattescreen_video.size > 0:
        fout.set('attack', self.devel_attacks_mattescreen_video)
      fout.cd('..')
      fout.create_group('print-fixed')
      fout.cd('print-fixed')
      if self.devel_attacks_print_fixed.size > 0:
        fout.set('attack', self.devel_attacks_print_fixed)
      fout.cd('..')
      fout.create_group('print-hand')
      fout.cd('print-hand')
      if self.devel_attacks_print_hand.size > 0:
        fout.set('attack', self.devel_attacks_print_hand)
      fout.cd('..')
      fout.cd('..')
      fout.create_group('test')
      fout.cd('test')
      fout.set('real', self.test_real)
      fout.create_group('mattescreen-photo')
      fout.cd('mattescreen-photo')
      if self.test_attacks_mattescreen_photo.size > 0:
        fout.set('attack', self.test_attacks_mattescreen_photo)
      fout.cd('..')
      fout.create_group('mattescreen-video')
      fout.cd('mattescreen-video')
      if self.test_attacks_mattescreen_video.size > 0:
        fout.set('attack', self.test_attacks_mattescreen_video)
      fout.cd('..')
      fout.create_group('print-fixed')
      fout.cd('print-fixed')
      if self.test_attacks_print_fixed.size > 0:
        fout.set('attack', self.test_attacks_print_fixed)
      fout.cd('..')
      fout.create_group('print-hand')
      fout.cd('print-hand')
      if self.test_attacks_print_hand.size > 0:
        fout.set('attack', self.test_attacks_print_hand)
      fout.cd('..')
      fout.cd('..')

  def load(self,path):
      """This function loads info"""
      fin = bob.io.base.HDF5File(os.path.join(path), 'r')
      if fin.has_group('devel'):
        fin.cd('devel')
        self.devel_real = fin.get('real')
        if fin.has_group('mattescreen-photo'):
          fin.cd('mattescreen-photo')
          self.devel_attacks_mattescreen_photo = fin.get('attack')
          fin.cd('..')
        if fin.has_group('mattescreen-video'):
          fin.cd('mattescreen-video')
          self.devel_attacks_mattescreen_video = fin.get('attack')
          fin.cd('..')
        if fin.has_group('print-fixed'):
          fin.cd('print-fixed')
          self.devel_attacks_print_fixed = fin.get('attack')
          fin.cd('..')
        if fin.has_group('print-hand'):
          fin.cd('print-hand')
          self.devel_attacks_print_hand = fin.get('attack')
          fin.cd('..')
        self.devel_attacks_mattescreen = numpy.concatenate((self.devel_attacks_mattescreen_photo,self.devel_attacks_mattescreen_video))
        self.devel_attacks_print = numpy.concatenate((self.devel_attacks_print_fixed,self.devel_attacks_print_hand))
        self.devel_attacks = numpy.concatenate((self.devel_attacks_mattescreen,self.devel_attacks_print))
      fin.cd('..')
      if fin.has_group('test'):
        fin.cd('test')
        self.test_real = fin.get('real')
        if fin.has_group('mattescreen-photo'):
          fin.cd('mattescreen-photo')
          self.test_attacks_mattescreen_photo = fin.get('attack')
          fin.cd('..')
        if fin.has_group('mattescreen-video'):
          fin.cd('mattescreen-video')
          self.test_attacks_mattescreen_video = fin.get('attack')
          fin.cd('..')
        if fin.has_group('print-fixed'):
          fin.cd('print-fixed')
          self.test_attacks_print_fixed = fin.get('attack')
          fin.cd('..')
        if fin.has_group('print-hand'):
          fin.cd('print-hand')
          self.test_attacks_print_hand = fin.get('attack')
          fin.cd('..')
        self.test_attacks_mattescreen = numpy.concatenate((self.test_attacks_mattescreen_photo,self.test_attacks_mattescreen_video))
        self.test_attacks_print = numpy.concatenate((self.test_attacks_print_fixed,self.test_attacks_print_hand))
        self.test_attacks = numpy.concatenate((self.test_attacks_mattescreen,self.test_attacks_print))
      fin.cd('..')
      

  def purgeNaN(self):
    self.devel_real                      = self.devel_real[~numpy.isnan(self.devel_real)]
    self.devel_attacks                   = self.devel_attacks[~numpy.isnan(self.devel_attacks)]
    self.devel_attacks_mattescreen       = self.devel_attacks_mattescreen[~numpy.isnan(self.devel_attacks_mattescreen)]
    self.devel_attacks_mattescreen_photo = self.devel_attacks_mattescreen_photo[~numpy.isnan(self.devel_attacks_mattescreen_photo)]
    self.devel_attacks_mattescreen_video = self.devel_attacks_mattescreen_video[~numpy.isnan(self.devel_attacks_mattescreen_video)]
    self.devel_attacks_print             = self.devel_attacks_print[~numpy.isnan(self.devel_attacks_print)]
    self.devel_attacks_print_fixed       = self.devel_attacks_print_fixed[~numpy.isnan(self.devel_attacks_print_fixed)]
    self.devel_attacks_print_hand        = self.devel_attacks_print_hand[~numpy.isnan(self.devel_attacks_print_hand)]
    self.test_real                       = self.test_real[~numpy.isnan(self.test_real)]
    self.test_attacks                    = self.test_attacks[~numpy.isnan(self.test_attacks)]
    self.test_attacks_mattescreen        = self.test_attacks_mattescreen[~numpy.isnan(self.test_attacks_mattescreen)]
    self.est_attacks_mattescreen_photo   = self.test_attacks_mattescreen_photo[~numpy.isnan(self.test_attacks_mattescreen_photo)]
    self.test_attacks_mattescreen_video  = self.test_attacks_mattescreen_video[~numpy.isnan(self.test_attacks_mattescreen_video)]
    self.test_attacks_print              = self.test_attacks_print[~numpy.isnan(self.test_attacks_print)]
    self.test_attacks_print_fixed        = self.test_attacks_print_fixed[~numpy.isnan(self.test_attacks_print_fixed)]
    self.test_attacks_print_hand         = self.test_attacks_print_hand[~numpy.isnan(self.test_attacks_print_hand)]

  def loadFromIdiapFile(self,path):
    fin = bob.io.base.HDF5File(os.path.join(path), 'r')
    if fin.has_group('devel'):
       fin.cd('devel')
       self.devel_real = fin.get('real')
       if fin.has_group('mattescreen_fixed'):
         fin.cd('mattescreen_fixed')
         self.devel_attacks_mattescreen = fin.get('attack')
         fin.cd('..')
       if fin.has_group('print_fixed'):
         fin.cd('print_fixed')
         self.devel_attacks_print_fixed = fin.get('attack')
         fin.cd('..')
       if fin.has_group('print_hand'):
         fin.cd('print_hand')
         self.devel_attacks_print_hand = fin.get('attack')
         fin.cd('..')
       self.devel_attacks_print = numpy.concatenate((self.devel_attacks_print_fixed,self.devel_attacks_print_hand))
       fin.cd('..')
       self.devel_attacks = numpy.concatenate((self.devel_attacks_mattescreen,self.devel_attacks_print))
    if fin.has_group('test'):
       fin.cd('test')
       self.test_real = fin.get('real')
       if fin.has_group('mattescreen_fixed'):
         fin.cd('mattescreen_fixed')
         self.test_attacks_mattescreen = fin.get('attack')
         fin.cd('..')
       if fin.has_group('print_fixed'):
         fin.cd('print_fixed')
         self.test_attacks_print_fixed = fin.get('attack')
         fin.cd('..')
       if fin.has_group('print_hand'):
         fin.cd('print_hand')
         self.test_attacks_print_hand = fin.get('attack')
         fin.cd('..')
       self.test_attacks_print = numpy.concatenate((self.test_attacks_print_fixed,self.test_attacks_print_hand))
       fin.cd('..')
       self.test_attacks = numpy.concatenate((self.test_attacks_mattescreen,self.test_attacks_print))

  def setValues(self, devel_real, 
		     devel_attacks,
		     devel_attacks_mattescreen,
	             devel_attacks_mattescreen_photo,
		     devel_attacks_mattescreen_video,
                     devel_attacks_print,
		     devel_attacks_print_fixed,
		     devel_attacks_print_hand,
		     test_real, 
  		     test_attacks,
		     test_attacks_mattescreen,
	             test_attacks_mattescreen_photo,
		     test_attacks_mattescreen_video,
                     test_attacks_print,
		     test_attacks_print_fixed,
		     test_attacks_print_hand,
 		     ): 
    self.devel_real = devel_real
    self.devel_attacks = devel_attacks
    self.devel_attacks_mattescreen = devel_attacks_mattescreen
    self.devel_attacks_mattescreen_photo = devel_attacks_mattescreen_photo
    self.devel_attacks_mattescreen_video = devel_attacks_mattescreen_video
    self.devel_attacks_print  = devel_attacks_print
    self.devel_attacks_print_fixed = devel_attacks_print_fixed
    self.devel_attacks_print_hand = devel_attacks_print_hand
    self.test_real = test_real
    self.test_attacks = test_attacks
    self.test_attacks_mattescreen = test_attacks_mattescreen
    self.test_attacks_mattescreen_photo = test_attacks_mattescreen_photo
    self.test_attacks_mattescreen_video = test_attacks_mattescreen_video
    self.test_attacks_print  = test_attacks_print
    self.test_attacks_print_fixed = test_attacks_print_fixed
    self.test_attacks_print_hand = test_attacks_print_hand
