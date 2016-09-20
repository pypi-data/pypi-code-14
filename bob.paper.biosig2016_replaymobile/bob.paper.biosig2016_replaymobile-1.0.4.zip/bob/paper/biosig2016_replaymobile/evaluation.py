#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Artur Costa Pazo <acosta@gradiant.org>

import numpy
import bob.io.base
import os
from matplotlib import pyplot 
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.font_manager

""" Methods for evaluation
"""

def calc_apcer(list_attacks,threshold):
  result_attacks = []
  for attacks in list_attacks:
    array_attacks = numpy.array(attacks)
    result = array_attacks[array_attacks>=threshold].shape[0]/float(len(attacks))
    result_attacks.append(result)
  return 100*max(result_attacks) 

def calc_bpcer(genuines,threshold):
  array_genuines = numpy.array(genuines)
  bpcer = array_genuines[array_genuines<threshold].shape[0]
  return 100*bpcer/float(len(genuines)) 

def calc_acer(apcer,bpcer):
  return (apcer + bpcer)/2

def getEER(real,attack):
  thresEER_dev = bob.measure.eer_threshold(attack, real)
  far, frr = bob.measure.farfrr(attack, real, thresEER_dev)
  eer = (100*far + 100*frr)/2 
  return eer

def evaluate_systems(list_systems, swap_subset = False):
  table = []
  from tabulate import tabulate
  headers = ["EER (dev)","HTER (grandtest)","EER (mp)","HTER (mp)","EER (mv)","HTER (mv)","EER (ph)","HTER (ph)","EER (pf)","HTER (pf)","APCER","BPCER","ACER"]

  for system in list_systems:
      if swap_subset==True:
       devel_real                       = system.test_real
       devel_attacks                    = system.test_attacks
       devel_attacks_mattescreen        = system.test_attacks_mattescreen
       devel_attacks_mattescreen_photo  = system.test_attacks_mattescreen_photo
       devel_attacks_mattescreen_video  = system.test_attacks_mattescreen_video
       devel_attacks_print              = system.test_attacks_print
       devel_attacks_print_fixed        = system.test_attacks_print_fixed
       devel_attacks_print_hand         = system.test_attacks_print_hand
       test_real                        = system.devel_real
       test_attacks                     = system.devel_attacks
       test_attacks_mattescreen         = system.devel_attacks_mattescreen
       test_attacks_mattescreen_photo   = system.devel_attacks_mattescreen_photo
       test_attacks_mattescreen_video   = system.devel_attacks_mattescreen_video
       test_attacks_print               = system.devel_attacks_print
       test_attacks_print_fixed         = system.devel_attacks_print_fixed
       test_attacks_print_hand          = system.devel_attacks_print_hand
      else: 
       devel_real                      = system.devel_real
       devel_attacks                   = system.devel_attacks
       devel_attacks_mattescreen       = system.devel_attacks_mattescreen
       devel_attacks_mattescreen_photo = system.devel_attacks_mattescreen_photo
       devel_attacks_mattescreen_video = system.devel_attacks_mattescreen_video
       devel_attacks_print             = system.devel_attacks_print
       devel_attacks_print_fixed       = system.devel_attacks_print_fixed
       devel_attacks_print_hand        = system.devel_attacks_print_hand
       test_real                       = system.test_real
       test_attacks                    = system.test_attacks
       test_attacks_mattescreen        = system.test_attacks_mattescreen
       test_attacks_mattescreen_photo  = system.test_attacks_mattescreen_photo
       test_attacks_mattescreen_video  = system.test_attacks_mattescreen_video
       test_attacks_print              = system.test_attacks_print
       test_attacks_print_fixed        = system.test_attacks_print_fixed
       test_attacks_print_hand         = system.test_attacks_print_hand

      #devel
      thresEER_dev = bob.measure.eer_threshold(devel_attacks, devel_real)
      print 'thresEER_dev (grandtest):', thresEER_dev
      dev_far, dev_frr = bob.measure.farfrr(devel_attacks, devel_real, thresEER_dev)
      eer_hter_devel = (100*dev_far + 100*dev_frr)/2

      #devel
      eer_mp = getEER(devel_real,devel_attacks_mattescreen_photo)
      eer_mv = getEER(devel_real,devel_attacks_mattescreen_video)
      eer_ph = getEER(devel_real,devel_attacks_print_hand)
      eer_pf = getEER(devel_real,devel_attacks_print_fixed)
      
      #test (grandtest)
      thresEER_test = bob.measure.eer_threshold(test_attacks, test_real)
      test_far_eer, test_frr_eer = bob.measure.farfrr(test_attacks,test_real, thresEER_test)
      test_far, test_frr = bob.measure.farfrr(test_attacks, test_real, thresEER_dev)
      eer_test  = (100*test_far_eer + 100*test_frr_eer)/2 
      hter_test = (100*test_far + 100*test_frr)/2

      #test (mattescreeen photo)
      test_far_mattescreen_photo, test_frr_mattescreen_photo = bob.measure.farfrr(test_attacks_mattescreen_photo, test_real, thresEER_dev)
      hter_test_mattescreen_photo = (100*test_far_mattescreen_photo + 100*test_frr_mattescreen_photo)/2

      #test (mattescreeen video)
      test_far_mattescreen_video, test_frr_mattescreen_video = bob.measure.farfrr(test_attacks_mattescreen_video, test_real, thresEER_dev)
      hter_test_mattescreen_video = (100*test_far_mattescreen_video + 100*test_frr_mattescreen_video)/2

      #test (print_fixed)
      test_far_print_fixed, test_frr_print_fixed = bob.measure.farfrr(test_attacks_print_fixed, test_real, thresEER_dev)
      hter_test_print_fixed = (100*test_far_print_fixed + 100*test_frr_print_fixed)/2

      #test (print_hand)
      test_far_print_hand, test_frr_print_hand = bob.measure.farfrr(test_attacks_print_hand, test_real, thresEER_dev)
      hter_test_print_hand = (100*test_far_print_hand + 100*test_frr_print_hand)/2

      #Calculate ACER, APCER , BPCER
      list_attacks = []
      list_attacks.append(test_attacks_mattescreen_photo)
      list_attacks.append(test_attacks_mattescreen_video)
      list_attacks.append(test_attacks_print_fixed)
      list_attacks.append(test_attacks_print_hand)
    
      apcer = calc_apcer(list_attacks,thresEER_dev)
      npcer = calc_bpcer(test_real,thresEER_dev)
      acer  = calc_acer(apcer,npcer)

      system_info = [system.label]
      system_info.append('%.2f%%' % (eer_hter_devel))
      system_info.append('%.2f%%' % (hter_test))
      system_info.append('%.2f%%' % (eer_mp))
      system_info.append('%.2f%%' % (hter_test_mattescreen_photo))
      system_info.append('%.2f%%' % (eer_mv))
      system_info.append('%.2f%%' % (hter_test_mattescreen_video))
      system_info.append('%.2f%%' % (eer_ph))
      system_info.append('%.2f%%' % (hter_test_print_hand))
      system_info.append('%.2f%%' % (eer_pf))
      system_info.append('%.2f%%' % (hter_test_print_fixed))
      system_info.append('%.2f%%' % (apcer))
      system_info.append('%.2f%%' % (npcer))
      system_info.append('%.2f%%' % (acer))
      table.append(system_info) 
      
      system_info = [system.label]
      system_info.append('%.2f%%' % (eer_hter_devel))
      system_info.append('%.2f%%' % (hter_test))

  txt_fancy_grid = tabulate(table,headers,tablefmt="fancy_grid")
  return txt_fancy_grid

def plot_curves(output,filename,title,system, swap_subset = False):
#   print output, filename, title
  if swap_subset==True:
    devel_real                     = system.test_real
    devel_attacks                  = system.test_attacks
    test_real                      = system.devel_real
    test_attacks                   = system.devel_attacks
    test_attacks_mattescreen       = system.devel_attacks_mattescreen
    test_attacks_mattescreen_photo = system.devel_attacks_mattescreen_photo
    test_attacks_mattescreen_video = system.devel_attacks_mattescreen_video
    test_attacks_print             = system.devel_attacks_print
    test_attacks_print_fixed       = system.devel_attacks_print_fixed
    test_attacks_print_hand        = system.devel_attacks_print_hand
  else: 
    devel_real                     = system.devel_real
    devel_attacks                  = system.devel_attacks
    test_real                      = system.test_real
    test_attacks                   = system.test_attacks
    test_attacks_mattescreen       = system.test_attacks_mattescreen
    test_attacks_mattescreen_photo = system.test_attacks_mattescreen_photo
    test_attacks_mattescreen_video = system.test_attacks_mattescreen_video
    test_attacks_print             = system.test_attacks_print
    test_attacks_print_fixed       = system.test_attacks_print_fixed
    test_attacks_print_hand        = system.test_attacks_print_hand
     
  outfile_eps = os.path.join(output, filename)
  fname, extn = os.path.splitext(outfile_eps)
  outfile_pdf= fname+'.pdf'
  print 'pdf file:', outfile_pdf
  with PdfPages(outfile_pdf) as pdf: 
      fig = pyplot.figure()
      line_width = 2
      bob.measure.plot.roc(test_attacks_mattescreen_photo, test_real, 150, color=(0,0,0), linestyle='-',marker='x', markeredgewidth=2,linewidth=line_width, label='mattescreen-photo') 
      bob.measure.plot.roc(test_attacks_mattescreen_video, test_real, 150, color=(0.6,0.3,0), linestyle='-', marker='^', linewidth=line_width, label='mattescreen-video') 
      bob.measure.plot.roc(test_attacks_print_fixed, test_real, 150, color=(0.2,0.2,1), linestyle='-', linewidth=line_width, label='print-fixed') 
      bob.measure.plot.roc(test_attacks_print_hand, test_real, 150, color=(0,1,0), linestyle='-', marker='s',linewidth=line_width, label='print-hand') 
      bob.measure.plot.roc(test_attacks, test_real, 150, color=(1,0,0), linestyle='-', linewidth=line_width, marker='o', label='Grandtest') 
    
      pyplot.xlabel('FAR (%)') 
      pyplot.ylabel('FRR (%)') 
      pyplot.grid(True) 
      pyplot.axis('tight')
      pyplot.xlim((0, 50))
      pyplot.ylim((0, 50))
      pyplot.legend(bbox_to_anchor=(1.05, 1), loc=1, borderaxespad=0.)
      pyplot.title( title )
      
      pdf.savefig()
      print("Plot saved in: %s" %outfile_eps)
      fig.savefig(outfile_eps)
      
  
