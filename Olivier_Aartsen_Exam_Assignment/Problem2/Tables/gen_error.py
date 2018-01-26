import numpy as np
from astropy.io.votable import parse
import matplotlib.pyplot as plt


votB = parse("PhotoZFileB.vot")

table = votB.get_first_table()

#Let's convert the 'astropy.io.votable.tree.Table' completely into an array. This is just to make it so that I can later change every row into a list and then into an numpy array:
array = np.ndarray.tolist(np.asarray(table.array))

#Define a numpy array for PhotoB so that I can handle it normally
PhotoB = np.zeros((len(array), len(array[1])))

#In this for-loop I make every row of array (which is a tuple) into a list and then into a numpy array:
for i in range(0, len(array)):
	PhotoB[i] = np.asarray(list(array[i]))

magr = PhotoB[:, 1]
ug = PhotoB[:, 2]
gr = PhotoB[:, 3]
ri = PhotoB[:, 4]
iz = PhotoB[:, 5]
zspec = PhotoB[:, 6]

#Let's define the model function:
def pred_z (ug, gr, ri, iz, theta=np.array([1,1,1,1,1])):
	return theta[0] + theta[1] * ug + theta[2] * gr + theta[3] * ri + theta[4] * iz

#So for the ridge regression we have performed theta is:
theta = np.array([-0.214, -0.027, 0.115, 0.666, 0.011])

zspec_pred = pred_z(ug, gr, ri, iz, theta)

residuals = zspec_pred - zspec

residuals_frac = residuals / (zspec + 1)
print np.median(np.absolute(residuals_frac))
