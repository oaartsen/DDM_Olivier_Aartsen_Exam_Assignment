#By: 			Olivier Aartsen
#Studentnumber:		s1397478
#Last modified on:	26/01/2018
#This file is meant to simulate new data-points as requested for problem 1c.

import numpy as np
import csv
import matplotlib.pyplot as plt
import random as r

#For problem 1c):
#Load in the data for 1c)
JH_YJ = np.loadtxt('JH_YJ.csv', delimiter = ',', skiprows=1)
#Define the actual data-columns
data = JH_YJ[:, 1:3]

#Now I will just define some lines that will be used in the following plot to highlight certain areas where there seemingly exists a structure:
x1 = [-1.65, -1.65]
y1 = [-5, 5]

x2 = [-0.8, -0.8]
y2 = [-5, 5]

x3 = [0.63, 0.63]
y3 = [-5, 5]

plt.plot(JH_YJ[:,2], JH_YJ[:,1], '.', color = 'c', alpha=0.5)
plt.plot(x1, y1, color = 'black')
plt.plot(x2, y2, color = 'black')
plt.plot(x3, y3, color = 'black')
plt.xlim(-3.0, 1.5)
plt.ylim(-4, 4)
plt.title("The J-H Color Versus the Y-J Color for the Original Data")
plt.xlabel("Y-J")
plt.ylabel("J-H")
plt.savefig("JH_YJ_original.png")
plt.show()
plt.close()

#Let's try to generate more data by taking random points in my data set and moving a bit around it.
amount = 100000
sim_data = np.zeros((amount,2))

#So basically I have just looked at the 2D plot of the original data and see what kind of structures I can recognize myself. Using this knowledge I split the field up in 5 parts (as can be seen in JH_YJ.png) and in these parts I apply different random offsets. For example in the part where Y-J>0.63 and J-H>-2 we can see a lobe that primarily stretches out in horizontal direction and so I will give the new data a higher possible random offset than in the vertical direction (as to maintain this structure). Also I use Gaussian (or Normal) offsets as to not put an hard limit on the value of the offset but still keep it almost always in a controlled range.
for i in range(0,amount):
	ind = np.random.randint(0, len(data[:,0]))
	
	if data[ind, 1] < -1.65:
		offsetx = np.random.normal(0.0, 0.15)
		offsety = np.random.normal(0.0, 0.3)
		offset = np.array([offsety, offsetx])
		#offset = 0
	if data[ind, 1] > -1.65 and data[ind, 1] < -0.8:
		offset = np.random.normal(0.0, 0.1, 2)
		#offset = 0
	if data[ind, 1] > -0.8 and data[ind, 1] < 0.63:
		offset = np.random.normal(0.0, 0.01, 2)
		#offset = 0
	if data[ind, 1] > 0.63:
		offsetx = np.random.normal(0.0, 0.2)
		offsety = np.random.normal(0.0, 0.05)
		offset = np.array([offsety, offsetx])
		#offset = 0
	#if data[ind, 0] < -3:
	#	offsetx = np.random.normal(0.0, 0.1)
	#	offsety = np.random.normal(0.0, 0.3)
	#	offset = np.array([offsety, offsetx])
	#	print "WRONG"
		#offset = 0

	sim_data[i] = data[ind] + offset
	
#Plot the simulated data:
plt.plot(sim_data[:,1], sim_data[:,0], '.', alpha=0.5)
plt.xlim(-3.0, 1.5)
plt.ylim(-4, 4)
plt.title("The J-H Color Versus the Y-J Color for the Simulated Data")
plt.xlabel("Y-J")
plt.ylabel("J-H")
plt.savefig("JH_YJ_simulated.png")
plt.show()
plt.close()

#Finally write the simulated file out to sim_JH_YJ.csv
np.savetxt("sim_JH_YJ.csv", sim_data, delimiter=',', header='JH,YJ', comments='')
