#!/usr/bin/env python

'''supplement.py: Functions to train RF or NN (3 layers) models'''

__author__     = 'Camilo A. Fernandes Salvador'
__email__      = 'csalvador@usp.br'
__copyright__  = 'Copyright © 2020, University of Sao Paulo'

# This code is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 of 29 June 2007.

import numpy as np
import pandas as pd
import pickle
import tensorflow as tf 
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import RandomizedSearchCV, KFold
from sklearn.model_selection import cross_val_score, cross_val_predict, train_test_split
from sklearn.pipeline import Pipeline
from keras.callbacks import CSVLogger
from keras.layers import Dense, Activation, LeakyReLU
from keras.models import Sequential, load_model
from keras.wrappers.scikit_learn import KerasRegressor

# Boundary conditions to be set
RSEED = 952001       # Random seed to ensure reproducibility
FOLDS = 5            # 5-fold cross validation, i.e. 20% reserved to testing 
SEARCH = 20          # 20 models will be searched randomly
MAX_NEURONS = 300    # Max. number of neurons allowed in the hidden layers
np.set_printoptions(precision=3)

def createRF(X, y): 
    # Input the full dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(1/FOLDS), random_state=RSEED)
    
    rf = RandomForestRegressor(n_estimators=100, random_state=RSEED)
    param_grid = {
        'n_estimators': np.linspace(10, 1000).astype(int),
        'max_depth': [None] + list(np.linspace(3, 100).astype(int)),
        'max_features': ['auto', 'sqrt', None] + list(np.arange(0.5, 1, 0.1)),
        'max_leaf_nodes': [None] + list(np.linspace(10, 5000).astype(int)),
        'min_samples_split': [2, 5, 10],
        'bootstrap': [True, False]
        }

    rs = RandomizedSearchCV(rf, param_grid, n_jobs = -1, scoring = 'r2',
                            cv = FOLDS, n_iter = (SEARCH/FOLDS), 
                            verbose = 1, random_state=RSEED)
    
    rs.fit(X_train, y_train)
    print('A summary of the best RF model:{}'.format(rs.best_params_))
    model = rs.best_estimator_

    # Optional save
    with open('rf_model.pkl', 'wb') as savefile:
        pickle.dump(model, savefile)
    
    return model 

def searchNN(X, y):
    # Input the full dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(1/FOLDS), random_state=RSEED)
    
    def create_model(neurons_hidden_1=1, neurons_hidden_2=1, neurons_hidden_3=1):
        # A method to create a generic NN with 3 layers
        model = Sequential()

        # Input layer
        model.add(Dense(neurons_hidden_1, input_dim=X.shape[1]))
        model.add(layer=LeakyReLU(alpha=0.01))

        # Hidden layers
        model.add(Dense(neurons_hidden_2, activation='relu'))
        model.add(layer=LeakyReLU(alpha=0.01))
        model.add(Dense(neurons_hidden_3, activation='relu'))
        model.add(layer=LeakyReLU(alpha=0.01))

        # Output layer
        model.add(Dense(1, activation='relu'))
        model.add(layer=LeakyReLU(alpha=0.01))
        model.compile(loss='mean_squared_error', optimizer='adam')

        return model
    
    kreg = KerasRegressor(build_fn=create_model, verbose=0)
    
    param_grid = {
    'neurons_hidden_1': np.linspace(10, MAX_NEURONS).astype(int),
    'neurons_hidden_2': np.linspace(10, MAX_NEURONS).astype(int),
    'neurons_hidden_3': np.linspace(10, MAX_NEURONS).astype(int)}
    
    rs_model = RandomizedSearchCV(kreg, param_grid, n_jobs = -1, cv=FOLDS,
                              scoring = 'neg_mean_squared_error',  n_iter = SEARCH, 
                              verbose = 1, random_state=RSEED)
                              
    
    rs_model.fit(X_train, y_train)
    print('A summary of the best NN model:{}'.format(rs_model.best_params_))
    
    # Defining the number of neurons based on the best estimator
    nh3 = list(rs_model.best_params_.values())[0]
    nh2 = list(rs_model.best_params_.values())[1]
    nh1 = list(rs_model.best_params_.values())[2]

    model = create_model(nh1, nh2, nh3)
    
    # Optional save
    model.save('nn_raw.h5')

    return (model) 

def trainNN(model, X, y, steps):
    # Input the model to be evaluated,the full dataset, and the numbers of training steps
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(1/FOLDS), random_state=RSEED)
    
    csv_log = CSVLogger('training.log', separator=',', append=False)
    model.fit(X_train, y_train, epochs=steps, batch_size=10, callbacks=[csv_log])
    
    # Optional save
    model.save('nn_trained.h5')

    return model

def evaluateModel(model, X, y):
    # Input the model to be evaluated and the full dataset.    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(1/FOLDS), random_state=RSEED)
        
    # Making predictions
    ytrain_pred = model.predict(X_train)
    ytest_pred = model.predict(X_test)
    
    mse_train = np.sqrt(mean_squared_error(y_train, ytrain_pred))
    print('Train RMSE = {}'.format(mse_train))
    
    mse_test = np.sqrt(mean_squared_error(y_test, ytest_pred))
    print('Test RMSE = {}'.format(mse_test))    

    return()

#
# --- end