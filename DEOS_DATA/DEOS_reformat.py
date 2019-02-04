#!/usr/bin/env python3
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
"""

import numpy as np
import pandas as pd
import glob
from dateutil.parser import parse
import datetime
import os


def merge_csv(file1,file2):
    a = pd.read_csv(file1, low_memory=False)
    b = pd.read_csv(file2, low_memory=False)
    merged = pd.concat([a,b])
    merged.to_csv(mydir + '/Merged/'+file1[:4]+"-deos-verify-data.csv", index=False)

    
mydir =   os.getcwd()
#Makes data frame of metadata 
df = pd.read_csv(mydir+"/current_deos_metadata_csv.csv", low_memory=False)

stationName = df['Station Name']
callSign = df['Call Sign']
#county = df['County']
#state = df['ST']
latitude = df['Latitude (DD)']
longitude = df['Longitude (DD)']
elevation = df['Elev (m)']
sensor_height = df['Sensor_Height (m)']

#Include additional parameters for WRF Data Assimilation
FM_Code = 'FM-12 SYNOP'
Source_Code = 'Delaware_Environmental_Observing_System'
  
### SET PATHS
wkdir =   os.getcwd()+"/Raw/"  
outdir = os.getcwd()+'/Reformatted/'
os.chdir(wkdir)

#for each formatted file with DEOS data in the folder this program is executed         
fileList=glob.glob('*.csv')
fileList.sort()
mergedList = []
for file1 in fileList:
    for file2 in fileList:
        if file1[:4] == file2[:4] and file1 !=file2 and file1[:4] not in mergedList:
            #print file1, file2
            merge_csv(file1,file2)
            mergedList.append(file1[:4])
            print ("MERGED", file1[:4])
        elif file1[:4] != file2[:4] and file1!=file2 and file1[:4] not in mergedList and file2 == fileList[-1]  :
            #print file1, file2
            a = pd.read_csv(file1, low_memory=False)
            a.to_csv(mydir + '/Merged/'+file1[:4]+"-deos-verify-data.csv", index=False)
            print ("SINGLE" , file1[:4])
        elif file1[:4] == file2[:4] and file1==file2 and file1[:4] not in mergedList and file2 == fileList[-1]  :
            #print file1, file2
            a = pd.read_csv(file1, low_memory=False)
            a.to_csv(mydir + '/Merged/'+file1[:4]+"-deos-verify-data.csv", index=False)
            print ("SINGLE" , file1[:4])
print (fileList)


os.chdir(mydir+"/Merged/")


HEADER = ["ID_String", 'DATE','Wind_Speed (m/s)','Wind_Direction (deg)',\
          'Air_Temperature (K)','Dewpoint_Temperature (K)','Relative_Humidity (%)',\
          'Pressure (Pa)','Latitude','Longitude','Elevation_SensorHeight (m)',\
          'Name_string','FM_string','Source_string','Elevation (m)','Wind_Sensor_Height (m)']

#for each formatted file with DEOS data in the folder this program is executed         
for file in glob.glob('*.csv'):
    print (file)
    #Read it in
    station_data = pd.read_csv(file, low_memory=False)
    
    station_data = station_data.mask(station_data == -999.0, other= np.nan)
    station_data = station_data.mask(station_data == " ", other= np.nan)
    station_data = station_data.mask(station_data == "", other= np.nan)
    station_data.columns = station_data.columns.str.upper()
    station_data.columns = [x.split("(",1)[0] for x in station_data.columns]
    station_data.columns = station_data.columns.str.strip()
    station_data.columns = station_data.columns.str.replace(" ","_")
    #Parse Time_Stamp to individual Columns  
    sizeNew2 = int(len(station_data['TIMESTAMP']))

    newTime = [0]*sizeNew2;
    for i in range(sizeNew2):
        d = parse(station_data['TIMESTAMP'][i])
        utc_dt = datetime.datetime(int(d.year),int(d.month),int(d.day),int(d.hour),int(d.minute),int(d.second))
        newTime[i] = utc_dt.strftime('%Y%m%d%H%M%S')


    #trim to only include the 4 letter station name
    fileName = file[:4]
    
    #Add a directory path if you want
    outstring = outdir+fileName+"-w-Metadata.csv"
    
    newData = np.zeros((len(station_data),len(HEADER)))



    #See if it matches any of the stations in the metadata file
    for idx in range(len(callSign)):
        #If it does add the metadata to the file
        if callSign[idx] == fileName:
            #Parse Time Data- You could cut this part to save lots of CPU time.
            
            
            newData[:,1] = newTime
            try:
                newData[:,2] = station_data.WIND_SPEED.astype(float)
            except:
                print ("No Wind Speed Data " + callSign[idx])
                newData[:,2] = -888888.0
                
            try:
                newData[:,3] = station_data.WIND_DIRECTION.astype(float)
            except:
                print ("No Wind Direction Data " + callSign[idx])
                newData[:,3] = -888888.0
                
            try:
                newData[:,4] = station_data.AIR_TEMPERATURE.astype(float) +273.15 
            except:
                print ("No Air Temperature Data "+ callSign[idx])
                newData[:,4] = -888888.0
            try:
                newData[:,5] =  station_data.DEW_POINT_TEMPERATURE.astype(float) + 273.15
            except:
                print ("No Dew Point Temperature Data "+ callSign[idx])
                newData[:,5] = -888888.0    
            try:
                newData[:,6] = station_data['RELATIVE_HUMIDITY']
            except:
                print ("No RH Data " + callSign[idx])
                newData[:,6] = -888888.0
                
            try:
                newData[:,7] = station_data.BAROMETRIC_PRESSURE.astype(float) * 100.0
            except:
                print ("No Barometric Pressure " + callSign[idx])
                newData[:,7] =  -888888.0
                
            newData[:,8] = latitude[idx]    
            newData[:,9] = longitude[idx]
            newData[:,10] = elevation[idx]+ sensor_height[idx]  ## USE THIS IN DA
            newData[:,14] = elevation[idx]
            newData[:,15] = sensor_height[idx]

            print ("Sensor Height ",callSign[idx],"  =  ",sensor_height[idx])
            
            dfwrite = pd.DataFrame(newData, columns = HEADER)
            
            dfwrite["ID_String"]= callSign[idx]   #0
            dfwrite["Name_string"]= stationName[idx]#11
            dfwrite["FM_string"]=FM_Code #12
            dfwrite["Source_string"]=Source_Code #13
                    
            #dfwrite = dfwrite.mask(dfwrite == np.nan, -888888.0)
            #dfwrite = dfwrite.mask(dfwrite == '',  -888888.0)

            #Concatenate the DataFrames 
            output_data= dfwrite

            #Save the output file
            output_data.to_csv(outstring,index=False)
