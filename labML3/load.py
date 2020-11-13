#!/usr/bin/env python

'''load.py: Script to load and test the final models; calls supplement.py'''

__author__     = 'Camilo A. Fernandes Salvador'
__email__      = 'csalvador@usp.br'
__copyright__  = 'Copyright © 2020, University of Sao Paulo'

# This code is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 of 29 June 2007.
# ATTENTION: please use sklearn.RandomForestRegressor ver. 0.21.2+
# ATTENTION: this script requires local files (supplement.py)
#
# -- start

import os
import pandas as pd
import numpy as np
import keras
import matminer
import pickle

from keras.models import load_model
from matminer.utils.io import load_dataframe_from_json
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from supplement import searchNN, trainNN, evaluateModel, createRF #stores custom methods/functions

fdf = load_dataframe_from_json('Batteries_final.json')
print("The starting dataset has {}".format(fdf.shape))
print (fdf.head())

'''
Block 1 - Random Forest
'''
print ('\n---\n')
print ('Selecting target variable...')

excluded = ['Spacegroup', 'Capacity Grav', 'Capacity Vol', 'Specific E Wh/kg',
            'E Density Wh/l', 'Stability Charge', 'Stability Discharge', 'Ion',
            'Reduced Formula', 'Id', 'composition', 'composition_oxid',
            'HOMO_character', 'HOMO_element',
            'LUMO_character', 'LUMO_element']

# A few additional adjustments
fdf = fdf.drop(excluded, axis=1)
fdf = fdf.replace([np.inf, -np.inf], np.nan)
fdf = fdf.fillna(0)

# Defining the target variable
target = 'Average Voltage'

y = fdf[target].values
X = fdf.drop([target], axis=1)
print ('The target variable was stored in y: {}'.format(y))

# Normalizing the data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)

# How many descriptors were generated? 
print('There are {} possible descriptors:\n{}'.format(X.shape[1], X.columns.values))

print ("\nAvailable cores: {}".format(os.sched_getaffinity(0)))
# os.sched_setaffinity(0, {0}) # running on one core
os.sched_setaffinity(0, {0, 1, 2, 3}) # running on four cores
print ("\nRunning on core/cores {}".format(os.sched_getaffinity(0)))


print ('\nCreating a Neural Net')

# Training model
model_raw = searchNN(X, y) # search the best NN
model = trainNN(model_raw, X, y, 2048) # train the best NN for 512 epochs
# model = load_model('nn_trained.h5') # already trained?

# Evaluating model
evaluateModel(model, X, y)
print ('Done 1')
print ('\n---\n')

'''
Block 2 - Plotting section
'''
print ('Making graphics...')

import matplotlib as mpl
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.colors
from matplotlib.ticker import StrMethodFormatter
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import seaborn as sns

# Defining colors and styles
plt.style.use('tableau-colorblind10')
plt.rcParams.update({'font.size': 18, 'figure.figsize': (8,6)})
#plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:,.1f}')) # 3 decimal places
#plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.1f}')) # 3 decimal places

# Importing the USP color identity
# color = c('RGBA string')
c = matplotlib.colors.ColorConverter().to_rgb
c0 = c('#fcb421ff') #00-yellow
c1 = c('#0b6879ff') #0d-blue
c2 = c('#1094abff') #00-blue

# Using the same from supplement.py
RSEED = 64   # Random seed to ensure reproducibility
FOLDS = 5    # 5-fold cross validation, i.e. 20% reserved to testing 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(1/FOLDS), random_state=RSEED)
#

# Plot 2 - Actual vs predicted
plt.rcParams.update({'font.size': 18, 'figure.figsize': (8,6)})
f, ax = plt.subplots(figsize=(8,8))

ax.set(xlim=(0, 8), ylim=(0, 8))

plt.scatter(model.predict(X_train), y_train, c=c0, alpha=0.7, label='Train')
plt.scatter(model.predict(X_test), y_test, c=c1, alpha=0.6, label='Test')
plt.xlabel('Predicted voltage (V)', fontsize=20)
plt.ylabel('Database voltage (V)', fontsize=20)
plt.title('(b)', fontsize=22)
plt.legend()

diag_line, = ax.plot(ax.get_xlim(), ax.get_ylim(), ls='--', c='.2')

plt.subplots_adjust(left=0.16, bottom=0.16, right=0.94)
plt.savefig('plot2.png', dpi=300)
plt.show()

# Preparing bins and residuals
train_res = y_train - model.predict(X_train)
bins_train = (-0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4)
test_res = y_test - model.predict(X_test)
bins_test = np.arange(np.floor(test_res.min()), np.ceil(test_res.max()), 0.4)

# Plot 3 - Error distribution
plt.rcParams.update({'font.size': 28, 'figure.figsize': (8,6)})
plt.style.use('seaborn-ticks')
mpl.rcParams['axes.linewidth'] = 2 
mpl.rcParams['xtick.major.size'] = 20
mpl.rcParams['xtick.major.width'] = 4
mpl.rcParams['xtick.minor.size'] = 10
mpl.rcParams['xtick.minor.width'] = 2

plt.hist(train_res, bins=bins_train, density=1, color=c0, alpha=0.7, label='Train')
plt.hist(test_res, bins=bins_test, density=1, color=c1, alpha=0.7, label='Test')
plt.xlim(xmin= -4, xmax = 4)
plt.xlabel('test-set abs. error (V)')
plt.yticks([])
plt.legend()

plt.subplots_adjust(left=0.09, bottom=0.20, right=0.95, top=0.95)
plt.savefig('plot3.png', dpi=300)
plt.show()

print ('Done 2')
print ('\n---\n')

#
# --- end
