from moneylover import *

#take a list and add together all of the amounts in each category
#return a hash table
def addAmountByCategory(mlRowList):
	#making a design decision between taking a presorted list or sorting it on the fly
	#for now we sacrifice cpu cycles so others can be lazy
	sortedList = sortByCategory(mlRowList)

	#compare row's category with the previous row's category
	#if they are the same, add together
	#if they are different, push the previous added value into the hash w/ category name
	#and begin anew

	#have to pop first element off of sortedList
	for row in sortedList:
		
	return
