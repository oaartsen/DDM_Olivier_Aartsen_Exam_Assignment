#By: 			Olivier Aartsen
#Studentnumber:		s1397478
#Last modified on:	26/01/2018
#This file is meant to plot the results for queries R2, R3 and R5 since they produced more than 20 entries of output.

import numpy as np
import csv
import matplotlib.pyplot as plt

#For R2:
JH1_5 = np.loadtxt('JH1_5.csv', delimiter = ',', skiprows=1)

plt.hist(JH1_5[:,1], bins=200, range=(1.4, 2))
plt.xlim(1.4, 2.4)
plt.title("The Amount of Stars for J-H > 1.5")
plt.xlabel("J-H")
plt.ylabel("Amount of stars")
plt.savefig("JH_1_5.png")
plt.show()
plt.close()


#For R3:
#First for field 1:
R3_F1 = np.loadtxt('R3_F1.csv', delimiter = ',', skiprows=1)
avgflux_F1 = R3_F1[:,1]

Ks1Flux = R3_F1[:, 2]
Ks1Fluxerr = R3_F1[:, 3]
Ks2Flux = R3_F1[:, 4]
Ks2Fluxerr = R3_F1[:, 5]
Ks3Flux = R3_F1[:, 6]
Ks3Fluxerr = R3_F1[:, 7]

#Here we define N as the number of times the variation from the average flux is larger than the uncertainty in that flux (for each exposure in the Ks-filter in field 1):
N = np.array([np.abs(avgflux_F1 - Ks1Flux)/Ks1Fluxerr, np.abs(avgflux_F1 - Ks2Flux)/Ks2Fluxerr, np.abs(avgflux_F1 - Ks3Flux)/Ks3Fluxerr])

#Here we define Nmax as the maximum of the number of times the variation from the average flux is larger than the uncertainty in that flux:
Nmax = np.amax(N, axis=0)

plt.hist(Nmax, bins=150, range=(0, 200))
#plt.title("The Amount of Stars with the Number of times that the Variation from the Average Flux is Larger than the Uncertainty in that Flux")
plt.title("Variation from the Average Flux for Field 1")
plt.xlabel("(Flux_avg - Flux) / Sigma_flux")
plt.ylabel("Amount of Stars")
plt.savefig("VarAvgFluxF1.png")
plt.show()
plt.close()


#Now for field 3:
R3_F3 = np.loadtxt('R3_F3.csv', delimiter = ',', skiprows=1)
avgflux_F3 = R3_F3[:,1]

Ks1Flux = R3_F3[:, 2]
Ks1Fluxerr = R3_F3[:, 3]
Ks2Flux = R3_F3[:, 4]
Ks2Fluxerr = R3_F3[:, 5]

#Here we define N as the number of times the variation from the average flux is larger than the uncertainty in that flux (for each exposure in the Ks-filter in field 1):
N = np.array([np.abs(avgflux_F3 - Ks1Flux)/Ks1Fluxerr, np.abs(avgflux_F3 - Ks2Flux)/Ks2Fluxerr])

#Here we define Nmax as the maximum of the number of times the variation from the average flux is larger than the uncertainty in that flux:
Nmax = np.amax(N, axis=0)

plt.hist(Nmax, bins=50, range=(0, 150))
plt.title("Variation from the Average Flux for Field 3")
plt.xlabel("(Flux_avg - Flux) / Sigma_flux")
plt.ylabel("Amount of Stars")
plt.savefig("VarAvgFluxF3.png")
plt.show()
plt.close()



#For R5:
#First for field 1
SN30_F1 = np.loadtxt('SN30_F1.csv', delimiter = ',', skiprows=1)
MagY = SN30_F1[:,1]
SNY = SN30_F1[:,2]
MagZ = SN30_F1[:,3]
SNZ = SN30_F1[:,4]
MagJ = SN30_F1[:,5]
SNJ = SN30_F1[:,6]
MagH = SN30_F1[:,7]
SNH = SN30_F1[:,8]
MagKs1 = SN30_F1[:,9]
SNKs1 = SN30_F1[:,10]
MagKs2 = SN30_F1[:,11]
SNKs2 = SN30_F1[:,12]
MagKs3 = SN30_F1[:,13]
SNKs3 = SN30_F1[:,14]

plt.plot(MagY, SNY, '.')
plt.plot(MagZ, SNZ, '.')
plt.plot(MagJ, SNJ, '.')
plt.plot(MagH, SNH, '.')
plt.plot(MagKs1, SNKs1, '.')
plt.plot(MagKs2, SNKs2, '.')
plt.plot(MagKs3, SNKs3, '.')
plt.gca().invert_xaxis()
plt.title("Signal to Noise vs Magnitude for each Exposure in Field 1")
plt.xlabel("Magnitude")
plt.ylabel("S/N")
plt.legend(["Y-Exposure", "Z-Exposure", "J-Exposure", "H-Exposure", "Ks1-Exposure", "Ks2-Exposure", "Ks3-Exposure"], loc='upper left')
plt.savefig("SNMagF1.png")
plt.show()
plt.close()


#Now for field 2
SN30_F2 = np.loadtxt('SN30_F2.csv', delimiter = ',', skiprows=1, usecols=(0,1,2,3,4,5,6,7,8,9,10))
MagY = SN30_F2[:,1]
SNY = SN30_F2[:,2]
MagZ = SN30_F2[:,3]
SNZ = SN30_F2[:,4]
MagJ = SN30_F2[:,5]
SNJ = SN30_F2[:,6]
MagH = SN30_F2[:,7]
SNH = SN30_F2[:,8]
MagKs1 = SN30_F2[:,9]
SNKs1 = SN30_F2[:,10]

plt.plot(MagY, SNY, '.')
plt.plot(MagZ, SNZ, '.')
plt.plot(MagJ, SNJ, '.')
plt.plot(MagH, SNH, '.')
plt.plot(MagKs1, SNKs1, '.')
plt.gca().invert_xaxis()
plt.title("Signal to Noise vs Magnitude for each Exposure in Field 2")
plt.xlabel("Magnitude")
plt.ylabel("S/N")
plt.legend(["Y-Exposure", "Z-Exposure", "J-Exposure", "H-Exposure", "Ks1-Exposure"], loc='upper left')
plt.savefig("SNMagF2.png")
plt.show()
plt.close()


#Now for field 3
SN30_F3 = np.loadtxt('SN30_F3.csv', delimiter = ',', skiprows=1, usecols=(0,1,2,3,4,5,6,7,8,9,10,11,12))
MagY = SN30_F3[:,1]
SNY = SN30_F3[:,2]
MagZ = SN30_F3[:,3]
SNZ = SN30_F3[:,4]
MagJ = SN30_F3[:,5]
SNJ = SN30_F3[:,6]
MagH = SN30_F3[:,7]
SNH = SN30_F3[:,8]
MagKs1 = SN30_F3[:,9]
SNKs1 = SN30_F3[:,10]
MagKs2 = SN30_F3[:,11]
SNKs2 = SN30_F3[:,12]

plt.plot(MagY, SNY, '.')
plt.plot(MagZ, SNZ, '.')
plt.plot(MagJ, SNJ, '.')
plt.plot(MagH, SNH, '.')
plt.plot(MagKs1, SNKs1, '.')
plt.plot(MagKs2, SNKs2, '.')
plt.gca().invert_xaxis()
plt.title("Signal vs Magnitude to Noise for each Exposure in Field 3")
plt.xlabel("Magnitude")
plt.ylabel("S/N")
plt.legend(["Y-Exposure", "Z-Exposure", "J-Exposure", "H-Exposure", "Ks1-Exposure", "Ks2-Exposure"], loc='upper left')
plt.savefig("SNMagF3.png")
plt.show()
plt.close()
