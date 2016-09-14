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
import sqlite3 as lite
import io

#from DataClass_Data import Data
from DataClass_SQLData import *


# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# CLASS OpticalConstants
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# This class inherits functions and variables from the SQLData class. See that class for 
# additional information.
class OpticalConstants(SQLData):

	# These are the keys corresponding to the columns in the database
	KEY_LABEL			= "label"	
	KEY_TYPE			= "type" # e.g. "carbon", "fe", "forsterite", "enstatite", "olivine", "pyroxene", "carbonates", "oxides", "sulfides", "ices"
	KEY_INFO			= "info"
	KEY_REF				= "ref"
	KEY_LAT				= "lat"
	KEY_RHO				= "rho"
	KEY_WAVELENGTH		= "wavelength"
	KEY_N1				= "N1"
	KEY_N2				= "N2"
	KEY_N3				= "N3"
	KEY_K1				= "K1"
	KEY_K2				= "K2"
	KEY_K3				= "K3"

	# SQL Table name
	NK_TABLE_NAME = "OpticalConstantsTable"

	# SQL Table column types
	NK_TABLE_COLUMNS = [	(KEY_LABEL, "VARCHAR(200)"), \
							(KEY_TYPE, "TEXT"), \
							(KEY_INFO, "TEXT"), \
							(KEY_REF, "TEXT"), \
							(KEY_LAT, "TEXT"), \
							(KEY_RHO, "REAL"), \
							(KEY_WAVELENGTH,"array"), \
							(KEY_N1, "array"), (KEY_N2, "array"), (KEY_N3, "array"), \
							(KEY_K1, "array"), (KEY_K2, "array"), (KEY_K3, "array")\
						]

	# This is to bookkeep of the optical constants exist in the database
	ocExists = False
	


	# ^^^^^^^^^^^^^^^
	# Constructor
	#
	def __init__(self, SQLITE_DB_FILE_PATH, **kargs):
		
		# Set the path to the SQLite db
		self.SQLITE_DB_FILE_PATH = SQLITE_DB_FILE_PATH

		# You can use the **kargs to search for optical
		# constants. 
		# Construct a search catalogue
		search_cat = {}
		for col in self.NK_TABLE_COLUMNS:
			key = col[0]
			if key in kargs:
				search_cat.update({key: kargs[key]})

		# Use the in super defined function to search and retrieve
		if len(search_cat) != 0:
			sqlDataCat = self.retrieveFromDB(search_cat)

			# Nothing can be found
			if len(sqlDataCat) == 0:
				self.ocExists = False
				warnings.warn("OpticalConstants: Nothing found, empty OpticalConstant object made.")
			else:
				self.ocExists = True

			# Search for keys and values
			for key in sqlDataCat.keys():
				self.setProperty(key, sqlDataCat[key])

		else:
			self.ocExists = False
			for col in self.NK_TABLE_COLUMNS:
				key = col[0]		
				self.setProperty(key, None)


	# ^^^^^^^^^^^^^^^
	# setProperty
	#
	# This function needs to get implemented for the super
	def setProperty(self, key, value):
		if key == self.KEY_ID:
			self.setID(value)
		if key == self.KEY_LABEL:
			self.setLabel(value)

		if key == self.KEY_TYPE:
			self.setType(value)
		if key == self.KEY_INFO:
			self.setInfo(value)
		if key == self.KEY_REF:
			self.setRef(value)
		if key == self.KEY_LAT:
			self.setLattice(value)
		if key == self.KEY_RHO:
			self.setRho(value)

		if key == self.KEY_WAVELENGTH:
			self.setWavelength(value)
		if key == self.KEY_N1:
			self.setN1(value)
		if key == self.KEY_N2:
			self.setN2(value)
		if key == self.KEY_N3:
			self.setN3(value)
		if key == self.KEY_K1:
			self.setK1(value)
		if key == self.KEY_K2:
			self.setK2(value)
		if key == self.KEY_K3:
			self.setK3(value)

	# ^^^^^^^^^^^^^^^
	# set functions for the columns
	#
	def setLabel(self, label):
		self.label = label
	def setType(self, value):
		self.type = value
	def setInfo(self, value):
		self.info = value
	def setRef(self, value):
		self.ref = value
	def setLattice(self, value):
		self.lattice = value
	def setRho(self, value):
		self.rho = value
	def setWavelength(self, w):
		self.wavelength = w
	def setN1(self, n1):
		self.N1 = n1
	def setN2(self, n2):
		self.N2 = n2
	def setN3(self, n3):
		self.N3 = n3
	def setK1(self, k1):
		self.K1 = k1
	def setK2(self, k2):
		self.K2 = k2
	def setK3(self, k3):
		self.K3 = k3


	# ^^^^^^^^^^^^^^^
	# set a property using its key
	#
	def getProperty(self, key):
		if key == self.KEY_ID:
			return self.getID()
		if key == self.KEY_LABEL:
			return self.getLabel()

		if key == self.KEY_TYPE:
			return self.getType()
		if key == self.KEY_INFO:
			return self.getInfo()
		if key == self.KEY_REF:
			return self.getRef()
		if key == self.KEY_LAT:
			return self.getLattice()
		if key == self.KEY_RHO:
			return self.getRho()

		if key == self.KEY_WAVELENGTH:
			return self.getWavelength()
		if key == self.KEY_N1:
			return self.getN1()
		if key == self.KEY_N2:
			return self.getN2()
		if key == self.KEY_N3:
			return self.getN3()
		if key == self.KEY_K1:
			return self.getK1()
		if key == self.KEY_K2:
			return self.getK2()
		if key == self.KEY_K3:
			return self.getK3()


	# ^^^^^^^^^^^^^^^
	# get functions for the columns
	#
	def getLabel(self):
		return self.label
	def getType(self):
		return self.type
	def getInfo(self):
		return self.info
	def getRef(self):
		return self.ref
	def getLattice(self):
		return self.lattice
	def getRho(self):
		return self.rho
	def getWavelength(self):
		return self.wavelength
	def getN1(self):
		return self.N1
	def getN2(self):
		return self.N2
	def getN3(self):
		return self.N3
	def getK1(self):
		return self.K1
	def getK2(self):
		return self.K2
	def getK3(self):
		return self.K3

	# ^^^^^^^^^^^^^^^
	# Check if the optical constants exist
	#
	def exists(self):
		return self.ocExists
