#By: 			Olivier Aartsen
#Studentnumber:		s1397478
#Last modified on:	26/01/2018
#This file is meant to change the file_info_for_problem.csv to a new info.csv file that includes the table names as the tables will be called in the future SQL-database.
import numpy as np
from astropy.io import fits
import csv

#Let's add a name of the table, which it will be called like in the sql database, to the csv-file
#So first open the original file using the csv package:
with open('file_info_for_problem.csv', 'rb') as info_file:
	reader = csv.reader(info_file)
	info = list(reader)

#This is just to account for the header
info[0].append("Tablename")
#Now use a for-loop to go through the original file (we start at 1 to avoid the header)
for i in range(1, len(info)):
	#This is to exclude the Ks-filter in the standard namecalling (since for this filter another identifier is needed, namely the time it was taken)
	if info[i][3] != 'Ks':
		table_name =  "F" + str(info[i][1]) + str(info[i][3]) 
	#Below we make up the name for the Ks-filters	
	else:
		#a will be the number in the back of the name (after E00), which indicates when the exposure was taken
		a = 1
		#So we will go through the whole file (except the header) to make sure we name the right exposures with the right names
		for j in range(1,len(info)):
			#The requirements are (in order): firstly check that the filter is actually the Ks filter, secondly check that we're going to compare the Ks exposures in the same field and thirdly check which Ks filter in a particular field was taken first, second, third,...
			if info[j][3] == 'Ks' and info[i][1] == info[j][1] and float(info[i][4]) > float(info[j][4]):
				a = a+1
		#Note that if we would have more than 9 Ks filter exposures taken in the same field a would become a double (or even triple) digit number, but the below code (which makes the table name for the Ks filters) even accounts for that
		table_name = "F" + str(info[i][1]) + str(info[i][3]) + "E{0:0=3d}".format(a)

	print table_name
	info[i].append(table_name)
		
#Now write the new table to an info.csv file (this file will have the exact same rows and columns as the original except for the added Tablename column
with open("info.csv",'wb') as output_file:
	wr = csv.writer(output_file, dialect='excel')
	wr.writerows(info)
