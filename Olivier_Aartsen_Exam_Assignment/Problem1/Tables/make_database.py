#By: 			Olivier Aartsen
#Studentnumber:		s1397478
#Last modified on:	26/01/2018
#This file is meant to make the database, create the tables in the database and fill them with the values from the files. IMPORTANT! READ THE FIRST LINE (with the os.remove function) BEFORE RUNNING THIS CODE TO MAKE SURE YOU DON'T DELETE SOMETHING ON ACCIDENT!
import sqlite3 as lite
import numpy as np
import csv
from astropy.io import fits
import os
import sys

#READ BEFORE RUNNING! The following line removes the database I called prob1.db, if coincidentally you have a file with the same name in the folder you're running this code in then that file will be deleted. Now I run this line so that the creation of tables in this database doesn't clash with already existing tables, in other words I want to have a clean and empty database so that I can run variants of this code multiple times in a row without getting error messages.
try:
    os.remove("prob1.db")
except OSError:
    pass

#Connect to the database (and since it doesn't exist yet this also creates the database)
con = lite.connect("prob1.db")
#Get a cursor
cur = con.cursor()
#Create the first table in the database; the info-table (with information about the fields, dates of observation, etc...)
cur.execute("CREATE TABLE IF NOT EXISTS Info (ID INT, FieldID INT, Filename varchar(100), Filter varchar(2), MJD DOUBLE, Airmass DOUBLE, Exptime FLOAT, Tablename varchar(20), UNIQUE (ID), UNIQUE (Tablename), PRIMARY KEY (Tablename));")

#Open the .csv file in which the information resides
with open('info.csv', 'rb') as info_file:
	reader = csv.reader(info_file)
	info = list(reader)

#Insert the values from the above opened .csv file into a table called Info:
cur.executemany("INSERT INTO Info (ID, FieldID, Filename, Filter, MJD, Airmass, Exptime, Tablename) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", info[1:len(info)])
con.commit()


#Now we want to create and fill the remaining tables, which we do with a for-loop since it is a large amount of tables (18 tables to be exact) and therefore we can use the range from 1 to the length of the info list, since the length of the info list is exactly the amount of exposures taken. I use the same for-loop as I did in the change_csv.py program, but I now included a data_name which is the name of the .fits files that hold the data (for more info see the change_csv.py file ).
#Define Filters here so that we can fill it in this for-loop and then use it in the following for-loop (in which I make unions)
Filters = []
for i in range(1, len(info)):

	if info[i][3] != 'Ks':
		table_name =  "F" + str(info[i][1]) + str(info[i][3])
		#So now we also define the data_name so that we can read in the data after these for-loops. Also we fill the Filters list by appending:
		data_name = "Field-" + str(info[i][1]) + "-" + str(info[i][3]) + ".fits"
		Filters.append(info[i][3])
		
	else:
		a = 1
		for j in range(1,len(info)):
			if info[j][3] == 'Ks' and info[i][1] == info[j][1] and float(info[i][4]) > float(info[j][4]):
				a = a+1
				
		table_name = "F" + str(info[i][1]) + str(info[i][3]) + "E{0:0=3d}".format(a)
		#Again we now also define data_name and fill the Filters list:
		data_name = "Field-" + str(info[i][1]) + "-" + str(info[i][3]) + "-" + "E{0:0=3d}".format(a) + ".fits"
		Filters.append(info[i][3] + str(a))
	
	#Here I define the ExpID which stands for the Exposure ID (which is the unique ID of each exposure as given in the info.csv file) and the Field so that I can put these values in the tables.
	ExpID = info[i][0]
	Field = info[i][1]
	print data_name
	
	#Here I load in the data using; fits.getdata() to open the fits file, then np.asarray() to convert it into a numpy array and finally np.ndarray.tolist() to convert the array to a list so that I can use the INSERT command to fill the table in the SQL database. Now I know that there might have been more elegant ways to do this, but I couldn't find a lot of information about loading fits files or numpy arrays into a table in a SQL-database, so I just use this.
	data = np.ndarray.tolist(np.asarray(fits.getdata(data_name)))
	
	#Finally define and execute the commands to create the tables and fill them
	command = "CREATE TABLE IF NOT EXISTS " + table_name + " (RunningID INT, X DOUBLE, Y DOUBLE, Flux1 DOUBLE, dFlux1 DOUBLE, Flux2 DOUBLE, dFlux2 DOUBLE, Flux3 DOUBLE, dFlux3 DOUBLE, Ra DOUBLE, Dec DOUBLE, Class INT, Mag1 DOUBLE, dMag1 DOUBLE, Mag2 DOUBLE, dMag2 DOUBLE, Mag3 DOUBLE, dMag3 DOUBLE, StarID INT, ExpID INT, Field INT, UNIQUE(StarID), PRIMARY KEY(StarID), FOREIGN KEY(ExpID) REFERENCES Info(ID));"
	cur.execute(command)

	command = "INSERT INTO " + table_name + " (RunningID, X, Y, Flux1, dFlux1, Flux2, dFlux2, Flux3, dFlux3, Ra, Dec, Class, Mag1, dMag1, Mag2, dMag2, Mag3, dMag3, StarID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
	cur.executemany(command, data)
	con.commit()
	
	command = "UPDATE " + table_name + " SET ExpID  = {0}, Field = {1}".format(ExpID, Field)
	cur.execute(command)
	con.commit()


#So now let's make UNIONS of tables with the same filter from different fields, where as for the Ks filter I will combine those that were taken in the same turn, meaning that I will combine for example all the first exposures taken in Ks filter in different fields, and then the second exposures, etc (while for the third exposure there is only 1 in field 1, so the contents of this table will remain the same, all though I will alter the name of the table just like I will alter the name of the UNIONS). This is so that the StarID in these unions of Ks filter tables will remain unique.
#First define a list in which we will store the first-occurence index of each Filter, this is so that we will break the for-loops when the all the unique unions have been made.
Filters_ind = []
#Since we need the previous tables to make the UNIONS (at least I couldn't think of an easier method that does this, but maybe I have just missed something fairly obvious), I need to make a new for-loop to make these UNIONS (note that the for-loops over i and j are the same as the above for-loops):
for i in range(1, len(info)):
	if info[i][3] != 'Ks':
		#Now we also define Filter1 to compare later to Filter2 to determine which tables need to be unified.
		Filter1 = info[i][3]
		#We still need the table_name as we will see later
		table_name1 =  "F" + str(info[i][1]) + str(info[i][3])
	else:
		a = 1
		
		for j in range(1, len(info)):
			if info[j][3] == 'Ks' and info[i][1] == info[j][1] and float(info[i][4]) > float(info[j][4]):
				a = a+1
		table_name1 = "F" + str(info[i][1]) + str(info[i][3]) + "E{0:0=3d}".format(a)
		Filter1 = info[i][3] + str(a)
	#These print statements below can give more clarity what is going on, but it also generates quite some text so I put them off as default
	#print "FILTER 1:"
	#print Filter1
	
	#Define b and c which we will later use to make sure that certain if-statements don't get approved twice
	b = 1
	c = 1
	#We now define another for-loop in which we will compare two filters so that we can unify the corresponding tables. We go from k=i+1 so that we avoid unifying the same tables (if we let k=1 then it will immediately see that the two filters of the tables are the same and try to unify them). The for-loops below over k and l are very similar to the ones over i and j, but now we use results from the loops over i and j to compare filters and tables.
	for k in range(i+1, len(info)):		
		if info[k][3] != 'Ks':
			Filter2 = info[k][3]
			table_name2 =  "F" + str(info[k][1]) + str(info[k][3])
		else:
			d = 1
		
			for l in range(1, len(info)):
				if info[l][3] == 'Ks' and info[k][1] == info[l][1] and float(info[k][4]) > float(info[l][4]):
					d = d+1
			table_name2 = "F" + str(info[k][1]) + str(info[k][3]) + "E{0:0=3d}".format(a)
			Filter2 = info[k][3] + str(d)
		#These print statements below can give more clarity what is going on, but it also generates quite some text so I put them off as default
		#print "FILTER 2:"
		#print Filter2
		
		#The below if-statement is just to ensure that the Filters_ind is actually filled in with every filter index, before we start using it.
		if i == 1:
			Filters_ind.append(Filters.index(Filter2))
		#The below if-statement makes sure that we will break out of the for-loop over k once every unique union has been made. The fact that it doesn't break immediately is because max(Filters_ind) will be zero the first time it runs over this, but so will i-1, so i-1!>max(Filters_ind). After multiple loops it will only break once every unique union has been made.
		if i-1 > max(Filters_ind):
			print Filters
			con.close()
			print "All the unions have been made, so we stop now!"
			break
		#Now we actually compare filters to see which tables we need to unify. The first requirement below checks that the filters are the same, the second is a back-up check that we don't unify the same tables and the third requirement is so that it only tries to unify tables if it hasn't been done before (for example if the for-loop is at the point of the Z-filter in the second field then we don't want to try and unify anything since we already unified all the Z-tables when the for-loop was at the point of the Z-filter in the first field, so this is ensured by the fact that i-1=7, but the first index of Filters is still 1, so they are not equal and no UNIONS will be made)
		if Filter1 == Filter2 and table_name1 != table_name2 and i-1 == Filters.index(Filter1):
			#Here we require b to be 1 so that only the first table in a certain filter will be renamed
			if b == 1:
				#Here we command to rename the first table to the name of the filter.
				command = "ALTER TABLE " + table_name1 + " RENAME TO " + Filter1 + ";"
				cur.execute(command)
				con.commit()
				print command
				b = b + 1
			#Now we unify the tables with similar filters by inserting the values of the second table (with the same filter as the first table) into the first table and then drop the old second table
			command = "INSERT INTO " + Filter1 + " SELECT * FROM " + table_name2 + ";"
			cur.execute(command)
			con.commit()
			print command
			command = "DROP TABLE " + table_name2 + ";"
			cur.execute(command)
			con.commit()
			print command
		#Now to make sure that every table is renamed afterwards for consistency, here we make sure that if the filter is used only in one field it will still be renamed. The first requirement checks that the filter is indeed unique and the second requirement makes sure that the for-loop doesn't try to alter the table name multiple times since that would result in an error (because after altering the name of the table the first time the original table_name will have dissappeared and so there is nothing to rename).	
		if Filters.count(Filter1) == 1 and c == 1:
			command = "ALTER TABLE " + table_name1 + " RENAME TO " + Filter1 + ";"
			cur.execute(command)
			con.commit()
			print command
			c = c + 1
	#This is to break out of the for-loop over i, which happens after we have broken out of the for-loop over k
	if i-1 > max(Filters_ind):
		break

#Just to make sure the for-loops have ended
print "BREAK WORKED!"

