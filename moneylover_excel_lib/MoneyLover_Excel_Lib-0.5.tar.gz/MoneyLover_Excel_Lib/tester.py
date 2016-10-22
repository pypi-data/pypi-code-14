from moneylover import *
#import calculations as calc

#mergeinto, hdr1 = loadMLWorkbook("ToMergeTo.xlsx")
#badsync, hdr2 = loadMLWorkbook("BadSyncExport.xlsx")

report = []

#mergeinto = sortByDate(mergeinto)
#badsync = sortByDate(badsync)

#for item1 in mergeinto:
#	for item2 in badsync:
#		if(not item1.compare(item2)):
#			print "OPPOSITES"
#			item1.display()
#			item2.display()



#hdr.display()
#for x in lsClass:
#	x.display()
#lsList = generateArray(lsClass)
#print lsList

test2 = spliceByCategory(report)
print test2
test = spliceDateRange("06/01/2016", "07/12/2016", report)
print test

#sortedClassList = sortByCategory(lsClass)
#test = 0
#for x in sortedClassList:
#	test += 1
#separatedcats = spliceByCategory(lsClass)
#totalelements
#exportToNewWorkbook(hdr, test, "datesplice.xlsx")
