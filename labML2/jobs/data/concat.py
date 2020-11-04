#!/usr/bin/env python

'''concat.py: Script to concatenate several pandas dataframes from the MP'''

__author__     = 'Camilo A. Fernandes Salvador'
__email__      = 'csalvador@usp.br'
__copyright__  = 'Copyright © 2020, University of Sao Paulo'

import numpy as np
import pandas as pd
import regex as re

df0 = pd.read_csv("MP0.csv")
df1 = pd.read_csv("MP1.csv")
df2 = pd.read_csv("MP2.csv")
df3 = pd.read_csv("MP3.csv")
df4 = pd.read_csv("MP4.csv")
df5 = pd.read_csv("MP5.csv")
df6 = pd.read_csv("MP6.csv")
df7 = pd.read_csv("MP7.csv")

# Concat frames
frames = [df0, df1, df2, df3, df4, df5, df6, df7]
df = pd.concat(frames, axis=0, join='outer', ignore_index=False, keys=None)

'''
Block 1 - Data preparation 
'''
import matminer
from matminer.utils.io import store_dataframe_as_json

# Filtering the active ion and it's respective potential from the RCF
df[["Ion", "Reduced Formula"]] = df["Reduced Cell Formula"].str.split(" –", expand=True)
df[["Trash", "Reduced Formula"]] = df["Reduced Formula"].str.split(".", 1, expand=True)

# Avoid None/null exceptions where there are no decimals
df["Reduced Formula"] = np.where(pd.isnull(df["Reduced Formula"]), df["Trash"], df["Reduced Formula"])

# Cleaning [:2] potential residual numeric characters from "Reduced Formula"
clean1 = df["Reduced Formula"].str[0:1] # 1st char
df["RF1"] = df["Reduced Formula"].str[1:]
clean2 = df["Reduced Formula"].str[1:2] # 2nd char
df["RF2"] = df["Reduced Formula"].str[2:]

df["Reduced Formula"] = np.where((clean1.str.isnumeric()) & (clean2.str.isalpha()), df["RF1"], df["Reduced Formula"])
df["Reduced Formula"] = np.where((clean1.str.isnumeric()) & (clean2.str.isnumeric()), df["RF2"], df["Reduced Formula"])

print ("Null formulas: {}".format(df["Reduced Formula"].isna().sum()))

# Avoid None/null exceptions
df["Reduced Formula"] = np.where(pd.isnull(df["Reduced Formula"]), df["Ion"], df["Reduced Formula"])

# Defining the ions correctly 
df[["Id", "Ion"]] = df["Battid"].str.split("_", expand=True)

# Final check to avoid errors in the matminer.composition module
clean3 = df["Reduced Formula"].str[0:1] # 1st char
df["RF3"] = df["Reduced Formula"].str[1:]
df["Reduced Formula"] = np.where(clean3.str.isnumeric(), df["RF3"], df["Reduced Formula"])

excluded = ["Type", "Unnamed: 11", "Trash", "RF1", "RF2", "RF3", "Battid", "Reduced Cell Formula"]
df = df.drop(excluded, axis=1)

# Print a summary before writing
print ("A summary of the dataframe: {}".format(df.describe))
print ("The reduced formula column: {}".format(df["Reduced Formula"]))

# Exporting "df" to *.csv and *.json
df.to_csv(r"Batteries_raw.csv", index = None, header = True)
store_dataframe_as_json(df, 'Batteries_raw.json', compression=None, orient='split')

# Debug routine
# reduced = df["Reduced Formula"]
# reduced.to_csv(r"reduced.csv", index = None, header = True)



