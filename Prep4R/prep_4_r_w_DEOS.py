#!/usr/bin/env python2
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


Missing Dew Point Temperature
Run from the directory with the data files that contain all the data for each source (CMLF and DEOS)
"""


import numpy as np
import pandas as pd
import glob
#from dateutil.parser import parse
import datetime
import pytz
### 

fileTypes = ['DEOS','MET']
for fType in fileTypes:
    print fType
    
    for file in glob.glob("*"+fType+"*.csv"):
        print file
        data2 = pd.read_csv(file, low_memory=False)
        data2.columns.tolist()
        
      
        if (fType =='MET'):
            year = list(data2['YEAR'])
            month= list(data2['MONTH'])
            day = list(data2['DAY'])
            hour = list(data2['HOUR'])
            minute=list(data2['MINUTE'])
            second=list(data2['SECOND'])
            newTime = []
            for j in range(len(year)):
                local = pytz.timezone ("America/New_York")
                naive = datetime.datetime(int(year[j]),int(month[j]),int(day[j]),int(hour[j]),int(minute[j]),int(second[j]))
                local_dt = local.localize(naive, is_dst=True)
                utc_dt = local_dt.astimezone (pytz.utc)
                fmtTime= utc_dt.strftime('%Y%m%d%H%M%S')
                newTime.append(fmtTime)
                
            time = newTime
            wspd = data2['WIND_SPEED']
            wdir = data2['WIND_DIRECTION']
            temp = data2['AIR_TEMPERATURE']
            temp = temp + 273.15
            rh = data2['RELATIVE_HUMIDITY']
            pressure = data2['PRESSURE']
            pressure = pressure *100 
            comphdg = data2['COMPHDG']
            wdir2hdg = data2['WDIR2HDG']
            lat_met = data2['LATITUDE']
            lon_met = data2['LONGITUDE']
            lon_met = lon_met *-1
            elevation = 0


            #%%
            data_list = [time,wspd,wdir,temp,rh,pressure,lat_met,lon_met]
            DATA = np.zeros((len(time),(len(data_list)+5)))
            #DATA[:,0] = time
            DATA[:,2] = wspd
            DATA[:,3] = wdir
            DATA[:,4] = temp
            DATA[:,5] = rh
            DATA[:,6] = pressure
            DATA[:,7] = lat_met
            DATA[:,8] = lon_met
            
            list2Check = [wspd,wdir,temp,rh,pressure,lat_met,lon_met]

            for variable in range(len(list2Check)):
                tmpVariable = list(list2Check[variable])
                for i,tmpD in enumerate(list2Check[variable]):
                    #print i,tmpD
                    if (str(tmpD) =='nan'):
                        #print "in here"
                        tmpVariable[i] = -888888.0
                tmpVariable = np.array(tmpVariable)
                DATA[:,variable+2] = tmpVariable
                    #%%
            HEADER = ['ID_String', 'DATE','Wind_Speed','Wind_Direction','Air_Temperature','Relative Humidity','Pressure','Latitude','Longitude','Elevation','Name_string','FM_string','Source_string']

            cmlf_4_r = pd.DataFrame(DATA,columns = HEADER)
            cmlf_4_r['DATE']          = time

	    #TEMPORARY SENSOR HEIGHT OF 20 Meters Until We Can Get An Accurate Measurement
	    station_height = 20
	    newElevation = elevation + station_height

            cmlf_4_r['Elevation']     = newElevation
            cmlf_4_r['ID_String']     = 'CMLF'
            cmlf_4_r['Name_string']   = 'Delaware_Bay/DE-NJ'
            cmlf_4_r['FM_string']     = 'FM-13 SHIP'
            cmlf_4_r['Source_string'] = 'UDel/DRBA' 

            

            
            
            #%%  

        if (fType =='DEOS'):
            name_list = data2['Station_Name']
            year = list(data2['Year'])
            month= list(data2['Month'])
            day = list(data2['Day'])
            hour = list(data2['Hour'])
            minute=list(data2['Minute'])
	    ## Seconds assumed to be 0
            newTime = []
            for j in range(len(year)):
                local = pytz.timezone ("America/New_York")
                naive = datetime.datetime(int(year[j]),int(month[j]),int(day[j]),int(hour[j]),int(minute[j]),int(0))
                local_dt = local.localize(naive, is_dst=True)
                utc_dt = local_dt.astimezone (pytz.utc)
                fmtTime= utc_dt.strftime('%Y%m%d%H%M%S')
                newTime.append(fmtTime)
            
            time = newTime
            elevation = data2['Elevation']
            lat_met = data2['Latitude']
            lon_met = data2['Longitude'] 

            temp = data2['Air Temperature']
            temp = temp + 273.15
            wspd = data2['Wind Speed']
            wdir = data2['Wind Direction']
            rh = data2['Relative Humidity']
            pressure = data2['Barometric Pressure']
            pressure = pressure *100 
            
            
            FM_String = data2['FM_Code']
            Source_String = data2['Source_Code']
            ID_list = data2['Call_Sign']

            #%%
            data_list = [time,wspd,wdir,temp,rh,pressure,lat_met,lon_met]
            DATA = np.zeros((len(time),(len(data_list)+5)))
            #DATA[:,0] = time
            DATA[:,2] = wspd
            DATA[:,3] = wdir
            DATA[:,4] = temp
            DATA[:,5] = rh
            DATA[:,6] = pressure
            DATA[:,7] = lat_met
            DATA[:,8] = lon_met
            
            list2Check = [wspd,wdir,temp,rh,pressure,lat_met,lon_met]

            for variable in range(len(list2Check)):
                tmpVariable = list(list2Check[variable])
                for i,tmpD in enumerate(list2Check[variable]):
                    if (str(tmpD) =='nan' or str(tmpD) == ''):
                        tmpVariable[i] = -888888.0
                tmpVariable = np.array(tmpVariable)
                DATA[:,variable+2] = tmpVariable
                    #%%
            HEADER = ['ID_String', 'DATE','Wind_Speed','Wind_Direction','Air_Temperature','Relative Humidity','Pressure','Latitude','Longitude','Elevation','Name_string','FM_string','Source_string']
            deos_4_r = pd.DataFrame(DATA,columns = HEADER)
            deos_4_r['DATE'] = time
            deos_4_r['Elevation'] = elevation    
            deos_4_r['ID_String']     = ID_list   #CODE 
            deos_4_r['Name_string']   = name_list #Station Name  LOCATION/STATE
            deos_4_r['FM_string']     = FM_String
            deos_4_r['Source_string'] = Source_String
        
    ##
combineBOTH = pd.concat([cmlf_4_r, deos_4_r], axis=0) 
prep4r = combineBOTH.sort_values(by='DATE', ascending=1)

print prep4r.iloc[0]  

np.savetxt("/home/work/clouds_wind_climate/ferry_data/data_CMLF2011_2016_D2013_2017.txt", prep4r.values, fmt='%10s %20s %13.5f %13.5f %13.5f %13.5f %13.5f %20.5f %20.5f %13.5f %40s %20s %40s') ## ADD DEW POINT AT THE END
print len(prep4r)
