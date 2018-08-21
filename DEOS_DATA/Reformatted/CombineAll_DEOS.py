#!/usr/bin/env python2
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

IMPORTANT: HARD CODED numOBS = 525888  for speed.!!! It seemed to take longer
each file with additional observations when I was appending. I know this greatly
increases the speed in matlab but I can't remember if the same applies to python.
Append will probably work better in the long run if/when this code is used
for a real time model.

####### USER ##########
THIS IS HARD CODED FOR THE SIZE OF THE FILES. The code is there to make it dynamic. But it will be much slower. Dynamic would be better for real-time processing.

Change outstring for your computer
"""

import numpy as np
import csv
import pandas as pd
import glob
import time as t
from itertools import islice


HEADERS = []
output = []

for file in glob.glob("*.csv"):
    print file
    with open(file,'rU') as infile:
        raw = csv.reader(infile,dialect='excel',delimiter=',')
        count = 0
        for row in raw:
            row2 = row[0:23]
            if count <= 0:
                HEADERS.append(row2)
            else:
                break
            count = count +1
    break
print HEADERS

HEADER = np.array(HEADERS)
dtf = pd.DataFrame(HEADER,index=None)
#%%              

allfiles = []

##Path to save the output file
#outstring = "/home/work/clouds_wind_climate/ferry_data/DEOS_DATA/All_Data/All-DEOS-Data.csv"
outstring = "/home/work/clouds_wind_climate/ferry_data/Prep4R/All-DEOS-Data.csv"


for file in glob.glob("*.csv"):
   allfiles.append(file)
print allfiles

#%%
filecount = len(allfiles)
########### HARD CODED - SEE COMMENTS HERE AND ABOVE##########

numOBS = 525888  #HARDCODED TO IMPROVE SPEED WITH LIKE 11 MILLION OBS
output = list(np.zeros((numOBS*filecount,23)))
#output = []
count = 0
########################################

print filecount
if filecount > 0:  
    for i  in range(filecount):
        with open(allfiles[i],'rU') as infile:
            raw = csv.reader(infile,dialect='excel',delimiter=',')
            print raw
            next(islice(raw, 1, 1), None)  
            for row in raw:
                ##output.append(row[0:23]) ## KEEP
                output[count] = row[0:23]
                count +=1
                
    print "Done with combining files, now onto formatting"
    
    #%%       
    newHEADER = ["Call_Sign","Station_Name","County","State","Year","Month","Day","Hour","Minute","Longitude","Latitude","Elevation","Air Temperature","Wind Speed","Wind Direction","Barometric Pressure","Radiation","Wind_Gust","Guage","Relative Humidity","Time_Stamp", "FM_Code","Source_Code"]
    df = pd.DataFrame(output,index=None,columns=newHEADER)
    
    # SELECT WHICH COLUMNS OF DATA YOU WANT TRIMMED. Not needed for Little_R
    cut_data = df.drop(df.columns[[0, 2, 3,16,17,18,20]], axis=1)
    
    # add the call sign to the from. 
    #I wanted to have the Call Sign in the first column to help the user for readability
    finalData = pd.concat([cut_data,df["Call_Sign"]],axis=1)
    
    #save to a csv file. This will likely crash Excel or only load partial data.
    #If you must view this file I suggest using TextEdit. The file will be over 10M lines (observations)
    finalData.to_csv(outstring,index=False)
