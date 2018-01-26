import numpy as np
from astropy.io.votable import parse
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor






votA = parse("PhotoZFileA.vot")

table = votA.get_first_table()

#Let's convert the 'astropy.io.votable.tree.Table' completely into an array. This is just to make it so that I can later change every row into a list and then into an numpy array:
array = np.ndarray.tolist(np.asarray(table.array))

#Define a numpy array for PhotoA so that I can handle it normally
PhotoA = np.zeros((len(array), len(array[1])))

#In this for-loop I make every row of array (which is a tuple) into a list and then into a numpy array:
for i in range(0, len(array)):
	PhotoA[i] = np.asarray(list(array[i]))


magrA = PhotoA[:, 1]
ugA = PhotoA[:, 2]
grA = PhotoA[:, 3]
riA = PhotoA[:, 4]
izA = PhotoA[:, 5]
zspecA = PhotoA[:, 6]

XA = np.vstack((ugA, grA, riA, izA, zspecA)).T
MA = np.vstack((ugA, grA, riA, izA)).T

print "PhotoZFileA.vot loaded!"


votB = parse("PhotoZFileB.vot")

table = votB.get_first_table()

#Let's convert the 'astropy.io.votable.tree.Table' completely into an array. This is just to make it so that I can later change every row into a list and then into an numpy array:
array = np.ndarray.tolist(np.asarray(table.array))

#Define a numpy array for PhotoB so that I can handle it normally
PhotoB = np.zeros((len(array), len(array[1])))

#In this for-loop I make every row of array (which is a tuple) into a list and then into a numpy array:
for i in range(0, len(array)):
	PhotoB[i] = np.asarray(list(array[i]))

magrB = PhotoB[:, 1]
ugB = PhotoB[:, 2]
grB = PhotoB[:, 3]
riB = PhotoB[:, 4]
izB = PhotoB[:, 5]
zspecB = PhotoB[:, 6]

XB = np.vstack((ugB, grB, riB, izB, zspecB)).T
MB = np.vstack((ugB, grB, riB, izB)).T

print "PhotoZFileB.vot loaded!"


rf = RandomForestRegressor(n_estimators=10, criterion='mae')

print "First part random forest done!"

z_est_rf = rf.fit(MA, zspecA).predict(MB)

print "Fit of random forest done!"

residuals = zspec - z_est_rf
residuals_frac = residuals / (zspec + 1)

E = np.median(np.abs(residuals))

print "The generalization error is: " + str(round(E, 4))





np.savetxt("z_est.txt", z_est_rf, delimiter = '	')




plt.scatter(zspecA, zspecA - z_est_rf, marker='.')
plt.xlabel(r'$z_{spec}$')
plt.ylabel(r'$z_{spec} - z_{est}$')
#plt.ylim(-3000, 3000)
plt.title('Random forest')
#sig = np.std(y_test-z_est_rf)
#plt.text(4500, 2500, r"RMS={0:.2f}K".format(sig))
plt.savefig("random_forrest.png")
plt.show()
plt.close()






















