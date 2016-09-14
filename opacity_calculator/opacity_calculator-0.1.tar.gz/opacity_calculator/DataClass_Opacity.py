# Author: Ben de Vries
# Contact: bldevries.science@gmail.com
# Web: www.stjerke.com
# Github: https://github.com/bldevries

import 	sys
import 	os
import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt
from operator import itemgetter
import warnings


from DataClass_SQLData import *
from DataClass_OpticalConstants import *
import Calculator_CDE
#import Calculator_MIE

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# CLASS DATA
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
class Opacity(object):

	GRAIN_SHAPES = ["CDE", "MIE"]


	KEY_ID				= "Id"
	KEY_LABEL			= "label"
	
	#KEY_TYPE			= "type" # e.g. "carbon", "fe", "forsterite", "enstatite", "olivine", "pyroxene", "carbonates", "oxides", "sulfides", "ices"
	#KEY_INFO			= "info"
	#KEY_REF				= "ref"
	#KEY_LAT				= "lat"
	#KEY_RHO				= "rho"

	KEY_WAVELENGTH		= "wavelength"
	#KEY_N1				= "N1"
	#KEY_N2				= "N2"
	#EY_N3				= "N3"
	#KEY_K1				= "K1"
	#KEY_K2				= "K2"
	#KEY_K3				= "K3"


	NK_TABLE_NAME = "OpacityTable"
	NK_TABLE_KEY_COL = (KEY_ID, "INTEGER PRIMARY KEY")
	NK_TABLE_COLUMNS = [	(KEY_LABEL, "VARCHAR(200)"), \
#							(KEY_TYPE, "TEXT"), \
#							(KEY_INFO, "TEXT"), \
#							(KEY_REF, "TEXT"), \
#							(KEY_LAT, "TEXT"), \
#							(KEY_RHO, "REAL"), \
							(KEY_WAVELENGTH,"array"), \
#							(KEY_N1, "array"), (KEY_N2, "array"), (KEY_N3, "array"), \
#							(KEY_K1, "array"), (KEY_K2, "array"), (KEY_K3, "array")\
						]

	def __init__(self, SQLITE_DB_FILE_PATH, label, grain_shape, grain_size):#, grain_max_size=None, grain_size_slope=None):

		self.SQLITE_DB_FILE_PATH = SQLITE_DB_FILE_PATH
		
		self.setLabel(label)
		self.setGrainSize(grain_size)

		if grain_shape in self.GRAIN_SHAPES:
		 	self.setGrainShape(grain_shape)
		else:
			self.setGrainShape(None)
		 	warnings.warn("Opacity, constructor: grain shape not in the standard list of possibilities")

		self.setOpticalConstants( OpticalConstants(SQLITE_DB_FILE_PATH = SQLITE_DB_FILE_PATH, label = label) )

		##
		# Check if the optical constants were succesfully found and retrieved
		##
		if not self.getOC().exists():
			warnings.warn("Opacity, optical constants not found for label: "+label)
		else:
			##
			# MAKE AN AMORPHOUS GRAIN
			if self.OC.getLattice() == "a": # len(self.OC.getN2()) == 0:
				##
				# MAKE A CDE GRAIN
				if self.getGrainShape() == "CDE":
					w, o_abs, o_sca, res_cat = Calculator_CDE.makeAmorph(	w=self.OC.getWavelength(), 	\
																			n=self.OC.getN1(), \
																			k=self.OC.getK1(), \
																			rho=self.OC.getRho(), size={"min":self.grain_size, "max":self.grain_size, "slope":1.0})
				##
				# MAKE A MIE GRAIN
				elif self.getGrainShape() == "MIE":
					w, o_abs, o_sca, res_cat = Calculator_MIE.makeAmorph(	w=self.OC.getWavelength(), 	\
																			n=self.OC.getN1(), \
																			k=self.OC.getK1(), \
																			rho=self.OC.getRho(), size={"min":self.grain_size, "max":self.grain_size, "slope":1.0})
				else:
					warnings.warn("Opacity, unknown grain shape: "+str(self.getGrainShape()))
					w, o_sca, o_abs = [], [], []

			##
			# MAKE A CRYSTALLINE GRAIN
			elif self.OC.getLattice() == "c":
				##
				# MAKE A CDE GRAIN
				if self.getGrainShape() == "CDE":
					w, o_abs, o_sca, res_cat = Calculator_CDE.makeCryst(	w=self.OC.getWavelength(), 	\
																			list_n=[self.OC.getN1(), self.OC.getN2(), self.OC.getN3()], \
																			list_k=[self.OC.getK1(),self.OC.getK2(),self.OC.getK3()], \
																			rho=self.OC.getRho(), size={"min":self.grain_size, "max":self.grain_size, "slope":1.0})
				##
				# MAKE A MIE GRAIN
				elif self.getGrainShape() == "MIE":
					w, o_abs, o_sca, res_cat = Calculator_MIE.makeCryst(	w=self.OC.getWavelength(), 	\
																			list_n=[self.OC.getN1(), self.OC.getN2(), self.OC.getN3()], \
																			list_k=[self.OC.getK1(),self.OC.getK2(),self.OC.getK3()], \
																			rho=self.OC.getRho(), size={"min":self.grain_size, "max":self.grain_size, "slope":1.0})
				else:
					warnings.warn("Opacity, unknown grain shape: "+str(self.OC.getGrainShape()))
					w, o_sca, o_abs = [], [], []

			else:
				warnings.warn("Opacity, unknown lattice structure: "+self.OC.getLattice())
				w, o_sca, o_abs = [], [], []


			self.setWavelength(w)
			self.setSca(o_sca)
			self.setAbs(o_abs)


	def setLabel(self, l):
		self.label=l

	def setGrainSize(self, gs):
		self.grain_size = gs

	# def setGrainSizeSlope(self, sl):
	# 	self.

	def setGrainShape(self, sh):
		self.grain_shape = sh

	def setOpticalConstants(self, oc):
		self.OC = oc

	def setWavelength(self,w):
		self.wavelength = w

	def setAbs(self, o_abs):
		self.o_abs = o_abs

	def setSca(self, o_sca):
		self.o_sca = o_sca

	def getWavelength(self,):
		return self.wavelength
	def getW(self):
		return self.wavelength

	def getOC(self):
		return self.OC

	def getAbs(self):
		return self.o_abs

	def getSca(self):
		return self.o_sca

	def getGrainShape(self):
		return self.grain_shape


		# if type(grain_size) == type(0):
		# 	self.grain_size = grain_size
		# 	self.self.max_grain_size = None
		# 	self.slope_grain_size = None
		# elif type(grain_size) == type({}):
		# 	self.grain_size = grain_size["min"]
		# 	self.max_grain_size = grain_size["max"]
		# 	self.slope_grain_size = grain_size["slope"]



