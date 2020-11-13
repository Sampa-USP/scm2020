#!/usr/bin/env python

'''predict_RF.py: Script to make predictions based on a prev. trained model'''

__author__     = 'Camilo A. Fernandes Salvador'
__email__      = 'csalvador@usp.br'

import matminer
from matminer.utils.io import load_dataframe_from_json
from matminer.utils.io import store_dataframe_as_json
import numpy as np
import pandas as pd
import pickle

'''
#Block 1 - Loading dataframe
'''
# arbitrary inputs - Li must be excluded to ensure consistency 
data = [['mp-1025496', 'Nb1 Se2'],
        ['mp-977563' , 'Nb1 Ir2'],
        ['mp-864631' , 'Nb1 Rh2'], 
        ['mp-3368'   , 'Nb3 O8']]

fdf = pd.DataFrame(data, columns = ['Id', 'Reduced Formula'])

## Initial conversion to matminer objects
from matminer.featurizers.conversions import StrToComposition
fdf = StrToComposition().featurize_dataframe(fdf, 'Reduced Formula')

from matminer.featurizers.conversions import CompositionToOxidComposition
fdf = CompositionToOxidComposition().featurize_dataframe(fdf, 'composition')

print("The initial dataset has {}".format(fdf.shape))
print(fdf.head())

'''
Block 2 - Featurization
'''
#
# -- start F1
from matminer.featurizers.composition import ElementProperty
ep_feat = ElementProperty.from_preset(preset_name='magpie')
fdf = ep_feat.featurize_dataframe(fdf, col_id='composition', ignore_errors=True)


# Excluding the 'MagpieData' string from the columns' names
magpie_cols = [col for col in fdf.columns if 'MagpieData' in col]

new_cols = []
for col in fdf.columns:
	if 'MagpieData' in col:
		new_col = col.split('MagpieData ', 1)
		del new_col[0]
		fin_col = ''.join(new_col)
		new_cols.append(fin_col)

cols_dict = dict(zip(magpie_cols, new_cols))
fdf = fdf.rename(columns=cols_dict)
# -- end F1

# -- start F3 --
from matminer.featurizers.composition import OxidationStates
os_feat = OxidationStates()
fdf = os_feat.featurize_dataframe(fdf, 'composition_oxid', ignore_errors=True)
# -- end F3

# -- start F4 -- 
from matminer.featurizers.composition import AtomicOrbitals
ao_feat = AtomicOrbitals()
fdf = ao_feat.featurize_dataframe(fdf, col_id='composition', ignore_errors=True)
# -- end F4

# -- start F5
from matminer.featurizers.composition import BandCenter
bce_feat = BandCenter()
fdf = bce_feat.featurize_dataframe(fdf, col_id='composition', ignore_errors=True)
# -- end F5

# -- start F6
from matminer.featurizers.composition import ElectronegativityDiff
eld_feat = ElectronegativityDiff()
fdf = eld_feat.featurize_dataframe(fdf, col_id='composition', ignore_errors=True)
# -- end F6

# -- start F7
from matminer.featurizers.composition import ElectronAffinity
ela_feat = ElectronAffinity()
fdf = ela_feat.featurize_dataframe(fdf, col_id='composition', ignore_errors=True)
# -- end F7

# -- start F9
from matminer.featurizers.composition import ValenceOrbital
vlo_feat = ValenceOrbital()
fdf = vlo_feat.featurize_dataframe(fdf, col_id='composition', ignore_errors=True)
# -- end F9

# -- start F10
from matminer.featurizers.composition import IonProperty
iop_feat = IonProperty()
fdf = iop_feat.featurize_dataframe(fdf, col_id='composition', ignore_errors=True)
# -- end F10

# -- start F12
from matminer.featurizers.composition import TMetalFraction
tmf_feat = TMetalFraction()
fdf = tmf_feat.featurize_dataframe(fdf, col_id='composition', ignore_errors=True)
# -- end F12

# End of the basic featurization

# Saving the database
print("The final dataset has {}".format(fdf.shape))
fdf.to_csv(r"Batteries_predict.csv", index = None, header = True)
store_dataframe_as_json(fdf, 'Batteries_predict.json', compression=None, orient='split')

'''
Block 3 - Loading and making predictions
'''

# Saving Id and Formula to an output dataframe odf
odf = pd.DataFrame() # output dataframe
odf['Id'] = fdf['Id']
odf['Reduced Formula'] = fdf['Reduced Formula']

excluded = ['Id', 'Reduced Formula', 'composition','composition_oxid',
            'HOMO_character', 'HOMO_element', 
            'LUMO_character', 'LUMO_element']

# A few additional adjustments
fdf = fdf.drop(excluded, axis=1)
fdf = fdf.replace([np.inf, -np.inf], np.nan)
fdf = fdf.fillna(0)

# No target variables, therefore:
X = fdf

# Normalizing the data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)

# Check dimensionality 
print('There are {} possible descriptors:\n{}'.format(X.shape[1], X.columns.values))

model = pickle.load(open('rf_model.pkl', 'rb'))

# Storing the predictions in the output dataframe
odf['Voltage'] = model.predict(X)

print ('\n---\n')
print ('Printing the results...')
print (odf.head())

odf.to_csv(r"predictions.csv", index = None, header = True)

print ('\n-- Done -- ')



