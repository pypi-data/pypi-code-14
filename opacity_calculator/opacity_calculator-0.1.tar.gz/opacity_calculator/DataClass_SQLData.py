# Author: Ben de Vries
# Contact: bldevries.science@gmail.com
# Web: www.stjerke.com
# Github: https://github.com/bldevries

import 	sys
import 	os
import numpy as np
#import scipy.interpolate
#import matplotlib.pyplot as plt
#from operator import itemgetter
import warnings
import sqlite3 as lite
import io


# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# CLASS OpticalConstants
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
#
# This class is used by objects that need to be saved to an SQLite database.
# This class implements two instance methods (insertIntoDB, retrieveFromDB) to store and retrieve 
# data. This class also implements three class methods (getColumnNamesInList, getColumnInTable, 
# getColumnNamesInString) to retrieve basic table information.
#
#
# Instruction to inherit this class. Declare the class as 
# DataClass_SomeDataToStore(SQLData)
# Then implement the following functions and variables:
#  - Implement a variable holding the name of the SQLite database on disk
#		NK_TABLE_NAME = "Somedatabase.db"
#  - A variable and corresponding set and get functions for every column:
#		KEY_COLUMNNAME = "example_col_name"
#		def getColumnName(self){..} 
#		def setColumnName(self, valueName){..}
#  - Also implement a list holding the data types for all columns
#		NK_TABLE_COLUMNS = [(KEY_COLUMNNAME, "TEXT"), {..., ""}
#  - Implement a set an get funtion to retrieve a value using the key:
#		!Note: you must implement the if statement for the KEY_ID for it to work
# 		def setProperty(self, key, value):
# 			if key == self.KEY_ID:
#		 		self.setID(value)
# 			if key == self.KEY_COLUMNNAME:
#		 		self.setColumnName(value)
# 			if key == ....:
#		 		etcetera
#
#	 	def getProperty(self, key):
#	 		if key == self.KEY_ID:
#	 			return self.getID()
# 			if key == self.KEY_COLUMNNAME:
# 				return self.getColumnName()
# 			if key == ...:
# 				etcetera
class SQLData(object):

	# These functions are needed to save nparaays in the sqlite db
	def adapt_array(arr):
		try:
		    buffer
		except NameError:
		    buffer = bytes

		out = io.BytesIO()
		np.save(out, arr)
		out.seek(0)
		return lite.Binary(out.read())

	def convert_array(text):
	    out = io.BytesIO(text)
	    out.seek(0)
	    return np.load(out)
			    
	# Converts np.array to TEXT when inserting
	lite.register_adapter(np.ndarray, adapt_array)

	# Converts TEXT to np.array when selecting
	lite.register_converter("array", convert_array)	


	# ^^^^^^^^^^^^^^^ 
	# 
	# This initialises the ID column in the table
	KEY_ID				= "Id"
	NK_TABLE_KEY_COL 	= (KEY_ID, "INTEGER PRIMARY KEY")

	# ^^^^^^^^^^^^^^^
	# Constructor
	# 
	# probably you want to implement your own
	def __init__(self):
		self.ID = None
		self.SQLITE_DB_FILE_PATH = ":memory:"

	# ^^^^^^^^^^^^^^^
	# getColumnNamesInList
	#
	# Get a list of column names 
	@classmethod
	def getColumnNamesInList(self):
		return zip(*self.NK_TABLE_COLUMNS)[0]

	# ^^^^^^^^^^^^^^^
	# getColumnInTable
	# 
	# Get a whole column in the database as a list
	@classmethod
	def getColumnInTable(self, col_name, SQLITE_DB_FILE_PATH):
		con = None
		try:
			# Make connection (dont forget the detect_types for using np arrays that you defined yourself)
			con = lite.connect(SQLITE_DB_FILE_PATH, detect_types=lite.PARSE_DECLTYPES)
			# Make a connection
			con.row_factory = lite.Row
			# Set the cursor
			cur = con.cursor()    

			# Execute and fetch
			cur.execute("select "+col_name+" from "+self.NK_TABLE_NAME)
			rows = cur.fetchall()

			return [ r[col_name] for r in rows]

		except lite.Error, e:
		    print "Error (Insert into db): %s" % e.args[0]
		    sys.exit(1)
		    
		finally:
		    if con:
		        con.close()

	# ^^^^^^^^^^^^^^^
	# getColumnNamesInString
	# 
	# Get all the column names in a comma seperated string
	@classmethod
	def getColumnNamesInString(self, with_ID=False):
		if with_ID: 
			columns = [self.NK_TABLE_KEY_COL]+self.NK_TABLE_COLUMNS
		else: 
			columns = self.NK_TABLE_COLUMNS

		if len(columns) == 0:
			return "()"
		elif len(columns) == 1:
			return "("+columns[0][0]+")"
		else:
			return "{}".format(zip(*columns)[0]).replace("'", "")



	# ^^^^^^^^^^^^^^^
	# getDataAsList
	# 
	# Functiont to get a row as a list
	def getDataAsList(self):
		return [self.getProperty(c[0]) for c in self.NK_TABLE_COLUMNS]

	# ^^^^^^^^^^^^^^^
	# setID
	#
	def setID(self, ID):
		self.ID = ID
		
	# ^^^^^^^^^^^^^^^
	# getID
	#
	def getID(self):
		return self.ID

	# ^^^^^^^^^^^^^^^
	# retrieveFromDB
	# 
	def retrieveFromDB(self, search_cat):
		con = None
		try:
			# Make connection (dont forget the detect_types for using np arrays that you defined yourself)
			con = lite.connect(self.SQLITE_DB_FILE_PATH, detect_types=lite.PARSE_DECLTYPES)
			# Make a connection
			con.row_factory = lite.Row
			# Set the cursor
			cur = con.cursor()    

			search_str = ""
			for key in search_cat.keys():
				search_str += key+"=:"+key

			sql_q = "SELECT * FROM "+self.NK_TABLE_NAME+" WHERE "+search_str
			cur.execute(sql_q, search_cat) 

			# This way you get dictionairies returned
			rows = cur.fetchall()
			if len(rows) > 1:
				warnings.warn("DataClass_SQLData, retrieveFromDB(): search did not give unique results, will just use the first item in the result list")

			if len(rows) > 0:
				return rows[0]
			else:
				return {}

		except lite.Error, e:		    
		    print "Error (retrieveFromDB): %s" % e.args[0]
		    sys.exit(1)
		    
		finally:
		    if con:
		        con.close()


	# ^^^^^^^^^^^^^^^
	# 
	# 
	# This function uses the function getDataAsList to know what to save in the DB
	def insertIntoDB(self, resetTable = False):
		con = None
		try:


			# Make connection (dont forget the detect_types for using np arrays that you defined yourself)
			con = lite.connect(self.SQLITE_DB_FILE_PATH, detect_types=lite.PARSE_DECLTYPES)
			# Make a connection
			con.row_factory = lite.Row
			# Set the cursor
			cur = con.cursor()    

			# Make the table
			if resetTable:
				cur.execute("DROP TABLE IF EXISTS "+self.NK_TABLE_NAME)
				sql_q = "create table "+self.NK_TABLE_NAME+" ("+self.NK_TABLE_KEY_COL[0]+" "+self.NK_TABLE_KEY_COL[1]+", "
				for i in range(len(self.NK_TABLE_COLUMNS)):
					COL = self.NK_TABLE_COLUMNS[i]
					sql_q += COL[0]+" "+COL[1]
					if i != len(self.NK_TABLE_COLUMNS)-1:
						sql_q += ", "
				sql_q += ")"

				cur.execute(sql_q)

				con.commit()

			# Insert twp examples
			sql_q = "insert into "+self.NK_TABLE_NAME+" "+self.getColumnNamesInString()+" values ("+", ".join(["?" for i in range(len(self.NK_TABLE_COLUMNS))])+")"

			cur.execute(sql_q, self.getDataAsList())

			con.commit()


		except lite.Error, e:
		    print "Error (Insert into db): %s" % e.args[0]
		    sys.exit(1)
		    
		finally:
		    if con:
		        con.close()


