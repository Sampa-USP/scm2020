#!/usr/bin/env python

'''feat_data.py: Script to run a few compositional featurizers for a given database'''

__author__     = 'Camilo A. Fernandes Salvador'
__email__      = 'csalvador@usp.br'
__copyright__  = 'Copyright © 2020, University of Sao Paulo'

__author__ = ['Camilo F Salvador <csalvador@usp.br>']

import pandas as pd
import numpy as np
import os

from pymatgen import MPRester

import matminer
from matminer.data_retrieval.retrieve_MP import MPDataRetrieval
from matminer.utils.io import store_dataframe_as_json
from matminer.utils.io import load_dataframe_from_json
from matminer.figrecipes.plot import PlotlyFig

'''
#Block 1 - Loading and filtering the experimental dataframe
'''
df = load_dataframe_from_json('data/Batteries_raw.json')


# Select the working ion among {Li, Al, Zr, Mg}
select = 'Li'

# Initial filter based on the selected element
from matminer.featurizers.conversions import StrToComposition
fdf = StrToComposition().featurize_dataframe(df, 'Ion')

select_at = fdf["composition"].apply(lambda x: x.get_atomic_fraction(select))
fdf = fdf [select_at==1]

# Debug 
print ("Remaining samples: {}".format(fdf.describe))
fdf = fdf.drop(['composition'], axis=1)

## Initial conversion to matminer objects
from matminer.featurizers.conversions import StrToComposition
fdf = StrToComposition().featurize_dataframe(fdf, 'Reduced Formula')

from matminer.featurizers.conversions import CompositionToOxidComposition
fdf = CompositionToOxidComposition().featurize_dataframe(fdf, 'composition')

print("The initial dataset has {}".format(fdf.shape))
# fdf.to_csv(r"Batteries_feat.csv", index = None, header = True)

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

'''
# CohesiveEnergy demands a MP-KEY, APE is heavy on processing
#
print ("\nAvailable cores: {}".format(os.sched_getaffinity(0)))
os.sched_setaffinity(0, {1, 3}) # running on two cores
print ("\nRunning on {} cores".format(os.sched_getaffinity(0)))

# -- start F13
from matminer.featurizers.composition import CohesiveEnergy
coe_feat = CohesiveEnergy(mpkey)
fdf = coe_feat.featurize_dataframe(fdf, col_id='composition', ignore_errors=True)
# -- end F13

# -- start F16
from matminer.featurizers.composition import AtomicPackingEfficiency
ape_feat = AtomicPackingEfficiency()
fdf = ape_feat.featurize_dataframe(fdf, col_id='composition', ignore_errors=True)
# -- end F16
#
'''

# End of the basic featurization

# Saving the database
print("The final dataset has {}".format(fdf.shape))
fdf.to_csv(r"Batteries_feat.csv", index = None, header = True)
store_dataframe_as_json(fdf, 'Batteries_feat.json', compression=None, orient='split')

#
# --- end
