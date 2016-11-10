
import os
from struct import *
import numpy as np

__all__ = ['saveBinTable','loadBinTableType','saveBinTableClass','loadBinTableClass', 'loadBinNdArrayType', 'saveBinString', 'loadBinString', 
		'saveBinNdMatrix', 'loadBinNdArrayMatrix', 'saveBinMatrixClass', 'loadBinMatrixClass', 'loadBinMatrixType']
_path = os.path.dirname(__file__) + "/.."

def saveBinType(fp, value, strDataType):
	"""
	Saves a list of simple type in a binary file
	-----------
	fp : binary file to write
	value : value we want to save
	strDataType : str which describe the data ("i":int, "N": size_t, "d":double, "f":float, "h":short, "I":unsigned int)
	-----------
	"""
	fp.write(pack(strDataType, value))

def loadBinType(fp, strDataType, dataNbByte):
	"""
	Loads a list of simple type with a binary file
	-----------
	fp : binary file to read
	strDataType : str which describe the data ("i":int, "N": size_t, "d":double, "f":float, "h":short, "I":unsigned int)
	dataNbByte : number of bytes of the type
	-----------
	Initialized value corresponding to the binary file
	"""
	nb = unpack(strDataType, fp.read(dataNbByte))[0]
	#print("loadBinType : nb = ",nb)
	return nb

def saveBinTable(fp, tabList, strDataType):
	"""
	Saves a list of simple type in a binary file
	-----------
	fp : binary file to write
	tabList : table of the values we want to save
	strDataType : str which describe the data ("i":int, "N": size_t, "d":double, "f":float, "h":short, "I":unsigned int)
	-----------
	"""
	fp.write(pack("N", len(tabList)))
	for el in tabList:
		fp.write(pack(strDataType, el))

def saveBinNdMatrix(fp, matOfType, strDataType):
	"""
	Saves a list of simple type in a binary file
	-----------
	fp : binary file to write
	tabList : table of the values we want to save
	strDataType : str which describe the data ("i":int, "N": size_t, "d":double, "f":float, "h":short, "I":unsigned int)
	-----------
	"""
	size = matOfType.shape
	nbCol = size[1]
	nbRow = size[0]
	nbEl = nbRow*nbCol
	fp.write(pack("N", nbCol))
	if nbCol == 0:
		return
	fp.write(pack("N", nbRow))
	if nbRow == 0:
		return
	for row in matOfType:
		for el in row:
			fp.write(pack(strDataType, el))

def loadBinTableType(fp, strDataType, dataNbByte):
	"""
	Loads a list of simple type with a binary file
	-----------
	fp : binary file to read
	strDataType : str which describe the data ("i":int, "N": size_t, "d":double, "f":float, "h":short, "I":unsigned int)
	dataNbByte : number of bytes of the type
	-----------
	Initialized list of values corresponding to the binary file
	"""
	tabList = []
	nbEl = unpack("N", fp.read(8))[0]
	#print("loadBinTableType : nbEl = ",nbEl)
	if nbEl == 0:
		return tabList
	for i in range(nbEl):
		el = unpack(strDataType, fp.read(dataNbByte))[0]
		tabList.append(el)
	return tabList

def loadBinNdArrayType(fp, strNumyType, strDataType, dataNbByte):
	"""
	Loads a list of simple type with a binary file
	-----------
	fp : binary file to read
	strNumyType : str which describe the data (np.int32:int, np.int64: size_t, np.float64:double, np.float:float, np.int16:short, np.uint32:unsigned int)
	dataNbByte : number of bytes of the type
	-----------
	Initialized list of values corresponding to the binary file
	"""
	nbEl = unpack("N", fp.read(8))[0]
	tab = np.ndarray(order='C', dtype=np.dtype(strNumyType), shape=(nbEl))
	if nbEl == 0:
		return tab
	for i in range(nbEl):
		el = unpack(strDataType, fp.read(dataNbByte))[0]
		tab[i] = el
	return tab

def loadBinNdArrayMatrix(fp, strNumyType, strDataType, dataNbByte):
	"""
	Loads a matrix of simple type with a binary file
	-----------
	fp : binary file to read
	strNumyType : str which describe the data (np.int32:int, np.int64: size_t, np.float64:double, np.float:float, np.int16:short, np.uint32:unsigned int)
	strDataType : string which describes the data
	dataNbByte : number of bytes of the type
	-----------
	Initialized matrix of values corresponding to the binary file
	"""
	nbCol = unpack("N", fp.read(8))[0]
	#print("loadBinNdArrayMatrix : nbCol = ",nbCol)
	if nbCol == 0 :
		return []
	nbRow = unpack("N", fp.read(8))[0]
	#print("loadBinNdArrayMatrix : nbRow = ",nbRow)
	tab = np.ndarray(order='C', dtype=np.dtype(strNumyType), shape=(nbRow,nbCol))
	if nbRow == 0:
		return tab
	for i in range(nbRow):
		for j in range(nbCol):
			el = unpack(strDataType, fp.read(dataNbByte))[0]
			tab[i][j] = el
	return tab

def saveBinTableClass(fp, tabClass):
	"""
	Saves a list of class in a binary file
	-----------
	fp : binary file to write
	tabClass : table of the class we want to save
	-----------
	"""
	fp.write(pack("N", len(tabClass)))
	for el in tabClass:
		el.saveFp(fp)

def saveBinMatrixClass(fp, matClass):
	"""
	Saves a list of class in a binary file
	-----------
	fp : binary file to write
	matClass : mat of the class we want to save
	-----------
	"""
	size = matClass.shape()
	nbCol = size[1]
	fp.write(pack("N", nbCol))
	if nbCol == 0:
		return;
	nbRow = size[0]
	fp.write(pack("N", nbRow))
	if nbRow == 0:
		return
	nbEl = nbRow*nbCol
	for row in tabClass:
		for col in row:
			el.saveFp(fp)

def loadBinMatrixClass(fp, constructorClass):
	"""
	Loads a list of simple type with a binary file
	-----------
	fp : binary file to read
	constructorClass : constructor function of the class we want to load
	-----------
	Initialized list of class corresponding to the binary file
	"""
	matClass = []
	nbCol = unpack("N", fp.read(8))[0]
	#print("loadBinMatrixClass : nbCol = ",nbCol)
	if nbCol == 0:
		return matClass
	nbRow = unpack("N", fp.read(8))[0]
	#print("loadBinMatrixClass : nbRow = ",nbRow)
	if nbRow == 0:
		return matClass
	for i in range(nbRow):
		tmp = []
		for j in range(nbCol):
			el = constructorClass()
			el.loadFp(fp)
			tmp.append(el)
		matClass.append(tmp)
	return matClass

def loadBinMatrixType(fp, strDataType, dataNbByte):
	"""
	Loads a list of simple type with a binary file
	-----------
	fp : binary file to read
	strDataType : string which describes the data
	dataNbByte : number of bytes of the type
	-----------
	Initialized list of values corresponding to the binary file
	"""
	matClass = []
	nbCol = unpack("N", fp.read(8))[0]
	#print("loadBinMatrixType : nbCol",nbCol)
	if nbCol == 0:
		return matClass
	nbRow = unpack("N", fp.read(8))[0]
	#print("loadBinMatrixType : nbRow",nbRow)
	if nbRow == 0:
		return matClass
	for i in range(nbRow):
		tmp = []
		for j in range(nbCol):
			el = unpack(strDataType, fp.read(dataNbByte))[0]
			tmp.append(el)
		matClass.append(tmp)
	return matClass


def loadBinTableClass(fp, constructorClass):
	"""
	Loads a list of simple type with a binary file
	-----------
	fp : binary file to read
	constructorClass : constructor function of the class we want to load
	-----------
	Initialized list of class corresponding to the binary file
	"""
	tabClass = []
	nbClass = unpack("N", fp.read(8))[0]
	#print("loadBinTableClass : nbClass = ",nbClass)
	if nbClass == 0:
		return tabClass
	for i in range(nbClass):
		el = constructorClass()
		el.loadFp(fp)
		tabClass.append(el)
	return tabClass

def saveBinString(fp, strChar):
	"""
	Saves a string in a binary file
	-----------
	fp : binary file to write
	strChar : string we want to save
	-----------
	"""
	fp.write(pack("N", len(strChar)))
	for ch in strChar:
		#print("ch :",ch)
		fp.write(pack("c", ch.encode()))

def loadBinString(fp):
	"""
	Loads a string with a binary file
	-----------
	fp : binary file to read
	-----------
	Initialized string corresponding to the binary file
	"""
	strChar = ""
	nbChar = unpack("N", fp.read(8))[0]
	for i in range(nbChar):
		ch = unpack("c", fp.read(1))[0].decode()
		strChar += ch
	return strChar

