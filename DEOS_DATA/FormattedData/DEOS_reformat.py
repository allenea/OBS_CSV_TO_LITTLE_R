#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Last Updated on Monday March  5th, 2018

@author: Eric Allen
email: allenea@udel.edu
University of Delaware
Clouds_Wind_Climate Research Group and DEOS

Reformat the DEOS data to include the metadata for each station.
Some of this information is redundant but everything in the original data file
and more is here. The time has been parsed (YYYY  MM DD HH mm ).
User should decide what he/she would like to use when reading in the output file.
Feel free to modify for your own needs.

If you do not need to parse time I highly consider removing the parsing. That 
adds a lot more CPU time for the program to finish. But if you will eventually 
need to parse the time then you might as well do it now. 

********Combines Sensor heights with elevation  and assigned to the elevation variable ********

Update mydir 
"""



import numpy as np
import pandas as pd
import glob
from dateutil.parser import parse


#UPDATE FOR THE PATH OF FILE ON YOUR COMPUTER
mydir ="/home/work/clouds_wind_climate/ferry_data/DEOS_DATA/"

#Makes data frame of metadata 
df = pd.read_csv(mydir+"current_deos_metadata_csv.csv")

stationName = df['Station Name']
callSign = df['Call Sign']
county = df['County']
state = df['ST']
latitude = df['Latitude (DD)']
longitude = df['Longitude (DD)']
elevation = df['Elev (m)']
sensor_height = df['Sensor_Height (m)']

#Include additional parameters for WRF Data Assimilation
FM_Code = 'FM-12 SYNOP'
Source_Code = 'Delaware_Environmental_Observing_System'
  
#Initialize the Header (DONE ONCE)
HEADING = ["Call_Sign", "Station_Name","County","State","Year","Month","Day","Hour","Minute", "Longitude","Latitude","Elevation"]

#for each formatted file with DEOS data in the folder this program is executed         
for file in glob.glob('*.csv'):
    #Read it in
    station_data = pd.read_csv(file, low_memory=False)
    Trimmed_station_data = station_data.drop(["Time_stamp"],axis=1)
            
    #Parse Time_Stamp to individual Columns  
    sizeNew2 = int(len(station_data["Time_stamp"]))
    year_raw = [0]*sizeNew2; month_raw = [0]*sizeNew2; day_raw = [0]*sizeNew2;
    hour_raw = [0]*sizeNew2; min_raw   = [0]*sizeNew2;
    for i in range(sizeNew2):
        d = parse(station_data["Time_stamp"][i])
        year_raw[i] = d.year
        month_raw[i] = d.month
        day_raw[i] = d.day
        hour_raw[i] = d.hour
        min_raw[i] = d.minute

        
    #trim to only include the 4 letter station name
    fileName = file[:4]
    print fileName
    #Add a directory path if you want
    outstring = mydir+"Reformatted/"+fileName+"-w-Metadata.csv"

    #print len(station_data), fileName
    newData = np.zeros((len(station_data),12))
    wrfData = np.zeros((len(station_data),2))

    #See if it matches any of the stations in the metadata file
    for idx in range(len(callSign)):
        
    #If it does add the metadata to the file
        if callSign[idx] == fileName:
            #Parse Time Data- You could cut this part to save lots of CPU time.
            newData[:,4] = year_raw
            newData[:,5] = month_raw
            newData[:,6] = day_raw
            newData[:,7] = hour_raw
            newData[:,8] = min_raw
                   
            newData[:,9] = longitude[idx]
            newData[:,10] = latitude[idx]    
            newData[:,11] = elevation[idx]  + sensor_height[idx] 
            print "Sensor Height",callSign[idx],"  =  ",sensor_height[idx]

            dfwrite = pd.DataFrame(newData, columns = HEADING)
            
            dfwrite["Call_Sign"]= callSign[idx]
            dfwrite["Station_Name"]= stationName[idx]
            dfwrite["County"]=county[idx]
            dfwrite["State"]=state[idx]
            
            WRF_INFO = pd.DataFrame(wrfData,columns=["FM_Code","Source_Code"])
            
            WRF_INFO["FM_Code"]=FM_Code
            WRF_INFO["Source_Code"]=Source_Code
                    
                    
            #Concatenate the DataFrames 
            output_data= pd.concat([dfwrite, Trimmed_station_data, station_data["Time_stamp"],WRF_INFO], axis=1)

            #Save the output file
            output_data.to_csv(outstring,index=False)
