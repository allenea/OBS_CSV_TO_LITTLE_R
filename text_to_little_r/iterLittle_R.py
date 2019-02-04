#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Updated on Tues Mar 27 6:30pm 2018

@author: Eric Allen
allenea@udel.edu
Clouds_Wind_Climate Workgroup, University of Delaware

Dewpoint Temperature and Geopotential Height data was not collected for this study and not processed for assimilation
DEOS and Cape May Lewes Ferry is being reformatted into Little_R format required for OBSGRID. Another file should be made for CMLF only.
Open/Read the DEOS + CMLF data from the text file created in prep4r. Reverse the list so the newest stuff is at the top and work backwards.
Initialize constants and unknown variables (Td and Z)
Read in all of the met_em files from the scratch directory and store as a list... reverse that list to work from Present->Past
Identify the interval between the two files. Determine what the time range should be for each file. This value is preset.

*** Go through each met_em file in the list. Parse it (Year, Month, Day Hour, Min).. Create a datestring... starting check point
Then based on the interval already identified. Create the end point that the observations should fall between. Calculate that.
	- Again remember you are working backwards. Check to make sure hours, days, months do not change. If they do address that.
reformat the endCheckPoint string that will be used for bound comparison. 
Setup and open the output file for each timestep that the data will be stored.
Iterate through the data (remember it's backwards). If it is not the right year,month, and day in the right month it moves to the next observations.
Once it found the observations from that day. Parse the string. Check if it falls within the start and end time-range-interval. 
	-  If it does then save it in the little r format with the header, data, end record, tail to the text file.
	-  If it does not fall within the range and is below the end record break the loop. Open a new met_em file and continue from the ***.

Then once it is through the last file the program ends.


Please log output file so you can go back and identify possible errors until further testing has been completed. Try all possible situtaions. Beggining of the month, end of the month end of the year 12/31 or 1/1/ diffferent hours of the day. Leap years leap days, etc.

-----------
Concerns and Future Thoughts on the research:

One concern is that the one observation after is getting tossed but I don't think that is the end of the world. Only place obs might be getting lost in the this.
Bigger concern would be the endCheck and making sure that it moves month-month, day-to-day, hour-hour, and down to the minute... I think I have coded it to do that but there could be an occassion where it messes up because of how I coded. There was nothing wrong in my intial case study...

For this research project.. I need to identify which time step proves to have the best results, and the computing time/cost required for the different intervals.

-------
TODO After this file

#### Subtract intial run from new run (USING DEOS DATA ONLY... ADD A CONDITION or an alternate file that is run)
#### Depending on if the user wants CMLF data or both DEOS and CMLF, run a specific file.. also one for no new data.. This should be done in the WRF directory

### ... Make sure that the result is the same.

### Less than an hour (50 mins?) to take 12M raw obs and prep4r
### Downloading input forcing (Can I automate??? How long?)
### 5 minute WPS takes about 20-25MINS

LITTLE_R OBS
### 3-hour = <45 seconds (41 sec)
### 5-minute = 10-20 Minutes (13:10 (not all), 12:30, 12:35 (farber))
### 1-hr??????

OBSGRID


RUNNING WRF


Is there a way to adjust all namelist files and things in real time simulation or based on the run....
"""

#IMPORTS
import glob
from datetime import datetime, date, time, timedelta
import time as t
import os

start_time = t.time()

#OPEN/READ DATA FILE - GET FARBER LOCATION
curdir = os.getcwd()
data_file = curdir+'/data_CMLF2011_2016_D2013_2017.txt'
#data_file = os.path.abspath('../Verification_Data')+"/all_verification_OBSdata_BADARC.txt"
outdir = os.path.abspath('../scratch-dir')

infile = open(data_file,'r')
readData = infile.readlines()
readData.reverse()
    
# INITIALIZE CONSTANT VARIABLES. MISSING OR DON'T CHANGE THROUGHOUT
isSounding = 'F';is_bogus = 'F';discard = 'F' # False- Booleans
seq_num = len(readData)
print(seq_num)

# IDENTIFY FIRST INSTANCE OF THE MET_EM FILE... AKA THE START TIME/ End Time. Reverse them. work back to front
#for file in glob.glob(...path..../WRF/OBSGRID/met_em.d01.*.nc"):
directory= outdir+'/met_em.d01.'
length = len(directory)
allfiles = glob.glob(directory+"*.nc")

allfiles.sort()
allfiles.reverse()
print (allfiles)

IntervalTime = datetime.strptime(allfiles[0][length:length+19],"%Y-%m-%d_%H:%M:%S") - datetime.strptime(allfiles[1][length:length+19],"%Y-%m-%d_%H:%M:%S")
IntervalTime = IntervalTime.total_seconds()

if int(IntervalTime//60) < 60:  ##Interval = int(IntervalTime//60) ## Minutes
    deltaInterval = int(IntervalTime//60)
    subTime = 4
    print (deltaInterval, "-MINUTE DATA")
elif int(IntervalTime//(60*60)) < 24:  ##Interval = int(IntervalTime//(60*60)) ## Hours
    deltaInterval = int(IntervalTime//(60*60))
    print (deltaInterval, "-HOURLY DATA")
    if deltaInterval == 1:
        subTime = 20
    elif deltaInterval == 3:
        subTime = 30
    else:
        subTime = 55
else:
    print ("This data is at a greater interval than daily")
    

#%% Go through the files in order and pull the times (splice)
for file in allfiles:
    countTotal = 0
    timestring = file[length:length+19]###file[68:87]
    print (file[length:length+19])   # FOR FARBER

    #timestring = file[38:57]   # FOR ERIC'S PERSONAL CPU
    #print file[38:57]
    
    year = timestring[0:4]
    
    month = timestring[5:7]
    intMonth = int(month)
    
    day = timestring[8:10] 
    intDay = int(day)
    
    hour = timestring[11:13]
    intHour = int(hour)

    minute = timestring[14:16]
    intMinute = int(minute)
    ## for each file iterate hour, hour +1 , hour +2 and create output filess
        
    print ("Year:",year, ". Month:",month,". Day:",day,". Hour:",hour,".Minute:", minute)

    # TIME STEP-WHAT DO I WANT TO USE?
    checkTime = year+month+day+hour + minute +'00'
    
    
    # Create End CheckTime String -> int for comparison
    if (intMinute == 0 and subTime <=60):
        lessMinute = 60-subTime
        if (intHour == 0):
            lessDay = intDay - 1
            lessHour = 23
            if (lessDay == 0):
                # NOV (12 -1 = 11)  Sept 10-1 = 9 June 7-1 = 6  April 5-1 =4 
                if ((intMonth - 1) == 11 or (intMonth - 1) == 9 or (intMonth - 1) == 6 or (intMonth - 1) == 4):
                    lessDay = 30
                    lessMonth = intMonth-1
                # December 1-1 - 0  January 2 -1 =1  March 4-1 =3  May = 6-1 = 5 July 8-1 = 7 August 9 -1 =8  OCT 11 -1 = 10
                elif ((intMonth - 1) == 0 or (intMonth - 1) == 1 or (intMonth - 1) == 3 or (intMonth - 1) == 5 or (intMonth - 1) == 7 or (intMonth - 1) == 8 or (intMonth - 1) == 10):
                    lessDay = 31
                    lessMonth  = intMonth - 1
                    if ((intMonth -1) == 0):
                        lessMonth = 12
                        year = int(year) -1
                elif ((intMonth-1)==2):
                    lessMonth = 2
                    if (int(year) % 4) == 0:
                        if (int(year) % 100) == 0:
                            if (int(year) % 400) == 0:
                                lessDay = 29
                            else: 
                                lessDay = 28
                        else:
                            lessDay = 29
                    else:
                        lessDay = 28
                else:
                    print ("BIG ERROR- No Month Connected")
            else:
                lessMonth = intMonth
                
        else:
            lessHour = intHour - 1
            lessDay = intDay
            lessMonth = intMonth            
    # Example 15 - 30 = -15 so 60 -15 = 45 and hour goes from say 22Z - 21Z        
    elif ((intMinute - subTime) < 0 and subTime <= 60):
        lessMinute = 60 - (intMinute - subTime)
        if (intHour == 0):
            lessDay = intDay - 1
            lessHour = 23
            if (lessDay == 0):
                # NOV (12 -1 = 11)  Sept 10-1 = 9 June 7-1 = 6  April 5-1 =4 
                if ((intMonth - 1) == 11 or (intMonth - 1) == 9 or (intMonth - 1) == 6 or (intMonth - 1) == 4):
                    lessDay = 30
                    lessMonth = intMonth-1
                # December 1-1 - 0  January 2 -1 =1  March 4-1 =3  May = 6-1 = 5 July 8-1 = 7 August 9 -1 =8  OCT 11 -1 = 10
                elif ((intMonth - 1) == 0 or (intMonth - 1) == 1 or (intMonth - 1) == 3 or (intMonth - 1) == 5 or (intMonth - 1) == 7 or (intMonth - 1) == 8 or (intMonth - 1) == 10):
                    lessDay = 31
                    lessMonth  = intMonth - 1
                    if ((intMonth -1) == 0):
                        lessMonth = 12
                        year = int(year) -1
                elif ((intMonth-1)==2):
                    lessMonth = 2
                    if (int(year) % 4) == 0:
                        if (int(year) % 100) == 0:
                            if (int(year) % 400) == 0:
                                lessDay = 29
                            else: 
                                lessDay = 28
                        else:
                            lessDay = 29
                    else:
                        lessDay = 28
                else:
                    print ("BIG ERROR- No Month Connected")
            else:
                lessMonth = intMonth
        else:
            lessHour = intHour - 1
            lessDay = intDay
            lessMonth = intMonth
    elif (subTime >60):
        print ("MAJOR ERROR WITH INTERVAL TIME")
    else:
        lessMinute = intMinute - subTime
        lessHour = intHour
        lessDay = intDay
        lessMonth = intMonth
    
    # String formatting
    if (lessMonth < 10):
        lessMonth = '0'+ str(lessMonth)
    if (lessDay < 10):
        lessDay = '0'+ str(lessDay)   
    if (lessHour < 10):
        lessHour = '0'+ str(lessHour)    
    if (lessMinute < 10):
        lessMinute = '0'+ str(lessMinute)  
        
        
    year = str(year)
    lessMonth = str(lessMonth)
    lessDay = str(lessDay)
    lessHour = str(lessHour)
    lessMinute =str(lessMinute)
    
    
    #endCheckTime = int(checkTime)-(3000+4000)  ## LAME FIRST TRY - 3hr only
    
    endCheckTime = year+lessMonth+lessDay+lessHour+lessMinute +'00'

    print ("START: ", checkTime, ", END: ", endCheckTime, ", Interval:", deltaInterval,", SubTime:", subTime)
    
    
    #%% CHANGE THE TIME STRING THROUGHOUT THE ITERATION
    
    #FARBER
    directory2 = curdir + '/OBS/OBS:'
    #'/...path..../MODEL/ferry_data/OBS/OBS:'

    outputFile = directory2 + year +'-'+month+'-'+day+'_'+hour  # NEEDS TO BE ADJUSTED FOR Sub-1-HR data
    print (outputFile)
    
    #Open the output file that the data will be written
    outfile = open(outputFile,'w+')
    
    #%% Iterate backwards through the data.
    for row in readData:
        seq_num = seq_num-1
        #Cut computing time to next to nothing my cutting out almost all irrelevant data for the time period
        if (row[15:19] != year): continue
        elif (intMonth ==12 or intMonth == 1): print ("*************YEAR TROUBLE*********************")
        if int(row[19:21]) > intMonth: continue
        elif (intDay==1 or ((intMonth==2 and intDay == 28) or (intMonth==2 and intDay == 29)) or intDay==30 or intDay ==31): print ("*************END MONTH TROUBLE*********************")
        if (int(row[21:23]) > intDay): continue
        raw = row.strip().split()
        ttime = int(float(raw[1])) 

        #%% Does it fall between the time range we want
        if ttime <= int(checkTime) and ttime >= int(endCheckTime):# and raw[11] == 'FM-13':  # FERRY and raw[11] == FM-18  ## BUOY ONLY
            # No data for Dew Point (td), Geopotential Height (z)
            # 0 = ID, 1 = Date, 2 = Wind Speed, 3 = Wind Direction 4 = Air Temperature # 5 = Dewpoint Temperature
            # 6 = Relative Humidity 7 = Pressure 8 = Latitude 9 = Longitude 10 = Elevation (BOTH Sensor Height + Elevation)
            # 11 = Name String   12+13 = FM String   14 = Source String

            countTotal +=1        
            #%% CAREFULLY FORMATTING CONNECTED WITH DATA req. for Little_R format in OBSGRID and WRFDA
            # 6 is number not nan
            num_vld_fields = 7 - raw.count("-888888.00000")

            header = ['%20.5f' % float(raw[8]), '%20.5f' % float(raw[9]), '%40s' % str(raw[0]),  '%40s' % str(raw[11]), '%40s' % str(raw[12]+' '+raw[13]),\
                               '%40s' % str(raw[14]), '%20.5f' % float(raw[10]), '%10d' % num_vld_fields, '%10d' % 0,\
                               '%10d' % 0, '%10d' % seq_num, '%10d' % 0, '%10s' % isSounding, '%10s' % is_bogus, '%10s' % discard, '%10d' % -888888.,\
                               '%10d' % -888888., '%20s' % str(ttime), '%13.5f'% float(raw[7]), '%7d'% 0, '%13.5f' % -888888., '%7d' % 0, '%13.5f' % -888888., '%7d' % 0, '%13.5f' % -888888.,\
                               '%7d' % 0, '%13.5f' % -888888., '%7d' % 0, '%13.5f' % -888888., '%7d' % 0,'%13.5f' % -888888., '%7d' % 0, '%13.5f' % -888888., '%7d' % 0, '%13.5f' % -888888.,\
                               '%7d' % 0, '%13.5f' % -888888., '%7d' % 0, '%13.5f' % -888888., '%7d' % 0,'%13.5f' % -888888., '%7d' % 0, '%13.5f' % -888888., '%7d' % 0]
                          
            data = ['%13.5f'% float(raw[7]),'%7d'% 0,'%13.5f'% float(raw[10]),'%7d'% 0,'%13.5f'% float(raw[4]),'%7d'% 0,'%13.5f'% float(raw[5]),'%7d'% 0,'%13.5f'% float(raw[2]),'%7d'% 0,'%13.5f'% float(raw[3]),'%7d'% 0,\
                        '%13.5f'% -888888.,'%7d'% 0,'%13.5f'% -888888.,'%7d'% 0,'%13.5f'% float(raw[6]),'%7d'%0 ,'%13.5f'% -888888.,'%7d'%0]
            
            end_record = ['%13.5f'% -777777.,'%7d'% 0,'%13.5f'% -777777.,'%7d'% 0,'%13.5f'% 1.,'%7d'% 0,'%13.5f'% -888888.,'%7d'% 0,'%13.5f'% -888888.,'%7d'% 0,'%13.5f'% -888888.,'%7d'% 0,\
                        '%13.5f'% -888888.,'%7d'% 0,'%13.5f'% -888888.,'%7d'% 0,'%13.5f'% -888888.,'%7d'%0 ,'%13.5f'% -888888.,'%7d'%0]
                
            tail_record = ['%7d'% num_vld_fields,'%7d' % 0, '%7d' % 0]
            
            #%% WRITE TO THE FILE            
            outfile.writelines(header)
            outfile.writelines('\n')
            
            outfile.writelines(data)
            outfile.writelines('\n')
            
            outfile.writelines(end_record)
            outfile.writelines('\n')
            
            outfile.writelines(tail_record)
            outfile.writelines('\n')
            del data, header, end_record, tail_record
        
        # If data is before the time of interest move on to the next file but keep spot in iteration 
        elif ttime < int(endCheckTime):
            print ("Total Observations =" , countTotal)
            break
        
        
elapsed_time = t.time() - start_time
print (t.strftime("%H:%M:%S", t.gmtime(elapsed_time)))

