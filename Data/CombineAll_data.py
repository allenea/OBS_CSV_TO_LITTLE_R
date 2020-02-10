#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 09:43:07 2018

@author: allenea
"""
import numpy as np
import pandas as pd
import glob
import os

#%%
HEADER = ["ID_String", 'DATE','Wind_Speed (m/s)','Wind_Direction (deg)',\
          'Air_Temperature (K)','Dewpoint_Temperature (K)','Relative_Humidity (%)','Pressure (Pa)',\
          'Latitude','Longitude','Elevation_SensorHeight (m)',\
          'Name_string','FM_string','Source_string',\
          'Elevation (m)','Wind_Sensor_Height (m)']


outstring = os.getcwd()+"/All_Delaware_Data.csv"

os.chdir(os.getcwd()+"/All_Sources/")

allfiles = glob.glob("*.csv")
allfiles.sort()

print(allfiles)
print ("File Count: ",len(allfiles))
float64 = np.float64
dtypesDict={"ID_String": object, "DATE":float64, "Wind_Speed (m/s)":float64,\
            "Wind_Direction (deg)":float64, "Air_Temperature (K)"  : float64,\
            "Dewpoint_Temperature (K)" :float64, "Relative_Humidity (%)" :float64,\
            "Pressure (Pa)":float64, "Latitude"   :float64, "Longitude" :float64,\
            "Elevation_SensorHeight (m)":float64, "Name_string" : object, \
            "FM_string": object, "Source_string" : object, "Elevation (m)":float64,\
            "Wind_Sensor_Height (m)":float64}

dfs = [pd.read_csv(f, usecols=HEADER,dtype=dtypesDict) for f in allfiles]
finaldf = pd.concat(dfs, axis=0, join='inner')
sortdf=finaldf.sort_values(['ID_String','DATE'])
print("Number of Observations: ", len(sortdf))
sortdf = sortdf.replace('',-888888.0)
sortdf = sortdf.replace(' ', -888888.0)
sortdf = sortdf.replace(np.nan, -888888.0)
print(sortdf.dtypes)
sortdf.to_csv(outstring,index=False) 

