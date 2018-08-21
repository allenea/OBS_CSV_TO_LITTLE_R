#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
##  Last Updated: 3/8/18

@author: ericallen
### Find and Replace NaN values through extrapolation
##  BY: Eric Allen, University of Delaware
#  Clouds Wind and Climate Research Group
#
## This program iterates through all the data and finds if there is good
## data on both sides of that data point that are reliable and that can be
## used to extrapolate the data point. Then extrapolate by taking the
## average between the two points. The first iteration looks at the 3 points
## on each side of the observation with NaN lat/lon value. The second
## iteration looks 3 points on each side. It checks outward to the furthest
## point and if there is a closer pair of observations it uses that
## location. If the observations did not occur within 4 observations of each
## other and within an hour of each other, then there will be no adjustment to lat/lon. 
## It will be left as a NaN value.
#
#
## Possible improvements to this code:
## give it an adjusted average location based on time between the observations and speed? of ferry. 
#
# This is very minimal.
#
## This can be used to investigate where NaN lat/lon appear in the data. It is a
## common trend that the NaN's not smoothed are during day(s) where no
## observations are recored or at night time when the ferry is not running. 


THIS IS TO TRY AND SALVAGE SOME OBSERVATIONS WE ARE VERY CONFIDENT IN THE ACCURACY OF THE FERRY LOCATION AND THE MEASUREMENTS.  IT LIKELY HAS NO IMPACT ON OUR SELECTED CASE STUDIES.
"""

##CHANGE
directory="/home/work/clouds_wind_climate/ferry_data/Prep4R/"

import numpy as np
import csv
import pandas as pd
import glob
import time as t
from dateutil.parser import parse

###
fileTypes = ['MET','EXO']
for fType in fileTypes:
    print fType
    HEADERS = []
    output = []
    for file in glob.glob("All-"+fType+"*.csv"):
        print file
        with open(file,'rU') as infile:
            raw = csv.reader(infile,dialect='excel',delimiter=',')
            count = 0
            for row in raw:
                row2 = row[0:15]
                if count <= 2:
                    HEADERS.append(row2)
                else:
                    row2 = row[0:15]
                    output.append(row2)
                count = count +1;
                


    HEADER = np.array(HEADERS)
    dtf = pd.DataFrame(HEADER,index=None)
    
                    
    outstring = directory+"QualityControlled-"+fType+"-Data.csv"

#%%EXO Iteration

    if (fType == 'EXO'):
                        
        df = pd.DataFrame(output,index=range(len(output)),columns=['Time','Temp','cond','sal','do','do1','turb','chlor','','','','','','LAT','LON'])
        dfsorted = df.sort_values(by='Time', ascending=1)
        
        date_raw=np.array(dfsorted['Time']);

        year_raw    = []; month_raw   = []; day_raw     = []; hour_raw    = []
        min_raw     = []; sec_raw     = []; ParseTime2   = []
        sizeNew2 = int(len(date_raw))
        print "Size of EXO", sizeNew2
        for i in range(sizeNew2):
                d = parse(date_raw[i])
                ParseTime2.append(d)
                year_raw.append(d.year)
                month_raw.append(d.month)
                day_raw.append(d.day)
                hour_raw.append(d.hour)
                min_raw.append(d.minute)
                sec_raw.append(d.second)
        
        Temp_raw=np.array(dfsorted['Temp'],dtype=float);
        cond_raw=np.array(dfsorted['cond'],dtype=float);
        sal_raw=np.array(dfsorted['sal'],dtype=float);
        do_raw=np.array(dfsorted['do'],dtype=float);
        do1_raw=np.array(dfsorted['do1'],dtype=float);
        turb_raw=np.array(dfsorted['turb'],dtype=float);
        chlor_raw=np.array(dfsorted['chlor'],dtype=float);
        lat_raw=np.array(dfsorted['LAT'],dtype=float);
        lon_raw =np.array(dfsorted['LON'],dtype=float);
                       
                           
        for jjk,tmpLat2 in enumerate(lat_raw):
            if(tmpLat2=='nan'):
                lat_raw[jjk]=np.nan
            if(tmpLat2<38.5):
                lat_raw[jjk]=np.nan

        for iij,tmpLon2 in enumerate(lon_raw):
            if(tmpLon2=='nan'):
                lon_raw[iij]=np.nan 
            if(tmpLon2 > 75.6):
                lon_raw[iij]=np.nan 
                       
        ### EXO DATA ITERATION
        ## check for NaN values in lat
        exoNaNLat = np.isnan(lat_raw)
        exosumNaNLat = np.sum(np.isnan(lat_raw))
        exoWhereNaNLat = np.where(np.isnan(lat_raw))
        
        # check for NaN values in lon
        exoNanLon = np.isnan(lon_raw)
        exosumNaNLon = np.sum(np.isnan(lon_raw))
        exoWhereNaNLon = np.where(np.isnan(lon_raw))
        
        print "Start of Exo loop one"
        print exosumNaNLat, exosumNaNLon

        ## FIRST EXO ITERATION
        # Iterate checking 4 to each side
        for ii in range(4,len(exoNaNLat)-4):
            if (exoNaNLat[ii] == 1):
                for i in range(1,4):
                    for j in range(1,4):
                        if (exoNaNLat[ii-i] == 0):
                            temp1 = lat_raw[ii-i];
                            temp5 = lon_raw[ii-i];
                            if (exoNaNLat[ii+j]==0):
                                #absolute value of the diff between the obs <1.
                                absDayCheck = abs(day_raw[ii+j]-day_raw[ii-i]);
                                absHourCheck = abs(hour_raw[ii+j]-hour_raw[ii-i]);
                                # Extrapolate
                                if (day_raw[ii+j]== day_raw[ii-i] and (absHourCheck <= 1 or absHourCheck == 23)):
                                    temp2 = lat_raw[ii+j];
                                    temp6 = lon_raw[ii+j];
                                    temp3 = (temp1 + temp2)/2;
                                    temp7 = (temp5 + temp6)/2;
                                    lat_raw[ii] = temp3;
                                    lon_raw[ii] = temp7;
                                    exoNaNLat[ii] = 0;

                                # Extrapolate between 23:00 hrs and 00:00 hrs
                                elif (absDayCheck <= 1 and absHourCheck == 23):
                                    temp2 = lat_raw[ii+j];
                                    temp6 = lon_raw[ii+j];
                                    temp3 = (temp1 + temp2)/2;
                                    temp7 = (temp5 + temp6)/2;
                                    lat_raw[ii] = temp3;
                                    lon_raw[ii] = temp7;
                                    exoNaNLat[ii] = 0;
        
        
        ## Check for NaN in data after first iterationb
        lat_raw2nd = lat_raw;
        lon_raw2nd = lon_raw;
        exoNaNLat2 = np.isnan(lat_raw2nd);
        exosumMissLat2 = np.sum(np.isnan(lat_raw2nd));
        exoNaNLon2 = np.isnan(lon_raw2nd);
        exosumMissLon2 = np.sum(np.isnan(lon_raw2nd));
        exoWhereNaN2Lat = np.where(np.isnan(lat_raw2nd))
        exoWhereNaN2Lon = np.where(np.isnan(lon_raw2nd))
        
        print "End of Exo loop one"
        print exosumMissLat2, exosumMissLon2
        
        ### Second EXO Iteration
        for ii in range(4,len(exoNaNLat2)-4):
            if (exoNaNLat2[ii] == 1):
                for i in range(1,4):
                    for j in range(1,4):
                        if (exoNaNLat2[ii-i] == 0):
                            temp1 = lat_raw2nd[ii-i];
                            temp5 = lon_raw2nd[ii-i];
                            if (exoNaNLat2[ii+j]==0):
                                absHourCheck = abs(hour_raw[ii+j]-hour_raw[ii-i]);
                                absDayCheck = abs(day_raw[ii+j]-day_raw[ii-i]);
                                #Extrapolate
                                if (day_raw[ii+j]== day_raw[ii-i] and (absHourCheck <= 1 or absHourCheck == 23)):
                                    temp2 = lat_raw2nd[ii+j];
                                    temp6 = lon_raw2nd[ii+j];
                                    temp3 = (temp1 +temp2)/2;
                                    temp7 = (temp5 + temp6)/2;
                                    lat_raw2nd[ii] = temp3;
                                    lon_raw2nd[ii] = temp7;
                                    exoNaNLat2[ii] = 0;

                                ## Extrapolate between 23:00 hrs and 00:00 hrs
                                elif (absDayCheck <= 1 and absHourCheck == 23):
                                    temp2 = lat_raw2nd[ii+j];
                                    temp6 = lon_raw2nd[ii+j];
                                    temp3 = (temp1 +temp2)/2;
                                    temp7 = (temp5 + temp6)/2;
                                    lat_raw2nd[ii] = temp3;
                                    lon_raw2nd[ii] = temp7;
                                    exoNaNLat2[ii] = 0;

        
        ### FINAL CHECK
        lat_raw3 = lat_raw2nd;
        lon_raw3 = lon_raw2nd;
        
        exoNaNLat3 = np.isnan(lat_raw3)
        exosumLat3 = np.sum(np.isnan(lat_raw3))
        exoNaNLon3 = np.isnan(lon_raw3)
        exosumLon3 = np.sum(np.isnan(lon_raw3))
        print "End of Exo"
        print exosumLat3, exosumLon3
        
        exoTime0 = np.where(hour_raw == 0 and lat_raw3 == np.nan)
        exoTime1 = np.where(hour_raw == 1 and lat_raw3 == np.nan)
        exoTime22 = np.where(hour_raw == 23 and lat_raw3 == np.nan)
        exoTime2 = np.where(hour_raw == 2 and lat_raw3 == np.nan)
        exoTime23 = np.where(hour_raw == 22 and lat_raw3 == np.nan)      

        HEADING2  = ["YEAR","MONTH","DAY","HOUR","MINUTE","SECOND",
                    "TEMPERATURE","CONDUCTIVITY","SALINITY","DISOLVED_OXYGEN",
                    "DISOLVED_OXYGEN_2","TURBIDITY","CHLOROPHYLL","LATITUDE","LONGITUDE"]
        
                         
        DATAF = np.zeros((len(Temp_raw),len(HEADING2)))
        DATAF[:,0] = year_raw
        DATAF[:,1] = month_raw
        DATAF[:,2] = day_raw
        DATAF[:,3] = hour_raw
        DATAF[:,4] = min_raw
        DATAF[:,5] = sec_raw
        DATAF[:,6] = Temp_raw
        DATAF[:,7] = cond_raw
        DATAF[:,8] = sal_raw
        DATAF[:,9] = do_raw 
        DATAF[:,10] = do1_raw 
        DATAF[:,11] = turb_raw 
        DATAF[:,12] = chlor_raw 
        DATAF[:,13] = lat_raw3 
        DATAF[:,14] = lon_raw3   
                 
        dfwrite = pd.DataFrame(DATAF, columns = HEADING2)
        dfwrite.to_csv(outstring)

        del DATAF, df, HEADING2


   
    elif (fType=='MET'):
                
        df = pd.DataFrame(output,index=range(len(output)),columns=['Time','Wind_Speed','Wind_Direction','AirTemp','RH','BarPress','CompHDG','wDR2HDG','','','','','','LAT','LON'])
        dfsorted = df.sort_values(by='Time', ascending=1)

        date_raw1=np.array(dfsorted['Time']);
        #print date_raw1[295584:295926]
        year_raw1   = []; month_raw1  = []; day_raw1    = []; hour_raw1   = []
        min_raw1    = []; sec_raw1    = []; ParseTime   = []
        sizeNew = int(len(date_raw1))
        print "Size of MET", sizeNew

        for i in range(sizeNew):
                d = parse(date_raw1[i])
                ParseTime.append(d)
                year_raw1.append(d.year)
                month_raw1.append(d.month)
                day_raw1.append(d.day)
                hour_raw1.append(d.hour)
                min_raw1.append(d.minute)
                sec_raw1.append(d.second)

        
        wSpd_raw=np.array(dfsorted['Wind_Speed'],dtype=float);
        wDir_raw=np.array(dfsorted['Wind_Direction'],dtype=float);
        AirTemp_raw=np.array(dfsorted['AirTemp'],dtype=float);
        RH_raw=np.array(dfsorted['RH'],dtype=float);
        BarPress_raw=np.array(dfsorted['BarPress'],dtype=float);                       
        CompHDG_raw=np.array(dfsorted['CompHDG'],dtype=float);
        wDR2HDG_raw=np.array(dfsorted['wDR2HDG'],dtype=float);         
        lat_raw1=np.array(dfsorted['LAT'],dtype=float);
        lon_raw1=np.array(dfsorted['LON'],dtype=float);

        for jkl,tmpLat in enumerate(lat_raw1):
            if(tmpLat=='nan'):
                lat_raw1[jkl]=np.nan
            if(tmpLat<38.5):
                lat_raw1[jkl]=np.nan

        for lkj,tmpLon in enumerate(lon_raw1):
            if(tmpLon=='nan'):
                lon_raw1[lkj]=np.nan 
            if(tmpLon > 75.6):
                lon_raw1[lkj]=np.nan              
                        

        metNaNLat1 = np.isnan(lat_raw1)
        metsumLat1 = np.sum(np.isnan(lat_raw1))
        metWhereNaNLat = np.where(np.isnan(lat_raw1))
        
        metNaNLon1 = np.isnan(lon_raw1)
        metsumLon1 = np.sum(np.isnan(lon_raw1))
        metWhereNaNLon = np.where(np.isnan(lon_raw1))
        
                
        print "Starting Met Loop One"
        print metsumLat1,metsumLon1
        
                              
        ## FIRST MET ITERATION
        for ii in range(4,len(metNaNLat1)-4):
            if (metNaNLat1[ii] == 1):
                for i in range(1,4):
                    for j in range(1,4):
                        if (metNaNLat1[ii-i] == 0):
                            temp1 = lat_raw1[ii-i];
                            temp5 = lon_raw1[ii-i];
                            if (metNaNLat1[ii+j]==0):
                                #absolute value of 2 hours less than 1.
                                absDayCheck1 = abs(day_raw1[ii+j]-day_raw1[ii-i]);
                                absHourCheck1 = abs(hour_raw1[ii+j]-hour_raw1[ii-i]);
                                # Extrapolate
                                if (day_raw1[ii+j]== day_raw1[ii-i] and (absHourCheck1 <= 1 or absHourCheck1 == 23)):
                                    temp2 = lat_raw1[ii+j];
                                    temp6 = lon_raw1[ii+j];
                                    temp3 = (temp1 +temp2)/2;
                                    temp7 = (temp5 + temp6)/2;
                                    lat_raw1[ii] = temp3;
                                    lon_raw1[ii] = temp7;
                                    metNaNLat1[ii] = 0;

                                # Extrapolate, if the values are between 23:00 hrs and 01:00hrs
                                elif (absDayCheck1 <= 1 and absHourCheck1 == 23):
                                    temp2 = lat_raw1[ii+j];
                                    temp6 = lon_raw1[ii+j];
                                    temp3 = (temp1 +temp2)/2;
                                    temp7 = (temp5 + temp6)/2;
                                    lat_raw1[ii] = temp3;
                                    lon_raw1[ii] = temp7;
                                    metNaNLat1[ii] = 0;

        
        ## Check data after first met iteration
        lat1_raw2nd = lat_raw1;
        lon1_raw2nd = lon_raw1;
        metNaNLat2nd = np.isnan(lat1_raw2nd)
        metsumMissLat2nd = np.sum(np.isnan(lat1_raw2nd))
        metNaNLon2nd = np.isnan(lon1_raw2nd);
        metsumMissLon2nd = np.sum(np.isnan(lon1_raw2nd));
        metWhereNaNLat2 = np.where(np.isnan(lat1_raw2nd))
        metWhereNaNLon2 = np.where(np.isnan(lon1_raw2nd))
        
        print "DONE Met Loop 1"
        print metsumMissLat2nd,metsumMissLon2nd
        
                
        ## SECOND MET ITERATION
        for ii in range(4,len(metNaNLat2nd)-4):
            if (metNaNLat2nd[ii] == 1):
                for i in range(1,4):
                    for j in range(1,4):
                        if (metNaNLat2nd[ii-i] == 0):
                            temp1 = lat1_raw2nd[ii-i];
                            temp5 = lon1_raw2nd[ii-i];
                            if (metNaNLat2nd[ii+j]==0):
                                absHourCheck1 = abs(hour_raw1[ii+j]-hour_raw1[ii-i]);
                                absDayCheck1 = abs(day_raw1[ii+j]-day_raw1[ii-i]);
                                #Extrapolate
                                if (day_raw1[ii+j]== day_raw1[ii-i] and (absHourCheck1 <= 1 or absHourCheck1 == 23)):
                                    temp2 = lat1_raw2nd[ii+j];
                                    temp6 = lon1_raw2nd[ii+j];
                                    temp3 = (temp1 +temp2)/2;
                                    temp7 = (temp5 + temp6)/2;
                                    lat1_raw2nd[ii] = temp3;
                                    lon1_raw2nd[ii] = temp7;
                                    metNaNLat2nd[ii] = 0;

                                # Extrapolate, if the values are between 23:00 hrs and 01:00hrs
                                elif (absDayCheck1 <= 1 and absHourCheck1 == 23):
                                    temp2 = lat1_raw2nd[ii+j];
                                    temp6 = lon1_raw2nd[ii+j];
                                    temp3 = (temp1 +temp2)/2;
                                    temp7 = (temp5 + temp6)/2;
                                    lat1_raw2nd[ii] = temp3;
                                    lon1_raw2nd[ii] = temp7;
                                    metNaNLat2nd[ii] = 0;

        
        ## FINAL CHECK
        lat1_raw3 = lat1_raw2nd;
        lon1_raw3 = lon1_raw2nd;
        
        metNaNLatFinal = np.isnan(lat1_raw3)
        metsumMissFinalLat = np.sum(np.isnan(lat1_raw3))
        metNaNLonFinal = np.isnan(lon1_raw3)
        metsumMissFinalLon = np.sum(np.isnan(lon1_raw3))

        
        metTime0 = np.where(hour_raw1 == 0 and lat1_raw3 == np.nan)
        metTime1 = np.where(hour_raw1 == 1 and lat1_raw3 == np.nan)
        metTime23 = np.where(hour_raw1 == 23 and lat1_raw3 == np.nan)
        metTime2 = np.where(hour_raw1 == 2 and lat1_raw3 == np.nan)
        metTime22 = np.where(hour_raw1 == 22 and lat1_raw3 == np.nan)
        
        print "DONE WITH MET"
        print metsumMissFinalLat,metsumMissFinalLon
        
        HEADING  = ["YEAR","MONTH","DAY","HOUR","MINUTE","SECOND",
                    "WIND_SPEED","WIND_DIRECTION","AIR_TEMPERATURE","RELATIVE_HUMIDITY",
                    "PRESSURE","COMPHDG","WDIR2HDG","LATITUDE","LONGITUDE"]
        
                         
        DATAF = np.zeros((len(wSpd_raw),len(HEADING)))
        DATAF[:,0] = year_raw1
        DATAF[:,1] = month_raw1
        DATAF[:,2] = day_raw1
        DATAF[:,3] = hour_raw1
        DATAF[:,4] = min_raw1
        DATAF[:,5] = sec_raw1
        DATAF[:,6] = wSpd_raw
        DATAF[:,7] = wDir_raw
        DATAF[:,8] = AirTemp_raw
        DATAF[:,9] = RH_raw 
        DATAF[:,10] = BarPress_raw 
        DATAF[:,11] = CompHDG_raw 
        DATAF[:,12] = wDR2HDG_raw 
        DATAF[:,13] = lat1_raw3 
        DATAF[:,14] = lon1_raw3   
                 
        dfwrite = pd.DataFrame(DATAF, columns = HEADING)
        dfwrite.to_csv(outstring)

        del DATAF, df, HEADING

