#By: 			Olivier Aartsen
#Studentnumber:		s1397478
#Last modified on:	26/01/2018
#This file is meant to perform regression on the PhotoZFileA data.

import numpy as np
from astropy.io.votable import parse
from sklearn.linear_model import Ridge, Lasso, LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


votA = parse("PhotoZFileA.vot")

table = votA.get_first_table()

#Let's convert the 'astropy.io.votable.tree.Table' completely into an array. This is just to make it so that I can later change every row into a list and then into an numpy array:
array = np.ndarray.tolist(np.asarray(table.array))

#Define a numpy array for PhotoA so that I can handle it normally
PhotoA = np.zeros((len(array), len(array[1])))

#In this for-loop I make every row of array (which is a tuple) into a list and then into a numpy array:
for i in range(0, len(array)):
	PhotoA[i] = np.asarray(list(array[i]))


magr = PhotoA[:, 1]
ug = PhotoA[:, 2]
gr = PhotoA[:, 3]
ri = PhotoA[:, 4]
iz = PhotoA[:, 5]
zspec = PhotoA[:, 6]

X = np.vstack((ug, gr, ri, iz, zspec)).T
M = np.vstack((ug, gr, ri, iz)).T

'''
df = pd.DataFrame(X[0:1000, :], columns=['u-g', 'g-r', 'r-i', 'i-z', 'zspec'])
g = sns.PairGrid(df, diag_sharey=False)
g.map_lower(sns.kdeplot, cmap="Blues_d")
g.map_upper(plt.scatter)
g.map_diag(sns.kdeplot)
plt.savefig("correlation.png")
plt.show()
plt.close()'''






#The data don't seem super correlated, but zspec seems to have correlations with all the colors, and between the colors there seem to be some correlation, so let's assume that zspec can be approximated by:
#zspec = theta_0 + theta_1 * ug + theta_2 * gr + theta_3 * ri + theta_4 * iz

#We go for a ridge model
ridge_model = Ridge(alpha=0.01, fit_intercept=True, normalize=True)

colors = M[:, 0:4]
#Actually fit the data and predict the temperature, the coeficients of the model are stored in result.coef_
result = ridge_model.fit(colors, zspec)
zspec_pred = ridge_model.predict(colors)
#Define the residuals
residuals = zspec_pred - zspec

#Store the coeficients inside a variable
coef = [result.intercept_]
[coef.append(coeff) for coeff in result.coef_]
print "The model that fits best is: zspec = {0:.3f} + {1:.3f} (u-g) + {2:.3f} (g-r) + {3:.3f} (r-i) + {4:.3f} (i-z) \n".format(coef[0], coef[1], coef[2], coef[3], coef[4])


residuals_frac = residuals / (zspec + 1)

E_theta = np.median(np.absolute(residuals_frac))

print "So the training error we obtain is: " + str(round(E_theta, 4))


#Below explained: we define fig as a matplotlib.figure.Figure object and ax as an array of axes objects, ncols and nrows are number of columns and rows of subplot grid, figsize speaks for itself
fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(12, 8))
#Add a scatter plot to ax of T vs residuals, with alpha being the transparency of the points; you can see by changing alpha to 1 that it becomes a much worse plot
ax.scatter(zspec, residuals_frac, marker='.', alpha=0.1)
#So the r'...' is so that you can use Latex in your labels, fontsize speaks for itself
ax.set_xlabel(r'$zspec$', fontsize=16)
ax.set_ylabel(r'$(zspec_{pred}-zspec)/zspec$', fontsize=16)
#This tick_params just alters the appearance of the labels
ax.tick_params(axis='both', which='major', labelsize=16)
#Set limit of y-axis, afterwards it automatically plots
ax.set_ylim(-0.5, 0.5)
plt.savefig("regression_lowest_training_error.png")
plt.show()
plt.close()





'''
#Try lasso now:
lasso_model = Lasso(alpha=0.000000001, fit_intercept=True, normalize=True)

colors = M[:, 0:4]
#Actually fit the data and predict the temperature, the coeficients of the model are stored in result.coef_
result = lasso_model.fit(colors, zspec)
zspec_pred = lasso_model.predict(colors)
#Define the residuals
residuals = zspec_pred - zspec

#Store the coeficients inside a variable
coef = [result.intercept_]
[coef.append(coeff) for coeff in result.coef_]
print "The model that fits best is: zspec = {0:.3f} + {1:.3f} (u-g) + {2:.3f} (g-r) + {3:.3f} (r-i) + {4:.3f} (i-z)".format(coef[0], coef[1], coef[2], coef[3], coef[4])


residuals_frac = residuals / (zspec + 1)

#x_median, median, bins = running_median(zspec, residuals_frac, binsize=100)


E_theta = np.median(abs(residuals_frac))

print "So the training error we obtain is: " + str(round(E_theta, 4))
'''










'''
plt.plot(ug, gr)
plt.show()
plt.close()

plt.plot(ug, gr)
plt.show()
plt.close()

plt.plot(ug, gr)
plt.show()
plt.close()

plt.plot(ug, gr)
plt.show()
plt.close()

plt.plot(ug, gr)
plt.show()
plt.close()

plt.plot(ug, gr)
plt.show()
plt.close()'''
