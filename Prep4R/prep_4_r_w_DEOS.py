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
"""


import numpy as np
import pandas as pd
import glob
import os 
import datetime
import pytz

fileTypes = ['DEOS','MET']
for fType in fileTypes:
    print (fType)
    for file in glob.glob("*"+fType+"*.csv"):
        print (file)

        if (fType =='MET'):
            """
            From what I can tell the original ferry data was collected in UTC time then converted to local time in the raw data files
            """
            data2 = pd.read_csv(file, low_memory=False)
            data2.columns.tolist()
            # GROSS ERROR CHECKS
            data2['WIND_SPEED'] = data2['WIND_SPEED'].mask(data2['WIND_SPEED'] > 74, other = np.nan)
            data2['AIR_TEMPERATURE'] = data2['AIR_TEMPERATURE'].mask(data2['AIR_TEMPERATURE'] > 55, other = np.nan)
            data2['WIND_DIRECTION'] = data2['WIND_DIRECTION'].mask(data2['WIND_DIRECTION'] >= 360, other = np.nan)

            
            year = list(data2['YEAR'])
            month= list(data2['MONTH'])
            day = list(data2['DAY'])
            hour = list(data2['HOUR'])
            minute=list(data2['MINUTE'])
            second=list(data2['SECOND'])
            
            newTime = []
            for j in range(len(year)):
                #local = pytz.timezone ("America/New_York")
                naive = datetime.datetime(int(year[j]),int(month[j]),int(day[j]),int(hour[j]),int(minute[j]),int(second[j]))
                #local_dt = local.localize(naive, is_dst=True)
                #utc_dt = local_dt.astimezone (pytz.utc)
                fmtTime= naive.strftime('%Y%m%d%H%M%S')
                newTime.append(fmtTime)
                
            time = newTime
            wspd = data2['WIND_SPEED']
            wspd = wspd * 0.44704
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


            HEADER = ["ID_String", 'DATE','Wind_Speed','Wind_Direction',\
                  'Air_Temperature','Dewpoint_Temperature','Relative_Humidity','Pressure',\
                  'Latitude','Longitude',"Elevation_SensorHeight",\
                  'Name_string','FM_string','Source_string', "Elevation", "Wind_Sensor_Height"]
            #OLD HEADER = ["ID_String", 'DATE','Wind_Speed','Wind_Direction','Air_Temperature','Relative Humidity','Pressure','Latitude','Longitude','Elevation','Name_string','FM_string','Source_string']


            DATA = np.zeros((len(time),len(HEADER)))
            
            #DATA[:,0] = time
            DATA[:,2] = wspd
            DATA[:,3] = wdir
            DATA[:,4] = temp
            #DATA[:,5] = -888888.0 #DEW POINT

            DATA[:,6] = rh
            DATA[:,7] = pressure
            DATA[:,8] = lat_met
            DATA[:,9] = lon_met
            
            cmlf_4_r = pd.DataFrame(DATA,columns = HEADER)
            
            cmlf_4_r['ID_String']     = 'CMLF' #0
            cmlf_4_r['DATE'] = time #1
            cmlf_4_r['DATE']= cmlf_4_r['DATE'].astype(np.float)

            cmlf_4_r['Dewpoint_Temperature'] = -888888.0 # 5 spot
            
            #TEMPORARY SENSOR HEIGHT OF 20 Meters Until We Can Get An Accurate Measurement
            station_height = 20.0
            newElevation = elevation + station_height
            
            
            cmlf_4_r['Elevation_SensorHeight']     = newElevation #10
            cmlf_4_r['Name_string']   = 'Delaware_Bay/DE-NJ' #11
            cmlf_4_r['FM_string']     = 'FM-13 SHIP' #12
            cmlf_4_r['Source_string']     = 'UDel/DRBA' #13
            cmlf_4_r['Elevation'] = elevation #14
            cmlf_4_r['Wind_Sensor_Height'] = station_height #15

            cmlf_4_r['Pressure'] = cmlf_4_r['Pressure'].mask(cmlf_4_r['Pressure'] == 80010, other=np.nan)
            cmlf_4_r['Pressure'] = cmlf_4_r['Pressure'].mask(cmlf_4_r['Pressure'] == 80000, other=np.nan)




            print ("***************** Max/Min/Mean ANALYSIS OF THE FERRY DATA **************")
            cmlf_4_r.columns = ["ID_String", 'DATE','Wind_Speed (m/s)','Wind_Direction (deg)',\
                  'Air_Temperature (K)','Dewpoint_Temperature (K)','Relative_Humidity (%)','Pressure (Pa)',\
                  'Latitude','Longitude',"Elevation_SensorHeight (m)",\
                  'Name_string','FM_string','Source_string', "Elevation (m)", "Wind_Sensor_Height (m)"]
            

            print ("Date:")
            print (np.nanmax(cmlf_4_r["DATE"]))
            print (np.nanmin(cmlf_4_r["DATE"]))
            print (np.nanmean(cmlf_4_r['DATE']))
            
            
            print ("Wind Speed:")
            print (np.nanmax(cmlf_4_r['Wind_Speed (m/s)']))
            print (np.nanmin(cmlf_4_r['Wind_Speed (m/s)']))
            print (np.nanmean(cmlf_4_r['Wind_Speed (m/s)']))
            
            print ("Wind Direction:")
            print (np.nanmax(cmlf_4_r['Wind_Direction (deg)']))
            print (np.nanmin(cmlf_4_r['Wind_Direction (deg)']))
            print (np.nanmean(cmlf_4_r['Wind_Direction (deg)']))
            
            print ("Air Temperature:")
            print (np.nanmax(cmlf_4_r['Air_Temperature (K)']))
            print (np.nanmin(cmlf_4_r['Air_Temperature (K)']))
            print (np.nanmean(cmlf_4_r['Air_Temperature (K)']))
            
            print ("NO DEW POINT TEMPERATURE DATA")
            
            print ("Relative Humidity:")
            print (np.nanmax(cmlf_4_r['Relative_Humidity (%)']))
            print (np.nanmin(cmlf_4_r['Relative_Humidity (%)']))
            print (np.nanmean(cmlf_4_r['Relative_Humidity (%)']))
            
            
            print ("Pressure:")
            print (np.nanmax(cmlf_4_r['Pressure (Pa)']))
            print (np.nanmin(cmlf_4_r['Pressure (Pa)']))
            print (np.nanmean(cmlf_4_r['Pressure (Pa)']))
            
            print ("Latitude:")
            print (np.nanmax(cmlf_4_r['Latitude']))
            print (np.nanmin(cmlf_4_r['Latitude']))
            print (np.nanmean(cmlf_4_r['Latitude']))
            
            print ("Longitude:")
            print (np.nanmax(cmlf_4_r['Longitude']))
            print (np.nanmin(cmlf_4_r['Longitude']))
            print (np.nanmean(cmlf_4_r['Longitude']))
            
            print ("Elevation + Sensor:")
            print (np.nanmax(cmlf_4_r['Elevation_SensorHeight (m)']))
            print (np.nanmin(cmlf_4_r['Elevation_SensorHeight (m)']))
            print (np.nanmean(cmlf_4_r['Elevation_SensorHeight (m)']))
            
            
            print ("Elevation:")
            print (np.nanmax(cmlf_4_r['Elevation (m)']))
            print (np.nanmin(cmlf_4_r['Elevation (m)']))
            print (np.nanmean(cmlf_4_r['Elevation (m)']))
            
            print ("Wind Sensor Height:")
            print (np.nanmax(cmlf_4_r['Wind_Sensor_Height (m)']))
            print (np.nanmin(cmlf_4_r['Wind_Sensor_Height (m)']))
            print (np.nanmean(cmlf_4_r['Wind_Sensor_Height (m)']))
            print("******************** END ANALYSIS ********************************")
            print()

            
            
            cmlf_4_r = cmlf_4_r.replace(" ", -888888.0)
            cmlf_4_r = cmlf_4_r.replace("",  -888888.0)
            cmlf_4_r = cmlf_4_r.replace(np.nan, -888888.0)
            cmlf_4_r = cmlf_4_r.replace("nan", -888888.0)
            #%%  

        if (fType =='DEOS'):
            HEADER =  ["ID_String", 'DATE','Wind_Speed (m/s)','Wind_Direction (deg)',\
                  'Air_Temperature (K)','Dewpoint_Temperature (K)','Relative_Humidity (%)','Pressure (Pa)',\
                  'Latitude','Longitude',"Elevation_SensorHeight (m)",\
                  'Name_string','FM_string','Source_string', "Elevation (m)", "Wind_Sensor_Height (m)"]

            float64 = np.float64
            dtypesDict={"ID_String": object, "DATE":float64, "Wind_Speed (m/s)":float64, "Wind_Direction (deg)":float64,\
                        "Air_Temperature (K)"  : float64, "Dewpoint_Temperature (K)" :float64, "Relative_Humidity (%)" :float64,\
                        "Pressure (Pa)":float64, "Latitude"   :float64, "Longitude" :float64, "Elevation_SensorHeight (m)":float64,\
                        "Name_string":object, "FM_string":object, "Source_string":object, "Elevation (m)":float64, "Wind_Sensor_Height (m)":float64}

            deos_4_r = pd.read_csv(file, dtype=dtypesDict, header=0)
            #deos_4_r = data2.drop(['Elevation (m)','Wind_Sensor_Height (m)'],axis=1)
            deos_4_r.columns.tolist()
            deos_4_r.columns = HEADER

            deos_4_r['Wind_Speed (m/s)'] = deos_4_r['Wind_Speed (m/s)'].mask(deos_4_r['Wind_Speed (m/s)'] ==65.9, other = np.nan)

            print ("***************** Max/Min/Mean ANALYSIS OF THE DEOS DATA **************")
            print ("Date:")
            print (np.nanmax(deos_4_r["DATE"]))
            print (np.nanmin(deos_4_r["DATE"]))
            print (np.nanmean(deos_4_r['DATE']))
            
            
            print ("Wind Speed:")
            print (np.nanmax(deos_4_r['Wind_Speed (m/s)']))
            print (np.nanmin(deos_4_r['Wind_Speed (m/s)']))
            print (np.nanmean(deos_4_r['Wind_Speed (m/s)']))
            
            print ("Wind Direction:")
            print (np.nanmax(deos_4_r['Wind_Direction (deg)']))
            print (np.nanmin(deos_4_r['Wind_Direction (deg)']))
            print (np.nanmean(deos_4_r['Wind_Direction (deg)']))
            
            print ("Air Temperature:")
            print (np.nanmax(deos_4_r['Air_Temperature (K)']))
            print (np.nanmin(deos_4_r['Air_Temperature (K)']))
            print (np.nanmean(deos_4_r['Air_Temperature (K)']))
            
            print ("NO DEW POINT TEMPERATURE DATA")
            
            print ("Relative Humidity:")
            print (np.nanmax(deos_4_r['Relative_Humidity (%)']))
            print (np.nanmin(deos_4_r['Relative_Humidity (%)']))
            print (np.nanmean(deos_4_r['Relative_Humidity (%)']))
            
            
            print ("Pressure:")
            print (np.nanmax(deos_4_r['Pressure (Pa)']))
            print (np.nanmin(deos_4_r['Pressure (Pa)']))
            print (np.nanmean(deos_4_r['Pressure (Pa)']))
            
            print ("Latitude:")
            print (np.nanmax(deos_4_r['Latitude']))
            print (np.nanmin(deos_4_r['Latitude']))
            print (np.nanmean(deos_4_r['Latitude']))
            
            print ("Longitude:")
            print (np.nanmax(deos_4_r['Longitude']))
            print (np.nanmin(deos_4_r['Longitude']))
            print (np.nanmean(deos_4_r['Longitude']))
            
            print ("Elevation + Sensor:")
            print (np.nanmax(deos_4_r['Elevation_SensorHeight (m)']))
            print (np.nanmin(deos_4_r['Elevation_SensorHeight (m)']))
            print (np.nanmean(deos_4_r['Elevation_SensorHeight (m)']))
            
            
            print ("Elevation:")
            print (np.nanmax(deos_4_r['Elevation (m)']))
            print (np.nanmin(deos_4_r['Elevation (m)']))
            print (np.nanmean(deos_4_r['Elevation (m)']))
            
            print ("Wind Sensor Height:")
            print (np.nanmax(deos_4_r['Wind_Sensor_Height (m)']))
            print (np.nanmin(deos_4_r['Wind_Sensor_Height (m)']))
            print (np.nanmean(deos_4_r['Wind_Sensor_Height (m)']))
            print("******************** END ANALYSIS ********************************")
            print()

            
            deos_4_r = deos_4_r.replace(" ", -888888.0)
            deos_4_r = deos_4_r.replace( "",  -888888.0)
            deos_4_r = deos_4_r.replace( np.nan, -888888.0)
            deos_4_r = deos_4_r.replace( "nan", -888888.0)
            deos_4_r = deos_4_r.replace( -3010120249.14000, -888888.0)
            ## OLD HEADER = ["ID_String", 'DATE','Wind_Speed','Wind_Direction','Air_Temperature','Relative Humidity','Pressure','Latitude','Longitude','Elevation','Name_string','FM_string','Source_string']


#%%
combineBOTH = pd.concat([cmlf_4_r, deos_4_r], axis=0) 
prep4r = combineBOTH.sort_values(by='DATE', ascending=1)
prep4r.columns =  ["ID_String", 'DATE','Wind_Speed (m/s)','Wind_Direction (deg)',\
                  'Air_Temperature (K)','Dewpoint_Temperature (K)','Relative_Humidity (%)','Pressure (Pa)',\
                  'Latitude','Longitude',"Elevation_SensorHeight (m)",\
                  'Name_string','FM_string','Source_string', "Elevation (m)", "Wind_Sensor_Height (m)"]

prep4r = prep4r.mask(prep4r == -888888.0, other= np.nan)
print()
print()

print ("***************** Max/Min/Mean ANALYSIS OF THE DATA **************")

print ("Date:")
print (np.nanmax(prep4r["DATE"]))
print (np.nanmin(prep4r["DATE"]))
print (np.nanmean(prep4r['DATE']))


print ("Wind Speed:")
print (np.nanmax(prep4r['Wind_Speed (m/s)']))
print (np.nanmin(prep4r['Wind_Speed (m/s)']))
print (np.nanmean(prep4r['Wind_Speed (m/s)']))

print ("Wind Direction:")
print (np.nanmax(prep4r['Wind_Direction (deg)']))
print (np.nanmin(prep4r['Wind_Direction (deg)']))
print (np.nanmean(prep4r['Wind_Direction (deg)']))

print ("Air Temperature:")
print (np.nanmax(prep4r['Air_Temperature (K)']))
print (np.nanmin(prep4r['Air_Temperature (K)']))
print (np.nanmean(prep4r['Air_Temperature (K)']))

print ("NO DEW POINT TEMPERATURE DATA")

print ("Relative Humidity:")
print (np.nanmax(prep4r['Relative_Humidity (%)']))
print (np.nanmin(prep4r['Relative_Humidity (%)']))
print (np.nanmean(prep4r['Relative_Humidity (%)']))


print ("Pressure:")
print (np.nanmax(prep4r['Pressure (Pa)']))
print (np.nanmin(prep4r['Pressure (Pa)']))
print (np.nanmean(prep4r['Pressure (Pa)']))

print ("Latitude:")
print (np.nanmax(prep4r['Latitude']))
print (np.nanmin(prep4r['Latitude']))
print (np.nanmean(prep4r['Latitude']))

print ("Longitude:")
print (np.nanmax(prep4r['Longitude']))
print (np.nanmin(prep4r['Longitude']))
print (np.nanmean(prep4r['Longitude']))

print ("Elevation + Sensor:")
print (np.nanmax(prep4r['Elevation_SensorHeight (m)']))
print (np.nanmin(prep4r['Elevation_SensorHeight (m)']))
print (np.nanmean(prep4r['Elevation_SensorHeight (m)']))


print ("Elevation:")
print (np.nanmax(prep4r['Elevation (m)']))
print (np.nanmin(prep4r['Elevation (m)']))
print (np.nanmean(prep4r['Elevation (m)']))

print ("Wind Sensor Height:")
print (np.nanmax(prep4r['Wind_Sensor_Height (m)']))
print (np.nanmin(prep4r['Wind_Sensor_Height (m)']))
print (np.nanmean(prep4r['Wind_Sensor_Height (m)']))
print("******************** END ANALYSIS ********************************")

print()
print()



prep4r['Wind_Direction (deg)'] = prep4r['Wind_Direction (deg)'].mask(prep4r['Wind_Direction (deg)'] > 360, other = np.nan)
prep4r['Wind_Direction (deg)'] = prep4r['Wind_Direction (deg)'].mask(prep4r['Wind_Direction (deg)'] < 0, other = np.nan)

prep4r['Wind_Speed (m/s)'] = prep4r['Wind_Speed (m/s)'].mask(prep4r['Wind_Speed (m/s)'] <= 0, other = np.nan)
prep4r['Wind_Speed (m/s)'] = prep4r['Wind_Speed (m/s)'].mask(prep4r['Wind_Speed (m/s)'] > 74, other = np.nan)
print ("Masked Wind Speed Starting at 165 MPH (74m/s) - stronger than an EF-3 tornado or Category 5 Hurricane")

prep4r['Air_Temperature (K)'] = prep4r['Air_Temperature (K)'].mask(prep4r['Air_Temperature (K)'] < 255, other = np.nan)
prep4r['Air_Temperature (K)'] = prep4r['Air_Temperature (K)'].mask(prep4r['Air_Temperature (K)'] > 322, other = np.nan)
prep4r['Dewpoint_Temperature (K)'] = prep4r['Dewpoint_Temperature (K)'].mask(prep4r['Dewpoint_Temperature (K)'] < 244, other = np.nan)
prep4r['Dewpoint_Temperature (K)'] = prep4r['Dewpoint_Temperature (K)'].mask(prep4r['Dewpoint_Temperature (K)'] > 322, other = np.nan)
print ("Masked Temperatures and Dewpoint Temperatures Below 0 degF (-20 F Td) or above 120 degF")

prep4r['Relative_Humidity (%)'] = prep4r['Relative_Humidity (%)'].mask(prep4r['Relative_Humidity (%)'] < 0, other = np.nan)
prep4r['Relative_Humidity (%)'] = prep4r['Relative_Humidity (%)'].mask(prep4r['Relative_Humidity (%)'] > 100, other = np.nan)
print ("Masked Relative Humidity Below 0 % or above 100 %")


prep4r['Pressure (Pa)'] = prep4r['Pressure (Pa)'].mask(prep4r['Pressure (Pa)'] < 85000.0, other = np.nan)
prep4r['Pressure (Pa)'] = prep4r['Pressure (Pa)'].mask(prep4r['Pressure (Pa)'] > 108500.0, other = np.nan)
print ("Masked Pressure Below 850mb or above 1085 mb")


print()
print()


print ("***************** Max/Min/Mean ANALYSIS OF THE QUALITY CONTROLLED DATA **************")
print ("Date:")
print (np.nanmax(prep4r["DATE"]))
print (np.nanmin(prep4r["DATE"]))
print (np.nanmean(prep4r['DATE']))


print ("Wind Speed:")
print (np.nanmax(prep4r['Wind_Speed (m/s)']))
print (np.nanmin(prep4r['Wind_Speed (m/s)']))
print (np.nanmean(prep4r['Wind_Speed (m/s)']))

print ("Wind Direction:")
print (np.nanmax(prep4r['Wind_Direction (deg)']))
print (np.nanmin(prep4r['Wind_Direction (deg)']))
print (np.nanmean(prep4r['Wind_Direction (deg)']))

print ("Air Temperature:")
print (np.nanmax(prep4r['Air_Temperature (K)']))
print (np.nanmin(prep4r['Air_Temperature (K)']))
print (np.nanmean(prep4r['Air_Temperature (K)']))

print ("NO DEW POINT TEMPERATURE DATA")

print ("Relative Humidity:")
print (np.nanmax(prep4r['Relative_Humidity (%)']))
print (np.nanmin(prep4r['Relative_Humidity (%)']))
print (np.nanmean(prep4r['Relative_Humidity (%)']))


print ("Pressure:")
print (np.nanmax(prep4r['Pressure (Pa)']))
print (np.nanmin(prep4r['Pressure (Pa)']))
print (np.nanmean(prep4r['Pressure (Pa)']))

print ("Latitude:")
print (np.nanmax(prep4r['Latitude']))
print (np.nanmin(prep4r['Latitude']))
print (np.nanmean(prep4r['Latitude']))

print ("Longitude:")
print (np.nanmax(prep4r['Longitude']))
print (np.nanmin(prep4r['Longitude']))
print (np.nanmean(prep4r['Longitude']))

print ("Elevation + Sensor:")
print (np.nanmax(prep4r['Elevation_SensorHeight (m)']))
print (np.nanmin(prep4r['Elevation_SensorHeight (m)']))
print (np.nanmean(prep4r['Elevation_SensorHeight (m)']))


print ("Elevation:")
print (np.nanmax(prep4r['Elevation (m)']))
print (np.nanmin(prep4r['Elevation (m)']))
print (np.nanmean(prep4r['Elevation (m)']))

print ("Wind Sensor Height:")
print (np.nanmax(prep4r['Wind_Sensor_Height (m)']))
print (np.nanmin(prep4r['Wind_Sensor_Height (m)']))
print (np.nanmean(prep4r['Wind_Sensor_Height (m)']))
print("******************** END ANALYSIS ********************************")


print()
print()
sizedf = len(prep4r)
print ("Number of Observations: ", sizedf)

print()
print()
print()


print (prep4r.iloc[0])
print (len(prep4r))

prep4r = prep4r.replace(np.nan, -888888.0)
prep4r = prep4r.replace("", -888888.0)
prep4r = prep4r.replace(" ", -888888.0)

outvalues = prep4r.drop(['Elevation (m)','Wind_Sensor_Height (m)'],axis=1)



outpath = os.path.abspath('../')
np.savetxt(outpath+"/data_CMLF2011_2016_D2010_2017.txt", outvalues.values, fmt='%10s %20s %13.5f %13.5f %13.5f %13.5f %13.5f %13.5f %20.5f %20.5f %13.5f %40s %20s %40s')    


#%%
prep4r['Wind_Speed (m/s)'] = prep4r['Wind_Speed (m/s)'].mask(prep4r['Wind_Speed (m/s)'] == -888888.0, other = np.nan)
wspd = np.array(prep4r['Wind_Speed (m/s)'])

prep4r['Wind_Direction (deg)'] = prep4r['Wind_Direction (deg)'].mask(prep4r['Wind_Direction (deg)'] == -888888.0, other = np.nan)
wdir = np.array(prep4r['Wind_Direction (deg)'])

sHeight = np.array(prep4r['Wind_Sensor_Height (m)'])

wspd10= np.empty(len(wspd))
wdir10 = np.empty(len(wdir))

def convert_wind_speed10(wspd,sensor_height):
    ## DOESN'T ACCOUNT FOR TURBULENCE - BAD - NEEDS FIXING: INCLUDE THE MONIN-OBUKHOV STABILITY PARAMETER
    height10 = 10.
    alpha = 1./7.
    WSpd10 = wspd * (height10/sensor_height) ** alpha
    return WSpd10



for idx in range(sizedf):
    if not np.isnan(wspd[idx]):
       wspd10[idx] = convert_wind_speed10(wspd[idx],sHeight[idx])
    else:
        wspd10[idx] = np.nan
        
wdir10 = wdir
#def convert_wind_direction10(wdir,sensor_height):
#    height10 = 10.
#    alpha = 1./7.
#    WSpd10 = wspd * (height10/sensor_height) ** alpha
#    return WSpd10



#for idx in range(sizedf):
#    if not np.isnan(wdir[idx]):
#        print(
 

print()
#%%
wspd10deos= np.empty(len(deos_4_r['Wind_Speed (m/s)']))
deos_4_r['Wind_Speed (m/s)'] = deos_4_r['Wind_Speed (m/s)'].mask(deos_4_r['Wind_Speed (m/s)'] == -888888.0, other = np.nan)
wspddeos = np.array(deos_4_r['Wind_Speed (m/s)'])
deosheight =np.array(deos_4_r['Wind_Sensor_Height (m)'])

wspd10dcmlf= np.empty(len(cmlf_4_r['Wind_Speed (m/s)']))
cmlf_4_r['Wind_Speed (m/s)'] = cmlf_4_r['Wind_Speed (m/s)'].mask(cmlf_4_r['Wind_Speed (m/s)'] == -888888.0, other = np.nan)
wspdcmlf = np.array(cmlf_4_r['Wind_Speed (m/s)'])


print()
print()
print()

for idx in range(len(wspd10deos)):
    if not np.isnan(wspddeos[idx]):
        wspd10deos[idx] = convert_wind_speed10(wspddeos[idx],deosheight[idx])
    else:
        wspd10deos[idx] = np.nan
print ("DEOS Wind Speed at 10m (  max/min/mean   ) :")
print (np.nanmax(wspd10deos))
print (np.nanmin(wspd10deos))
print (np.nanmean(wspd10deos))

print()

for idx in range(len(wspd10dcmlf)):
    if not np.isnan(wspdcmlf[idx]):
       wspd10dcmlf[idx] = convert_wind_speed10(wspdcmlf[idx],20)
    else:
        wspd10dcmlf[idx] = np.nan
        
        
print ("CMLF Wind Speed at 10m:")
print (np.nanmax(wspd10dcmlf))
print (np.nanmin(wspd10dcmlf))
print (np.nanmean(wspd10dcmlf))  

print()
################################        
prep4r['Wind_Speed (m/s)']=wspd10

print ("All Wind Speed at 10 meters:")
print (np.nanmax(prep4r['Wind_Speed (m/s)']))
print (np.nanmin(prep4r['Wind_Speed (m/s)']))
print (np.nanmean(prep4r['Wind_Speed (m/s)']))


#%%
prep4r['Wind_Direction (deg)'] = wdir10
prep4r['Wind_Sensor_Height (m)'] = 10.00
prep4r['Elevation_SensorHeight (m)'] = prep4r['Elevation (m)'] +  10.00
prep4r = prep4r.replace(np.nan , -888888.0)
prep4r = prep4r.replace("" , -888888.0)
prep4r = prep4r.replace(" " , -888888.0)


outstring10 = outpath +"/Assimilation_Data_10m_DEOS_CMLF.txt"
prep4r = prep4r.drop(['Elevation (m)','Wind_Sensor_Height (m)'],axis=1)

np.savetxt(outstring10, prep4r.values, fmt='%10s %20s %13.5f %13.5f %13.5f %13.5f %13.5f %13.5f %20.5f %20.5f %13.5f %40s %20s %40s')
