#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Updated on March 8th 2018

@author: Eric Allen, University of Delaware
Questions?: allenea@udel.edu

Cloud Wind and Climate Research Group & Delaware Environmental Observing System

This program combines all DEOS stations then trims data that is not needed for 
the little_r format. The next program prep4r_w_DEOS (or something like that)
will use the formatted output file from this. It is vital not to change anything in this 
file. If you would like to combine all the data and do something else. Copy the file
and choose what data to trim (if any data at all). 

# This file will take a little while to run since it is processing 5 years of 5 minute data
# from many stations
"""


import numpy as np
import pandas as pd
import glob
import os

HEADER = ["ID_String", 'DATE','Wind_Speed (m/s)','Wind_Direction (deg)',\
          'Air_Temperature (K)','Dewpoint_Temperature (K)','Relative_Humidity (%)','Pressure (Pa)',\
          'Latitude','Longitude','Elevation_SensorHeight (m)',\
          'Name_string','FM_string','Source_string',\
          'Elevation (m)','Wind_Sensor_Height (m)']

float64 = np.float64

dtypesDict={"ID_String": object, "DATE":float64, "Wind_Speed (m/s)":float64,\
            "Wind_Direction (deg)":float64, "Air_Temperature (K)"  : float64,\
            "Dewpoint_Temperature (K)" :float64, "Relative_Humidity (%)" :float64,\
            "Pressure (Pa)":float64, "Latitude"   :float64, "Longitude" :float64,\
            "Elevation_SensorHeight (m)":float64, "Name_string" : object, "FM_string" : object,\
            "Source_string" : object, "Elevation (m)"  : float64, "Wind_Sensor_Height (m)":float64}

os.chdir(os.getcwd()+"/Reformatted/")
outstring = os.path.abspath('../..')+"/Prep4R/All-DEOS-Data.csv"

allfiles =  glob.glob("*.csv")   
print ("DEOS File Count:", len(allfiles))

dfs = [pd.read_csv(f, usecols=HEADER,dtype=dtypesDict) for f in allfiles]
finaldf = pd.concat(dfs, axis=0, join='inner')
sortdf=finaldf.sort_values(['ID_String','DATE'])
sortdf = sortdf.mask(sortdf=='',  -888888.0)
sortdf = sortdf.mask(sortdf==' ',  -888888.0)
sortdf = sortdf.mask(sortdf==np.nan, -888888.0)
sortdf.to_csv(outstring,index=False) 