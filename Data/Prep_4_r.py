#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Updated on March 8th 2018
@author: Eric Allen, University of Delaware
Questions?: allenea@udel.edu

Cloud Wind and Climate Research Group & Delaware Environmental Observing System

This file processes DEOS and Cape May Lewes Ferry data that have been
combined and quality controlled/reformatted to meet the specifications
to run this program. This file must be run from the same directory
containing those files. This file will create an output text file
(~3.27GB for me) which can then be used to write the data to
little_r format for a specified case study. Formatting in that will be
cruicial and that file will be written to handle data specifically
formatted from this file. Adjustments to this file might impact the
ability of the other files.

THIS IS NOT THE MOST EFFICIENT WAY TO DO THIS.....
Basically would need to drop last 2 columns and change column names
then drop last 2 columns, then replace the data. Sort by date and then save to text file
Missing Dew Point Temperature

{'13764': 'KGED', '03726': 'KWWD', '13707': 'KDOV', '13735': 'KMIV', '93739': 'KWAL',
 '00356': 'KCGE', '93720': 'KSBY', '93786': 'KOXB', '03756': 'KESN', '93730': 'KACY'}
['13735', '13707', '93786', '03726', '00356', '03756', '13764', '93739', '93720', '93730']
"""
#IMPORTS
import glob
import os
#import sys
import numpy as np
import pandas as pd

HEADERIN = ["ID_String", 'DATE', 'Wind_Speed (m/s)', 'Wind_Direction (deg)',\
          'Air_Temperature (K)', 'Dewpoint_Temperature (K)', 'Relative_Humidity (%)',\
          'Pressure (Pa)',\
          'Latitude', 'Longitude', 'Elevation_SensorHeight (m)',\
          'Name_string', 'FM_string', 'Source_string',\
          'Elevation (m)', 'Wind_Sensor_Height (m)']

HEADER = ['ID_String', 'DATE', 'Wind_Speed', 'Wind_Direction', 'Air_Temperature',\
          'Dewpoint_Temperature',\
          'Relative Humidity', 'Pressure', 'Latitude', 'Longitude', 'Elevation',\
          'Name_string', 'FM_string', 'Source_string']


float64 = np.float64
dtypesDict = {"ID_String": object, "DATE":float64, "Wind_Speed (m/s)":float64,\
            "Wind_Direction (deg)":float64,\
            "Air_Temperature (K)"  : float64, "Dewpoint_Temperature (K)":float64,\
            "Relative_Humidity (%)" :float64,\
            "Pressure (Pa)":float64, "Latitude":float64, "Longitude":float64,\
            "Elevation_SensorHeight (m)":float64,\
            "Name_string":object, "FM_string":object, "Source_string":object,\
            "Elevation (m)":float64, "Wind_Sensor_Height (m)":float64}

outdir = os.path.abspath('../')
os.chdir(outdir)
print(outdir)
filelist = glob.glob("*_OBS.csv")
for file in filelist:
    #print(file[19:22])
    data2 = pd.read_csv(file, dtype=dtypesDict, header=0)
    data2.columns = HEADERIN
    newdf = data2.drop(['Elevation (m)', 'Wind_Sensor_Height (m)'], axis=1)
    newdf.columns.tolist()
    newdf.columns = HEADER

    newdf = newdf.replace(" ", -888888.0)
    newdf = newdf.replace("", -888888.0)
    newdf = newdf.replace(np.nan, -888888.0)
    newdf = newdf.replace("nan", -888888.0)
    newdf = newdf.replace(-3010120249.14000, -888888.0)
    newdf['Name_string'] = newdf['Name_string'].str.replace(" ", "_")
    newdf['Source_string'] = newdf['Source_string'].str.replace(" ", "_")
    prep4r = newdf.sort_values(by='DATE', ascending=1)
    print(prep4r.iloc[0])
    print(len(prep4r))

    np.savetxt(outdir+"/all_delaware_data_eric_thesis_"+str(file[19:22])+".txt",\
      prep4r.values,\
      fmt='%10s %20s %13.5f %13.5f %13.5f %13.5f %13.5f %13.5f %20.5f %20.5f %13.5f %40s %20s %40s')
