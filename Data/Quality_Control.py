"""
Created on Wed Nov 28 12:33:33 2018

@author: allenea

QUALITY CONTROL

- Adding 273.15 (doing math) on missing values changing their -8888888.0
        flag to be adjusted by the math.
- Buoy data still at -999/-99/-9999
"""
#IMPORTS
import os
#import sys
import math
import numpy as np
import pandas as pd


HEADER = ["ID_String", 'DATE', 'Wind_Speed (m/s)', 'Wind_Direction (deg)',\
          'Air_Temperature (K)', 'Dewpoint_Temperature (K)', 'Relative_Humidity (%)',\
          'Pressure (Pa)',\
          'Latitude', 'Longitude', 'Elevation_SensorHeight (m)',\
          'Name_string', 'FM_string', 'Source_string',\
          'Elevation (m)', 'Wind_Sensor_Height (m)']

data = os.getcwd()+"/All_Delaware_Data.csv"

out10csvname = "/delaware_thesis_QC_10m_OBS.csv"
outcsvname = "/delaware_thesis_QC_OBS.csv"

float64 = np.float64
dtypesDict = {"ID_String":object, "DATE":float64, "Wind_Speed (m/s)":float64,\
              "Wind_Direction (deg)":float64, "Air_Temperature (K)": float64,\
              "Dewpoint_Temperature (K)":float64, "Relative_Humidity (%)":float64,\
              "Pressure (Pa)":float64, "Latitude":float64, "Longitude":float64,\
              "Elevation_SensorHeight (m)":float64, "Name_string": object,\
              "FM_string" : object, "Source_string":object, "Elevation (m)":float64,\
              "Wind_Sensor_Height (m)":float64}
df = pd.read_csv(data, usecols=HEADER, dtype=dtypesDict)
#%%
df = df.mask(df == -888888.0, other=np.nan)
df = df.mask(df == 999.0, other=np.nan)
df = df.mask(df == 99.0, other=np.nan)
df = df.mask(df == 9999.0, other=np.nan)
df = df.mask(df == -999.0, other=np.nan)
df = df.mask(df == -99.0, other=np.nan)
df = df.mask(df == -9999.0, other=np.nan)
df = df.mask(df == ' ', other=np.nan)
df = df.mask(df == '', other=np.nan)

########## THESE CAN HAVE 0 VALUES ##################
elevation = np.array(df['Elevation (m)'])
wind_direction = np.array(df['Wind_Direction (deg)'])
# MASK THE 0's and put the 2 data back in the dataframe
df = df.mask(df == 0, other=np.nan)
df['Elevation (m)'] = elevation
df['Wind_Direction (deg)'] = wind_direction
####################################################

print("***************** Max/Min/Mean ANALYSIS OF THE DATA **************")

print("Date:")
print(np.nanmax(df["DATE"]))
print(np.nanmin(df["DATE"]))
print(np.nanmean(df['DATE']))


print("Wind Speed:")
print(np.nanmax(df['Wind_Speed (m/s)']))
print(np.nanmin(df['Wind_Speed (m/s)']))
print(np.nanmean(df['Wind_Speed (m/s)']))

print("Wind Direction:")
print(np.nanmax(df['Wind_Direction (deg)']))
print(np.nanmin(df['Wind_Direction (deg)']))
print(np.nanmean(df['Wind_Direction (deg)']))

print("Air Temperature:")
print(np.nanmax(df['Air_Temperature (K)']))
print(np.nanmin(df['Air_Temperature (K)']))
print(np.nanmean(df['Air_Temperature (K)']))

print("Dewpoint Temperature:")
print(np.nanmax(df['Dewpoint_Temperature (K)']))
print(np.nanmin(df['Dewpoint_Temperature (K)']))
print(np.nanmean(df['Dewpoint_Temperature (K)']))

print("Relative Humidity:")
print(np.nanmax(df['Relative_Humidity (%)']))
print(np.nanmin(df['Relative_Humidity (%)']))
print(np.nanmean(df['Relative_Humidity (%)']))


print("Pressure:")
print(np.nanmax(df['Pressure (Pa)']))
print(np.nanmin(df['Pressure (Pa)']))
print(np.nanmean(df['Pressure (Pa)']))

print("Latitude:")
print(np.nanmax(df['Latitude']))
print(np.nanmin(df['Latitude']))
print(np.nanmean(df['Latitude']))

print("Longitude:")
print(np.nanmax(df['Longitude']))
print(np.nanmin(df['Longitude']))
print(np.nanmean(df['Longitude']))

print("Elevation + Sensor:")
print(np.nanmax(df['Elevation_SensorHeight (m)']))
print(np.nanmin(df['Elevation_SensorHeight (m)']))
print(np.nanmean(df['Elevation_SensorHeight (m)']))


print("Elevation:")
print(np.nanmax(df['Elevation (m)']))
print(np.nanmin(df['Elevation (m)']))
print(np.nanmean(df['Elevation (m)']))

print("Wind Sensor Height:")
print(np.nanmax(df['Wind_Sensor_Height (m)']))
print(np.nanmin(df['Wind_Sensor_Height (m)']))
print(np.nanmean(df['Wind_Sensor_Height (m)']))
print("******************** END ANALYSIS ********************************")

#sys.exit(0)

print("Using OBSGRID's Gross Error Check Standards")
df['Wind_Direction (deg)'] = df['Wind_Direction (deg)'].mask(df['Wind_Direction (deg)'] > 360,\
  other=np.nan)
df['Wind_Direction (deg)'] = df['Wind_Direction (deg)'].mask(df['Wind_Direction (deg)'] < 0,\
  other=np.nan)
df['Wind_Speed (m/s)'] = df['Wind_Speed (m/s)'].mask(df['Wind_Speed (m/s)'] <= 0, other=np.nan)
df['Wind_Speed (m/s)'] = df['Wind_Speed (m/s)'].mask(df['Wind_Speed (m/s)'] > 60, other=np.nan)

df['Air_Temperature (K)'] = df['Air_Temperature (K)'].mask(df['Air_Temperature (K)'] < 225,\
  other=np.nan)
df['Air_Temperature (K)'] = df['Air_Temperature (K)'].mask(df['Air_Temperature (K)'] > 323,\
  other=np.nan)
df['Dewpoint_Temperature (K)'] = df['Dewpoint_Temperature (K)'].mask(df['Dewpoint_Temperature (K)']\
  < 225, other=np.nan)
df['Dewpoint_Temperature (K)'] = df['Dewpoint_Temperature (K)'].mask(df['Dewpoint_Temperature (K)']\
  > 323, other=np.nan)

df['Relative_Humidity (%)'] = df['Relative_Humidity (%)'].mask(df['Relative_Humidity (%)'] <= 1,\
  other=np.nan)
df['Relative_Humidity (%)'] = df['Relative_Humidity (%)'].mask(df['Relative_Humidity (%)'] > 105,\
  other=np.nan)

df['Pressure (Pa)'] = df['Pressure (Pa)'].mask(df['Pressure (Pa)'] < 80000.0, other=np.nan)
df['Pressure (Pa)'] = df['Pressure (Pa)'].mask(df['Pressure (Pa)'] > 107840.0, other=np.nan)

print()
print()

print("***************** Max/Min/Mean ANALYSIS OF THE QC'd DATA **************")

print("Date:")
print(np.nanmax(df["DATE"]))
print(np.nanmin(df["DATE"]))
print(np.nanmean(df['DATE']))


print("Wind Speed:")
print(np.nanmax(df['Wind_Speed (m/s)']))
print(np.nanmin(df['Wind_Speed (m/s)']))
print(np.nanmean(df['Wind_Speed (m/s)']))

print("Wind Direction:")
print(np.nanmax(df['Wind_Direction (deg)']))
print(np.nanmin(df['Wind_Direction (deg)']))
print(np.nanmean(df['Wind_Direction (deg)']))

print("Air Temperature:")
print(np.nanmax(df['Air_Temperature (K)']))
print(np.nanmin(df['Air_Temperature (K)']))
print(np.nanmean(df['Air_Temperature (K)']))

print("Dewpoint Temperature:")
print(np.nanmax(df['Dewpoint_Temperature (K)']))
print(np.nanmin(df['Dewpoint_Temperature (K)']))
print(np.nanmean(df['Dewpoint_Temperature (K)']))

print("Relative Humidity:")
print(np.nanmax(df['Relative_Humidity (%)']))
print(np.nanmin(df['Relative_Humidity (%)']))
print(np.nanmean(df['Relative_Humidity (%)']))


print("Pressure:")
print(np.nanmax(df['Pressure (Pa)']))
print(np.nanmin(df['Pressure (Pa)']))
print(np.nanmean(df['Pressure (Pa)']))

print("Latitude:")
print(np.nanmax(df['Latitude']))
print(np.nanmin(df['Latitude']))
print(np.nanmean(df['Latitude']))

print("Longitude:")
print(np.nanmax(df['Longitude']))
print(np.nanmin(df['Longitude']))
print(np.nanmean(df['Longitude']))

print("Elevation + Sensor:")
print(np.nanmax(df['Elevation_SensorHeight (m)']))
print(np.nanmin(df['Elevation_SensorHeight (m)']))
print(np.nanmean(df['Elevation_SensorHeight (m)']))


print("Elevation:")
print(np.nanmax(df['Elevation (m)']))
print(np.nanmin(df['Elevation (m)']))
print(np.nanmean(df['Elevation (m)']))

print("Wind Sensor Height:")
print(np.nanmax(df['Wind_Sensor_Height (m)']))
print(np.nanmin(df['Wind_Sensor_Height (m)']))
print(np.nanmean(df['Wind_Sensor_Height (m)']))
print("******************** END ANALYSIS ********************************")
print()
print()

sizedf = len(df)
print("Number of Observations: ", sizedf)

print()
print()
print(list(set(df["ID_String"])))
print()
print()

outdir = os.path.abspath('../')
outstring = outdir + outcsvname
outdf = df
outdf = outdf.replace(np.nan, -888888.0)
outdf = outdf.replace("", -888888.0)
df.to_csv(outstring, index=False, header=HEADER)



wspd = np.array(df['Wind_Speed (m/s)'])
wdir = np.array(df['Wind_Direction (deg)'])
sHeight = np.array(df['Wind_Sensor_Height (m)'])
wspd10 = np.empty(len(wspd))
wdir10 = np.empty(len(wdir))
#%% ADJUST MEASUREMENT TO A STANDARDIZED HEIGHT

def convert_wind_speed10(wspd_var, sensor_height):
    """
    height10 = 10.
    alpha = 1./7.
    WSpd10 = wspd * (height10/sensor_height) ** alpha
    return WSpd10

    https://rmets.onlinelibrary.wiley.com/doi/pdf/10.1017/S1350482799000961
    https://en.wikipedia.org/wiki/Log_wind_profile#cite_note-Holmes2015-2
    z0 = https://en.wikipedia.org/wiki/Roughness_length
    """
    height10 = 10
    d = 0
    z0 = 0.10
    return wspd_var * math.log((height10 - d) / z0) / math.log((sensor_height - d) / z0)

for idx in range(sizedf):
    if not np.isnan(wspd[idx]):
        wspd10[idx] = convert_wind_speed10(wspd[idx], sHeight[idx])
    else:
        wspd10[idx] = np.nan

wdir10 = wdir
#def convert_wind_direction10(wdir,sensor_height):
#    height10 = 10.
#    alpha = 1./7.
#    WSpd10 = wspd * (height10/sensor_height) ** alpha
#    return WSpd10

# DO NOT HAVE TEMPERATURE SENSOR HEIGHT AT THIS TIME
#def convert_temperature_2m(temp,sensor_height):
#    height2= 2.
#    alpha = 1./7.
#### NOT THE ACTUAL EQUATION USE T(Z) eq
#    Temp2 = temp * (height2/sensor_height) ** alpha
#    return Temp2

#for idx in range(sizedf):
#    if not np.isnan(wdir[idx]):
#        print()
###############################
print("Wind Speed Regular:")
print(np.nanmax(df['Wind_Speed (m/s)']))
print(np.nanmin(df['Wind_Speed (m/s)']))
print(np.nanmean(df['Wind_Speed (m/s)']))
print()
print("Wind Speed 10m:")
print(np.nanmax(wspd10))
print(np.nanmin(wspd10))
print(np.nanmean(wspd10))
###############################
df['Wind_Speed (m/s)'] = wspd10
df['Wind_Direction (deg)'] = wdir10
df['Wind_Sensor_Height (m)'] = 10.00
df['Elevation_SensorHeight (m)'] = df['Elevation (m)'] +  10.00
df = df.replace(np.nan, -888888.0)
df = df.replace("", -888888.0)
df = df.replace(" ", -888888.0)

NEWHEADER = ["ID_String", 'DATE', 'Wind_Speed10 (m/s)', 'Wind_Direction10 (deg)',\
          'Air_Temperature (K)', 'Dewpoint_Temperature (K)', 'Relative_Humidity (%)',\
          'Pressure (Pa)',\
          'Latitude', 'Longitude', 'Elevation_10mSensorHeight (m)',\
          'Name_string', 'FM_string', 'Source_string',\
          'Elevation (m)', 'Wind_Sensor_Height (10m)']

outstring10 = outdir + out10csvname
df.to_csv(outstring10, index=False, header=NEWHEADER)
