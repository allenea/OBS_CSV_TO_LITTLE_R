#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Last Updated on Tues Aug 20 8:00pm 2018

@author: Eric Allen
allenea@udel.edu
Clouds_Wind_Climate Workgroup, University of Delaware


NOTE TO USERS:
############################################################
User will need to update the directory paths for their computer. Variables: data_file, directory, directory2, subTime (twindo/Time before analysis time you want obs put into OBS files in Little_R format),


USER WARNING: THIS FILE IS NOT CREATED TO HANDLE Dew-Point Temperature. My data did not have it. Td is hard-coded as a missing value in the initialized variables. Same with soundings (=False).

Dew point Temperature (Td) and Geopotential Height (Z) data was not collected for this study and not processed for assimilation. Z = Elevation for this program and for OBSGRID. This program should work if the user has that data to pass the program. But my scripts don't handle those observations so you will need to make some changes.

Make sure that you have elevation of the observation to also include sensor height as well as the elevation. In this case geopotential height is set to the elevation (which was the sensor height + elevation). OBSGRID expects these to be the same for surface observations.


###########################################################


DEOS and Cape May Lewes Ferry is being reformatted into Little_R format required for OBSGRID. Another file will be made for CMLF only and DEOS only. The IF statement will add an extra condition that the FM code matches the expected dataset. 13- Ferry. 12-DEOS. See below.

Open/Read the DEOS + CMLF data from the text file created in prep4r. Reverse the list so the newest stuff is at the top and work backwards. Also sets the sequence number as a fail-safe.

V3.8 is supposed to use most recent but I have serious concerns about several features in what is supposed to be V3.8. I exchanged many emails with the WRF-Help people and provided several suggestions. Namely, I do not think that radius of influence scale works. It is also supposed to better handle/reorder observations so most recent are used first. This does the same thing. The seq_num counts up (from the end of the file towards the front) and the file is processed in reverse. IMO the update in V3.8 is just a 3rd level of verification. Should not be an issue. 
Downloaded from   http://www2.mmm.ucar.edu/wrf/users/download/get_sources.html



ADDITIONAL/DETAILED INFORMATION ON HOW THIS PROGRAM WORKS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Initialize constants and unknown variables (Td and Z)

Read in all of the met_em files from the scratch directory and store as a list... reverse that list to work from Present->Past
Identify the interval between the two files. Determine what the time range should be for each file. This value is preset. You can change this to whatever you want. OBSGRID does not nudge at intervals less than 1 hour.

*** Go through each met_em file in the list. Parse it (Year, Month, Day Hour, Min). Create a date-string... starting check point
Then based on the interval already identified. Create the end point that the observations should fall between. Calculate that.
	- Again remember you are working backwards. Check to make sure hours, days, months do not change. If they do address that.
reformat the endCheckPoint string that will be used for bound comparison. 
Setup and open the output file for each time-step that the data will be stored.
Iterate through the data (remember it's backwards). If it is not the right year, month, and day in the right month it moves to the next observations.
Once it found the observations from that day. Parse the string. Check if it falls within the start and end time-range-interval. 
	-  If it does then save it in the little r format with the header, data, end record, tail to the text file.
	-  If it does not fall within the range and is below the end record break the loop. Open a new met_em file and continue from the ***.

Then once it is through the last file the program ends.

Please log output file so you can go back and identify possible errors until further testing has been completed. Try all possible situations. Beginning of the month, end of the month end of the year 12/31 or 1/1/ different hours of the day. Leap years leap days, etc. All of these should be accounted for but I haven't formally tested. I have verified that it is working correctly for my research runs.

-----------
Concerns and Future Thoughts on the research:

One concern is that the one observation after is getting tossed but I don't think that is the end of the world. Only place obs might be getting lost in the this.... Not sure why I thought this or where I was going with this. Will have to dig in, but I don't see where this might be an issue. Leaving this comment so you are aware that at one point I thought I might be losing an observation.
Bigger concern would be the endCheck and making sure that it moves month-month, day-to-day, hour-hour, and down to the minute... I think I have coded it to do that but there could be an occasion where it messes up because of how I coded. There was nothing wrong in my initial case study...
-------
This is very fast and left a little clock to tell you how long the program took to run start to finish.
"""

#IMPORTS
import glob
from datetime import datetime, date, time, timedelta
import time as t
start_time = t.time()


#OPEN/READ DATA FILE - GET FARBER LOCATION
data_file = '/home/work/clouds_wind_climate/allenea/my361/WRF/delaware_bay_configuration/ferry_data/data_CMLF2011_2016_D2013_2017.txt'
infile = open(data_file,'rU')
readData = infile.readlines()
readData.reverse()
    
# INITIALIZE CONSTANT VARIABLES. MISSING OR DOESN'T CHANGE THROUGHOUT
td = -888888.0;
isSounding = 'F';is_bogus = 'F';discard = 'F' # False- Booleans
seq_num = len(readData)
print(seq_num)

# IDENTIFY FIRST INSTANCE OF THE MET_EM FILE... AKA THE START TIME/ End Time. Reverse them. Works back to front
allfiles = []
directory='/home/work/clouds_wind_climate/allenea/my361/WRF/delaware_bay_configuration/scratch-dir/met_em.d01.'
length = len(directory)
for file in glob.glob(directory+"*.nc"):
    allfiles.append(file)
del file
allfiles.sort()
allfiles.reverse()
print allfiles

#Calculate the time between two analysis times (interval_seconds)
IntervalTime = datetime.strptime(allfiles[0][length:length+19],"%Y-%m-%d_%H:%M:%S") - datetime.strptime(allfiles[1][length:length+19],"%Y-%m-%d_%H:%M:%S")
IntervalTime = IntervalTime.total_seconds()


# SET WINDOW OF TIME LEADING UP TO ANALYSIS TIME
if int(IntervalTime//60) < 60:  ##Interval = int(IntervalTime//60) ## Minutes
    deltaInterval = int(IntervalTime//60)
    subTime = 4
    print deltaInterval, "-MINUTE DATA"
elif int(IntervalTime//(60*60)) < 24:  ##Interval = int(IntervalTime//(60*60)) ## Hours
    deltaInterval = int(IntervalTime//(60*60))
    print deltaInterval, "-HOURLY DATA"
    if deltaInterval == 1:
        subTime = 20
    elif deltaInterval == 3:
        subTime = 30
    else:
        subTime = 55
else:
    print "This data is at a greater interval than daily"
    

#%% Go through the files in order and pull the times (splice)
for file in allfiles:
    countTotal = 0
    timestring = file[length:length+19]###file[68:87]
    print file[length:length+19]   # FOR FARBER

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
        
    print "Year:",year, ". Month:",month,". Day:",day,". Hour:",hour,".Minute:", minute

    # TIME STEP-WHAT DO I WANT TO USE?
    checkTime = year+month+day+hour + minute +'00'
    
    
    #%% Calculates and Creates End CheckTime String -> int for comparison
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
                    print "BIG ERROR- No Month Connected"
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
                    print "BIG ERROR- No Month Connected"
        else:
            lessHour = intHour - 1
            lessDay = intDay
            lessMonth = intMonth
    elif (subTime >60):
        print "MAJOR ERROR WITH INTERVAL TIME"
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
    

    endCheckTime = year+lessMonth+lessDay+lessHour+lessMinute +'00'

    print "START: ", checkTime, ", END: ", endCheckTime, ", Interval:", deltaInterval,", SubTime:", subTime
    
    
    #%% CHANGE THE TIME STRING THROUGHOUT THE ITERATION

    #FARBER
    directory2 = '/home/work/clouds_wind_climate/allenea/my361/WRF/delaware_bay_configuration/ferry_data/OBS/OBS:'

    outputFile = directory2 + year +'-'+month+'-'+day+'_'+hour  # NEEDS TO BE ADJUSTED FOR Sub-1-HR data
    print outputFile
    
    #Open the output file that the data will be written
    outfile = open(outputFile,'w+')
    
    #%% Iterate backwards through the data.
    for row in readData:
        seq_num += 1
        #Cut computing time to next to nothing my cutting out almost all irrelevant data for the time period
        if (row[17:21] != year): continue
        elif (intMonth ==12 or intMonth == 1): print "*************YEAR TROUBLE*********************"
        if int(row[21:23]) > intMonth: continue
        elif (intDay==1 or ((intMonth==2 and intDay == 28) or (intMonth==2 and intDay == 29)) or intDay==30 or intDay ==31): print "*************END MONTH TROUBLE*********************"
        if (int(row[23:25]) > intDay): continue
        raw = row.strip().split()

        #%% Does it fall between the time range we want
        if int(raw[1]) <= int(checkTime) and int(raw[1]) >= int(endCheckTime):# and raw[11] == 'FM-13':  # and raw[11] == FM-13  ## FERRY ONLY
            # No data for Dew Point (td), Geopotential Height (z)
            # 0 = ID, 1 = Date, 2 = Wind Speed, 3 = Wind Direction 4 = Air Temperature
            # 5 = Relative Humidity 6 = Pressure 7 = Latitude 8 = Longitude 9 = Elevation
            # 10 = Name String   11+12 = FM String   13 = Source String
	    countTotal +=1
            #print(seq_num)        
            #%% CAREFULLY FORMATTING CONNECTED WITH DATA req. for Little_R format in OBSGRID and WRFDA
            header = ['%20.5f' % float(raw[7]), '%20.5f' % float(raw[8]), '%40s' % str(raw[0]),  '%40s' % str(raw[10]), '%40s' % str(raw[11]+' '+raw[12]),\
                               '%40s' % str(raw[13]), '%20.5f' % float(raw[9]), '%10d' % 5, '%10d' % 0,\
                               '%10d' % 0, '%10d' % seq_num, '%10d' % 0, '%10s' % isSounding, '%10s' % is_bogus, '%10s' % discard, '%10d' % -888888.,\
                               '%10d' % -888888., '%20s' % str(raw[1]), '%13.5f'% float(raw[6]), '%7d'% 0, '%13.5f' % -888888., '%7d' % 0, '%13.5f' % -888888., '%7d' % 0, '%13.5f' % -888888.,\
                               '%7d' % 0, '%13.5f' % -888888., '%7d' % 0, '%13.5f' % -888888., '%7d' % 0,'%13.5f' % -888888., '%7d' % 0, '%13.5f' % -888888., '%7d' % 0, '%13.5f' % -888888.,\
                               '%7d' % 0, '%13.5f' % -888888., '%7d' % 0, '%13.5f' % -888888., '%7d' % 0,'%13.5f' % -888888., '%7d' % 0, '%13.5f' % -888888., '%7d' % 0]
                               #IF YOU HAVE DEWPOINT TEMPERATURE ADD TO THE END OF YOU CSV DATA FILES AND THEN IN PREP_4_R add it to the last column. Change Td here and where initialized above to be dynamic.
            data = ['%13.5f'% float(raw[6]),'%7d'% 0,'%13.5f'% float(raw[9]),'%7d'% 0,'%13.5f'% float(raw[4]),'%7d'% 0,'%13.5f'% td,'%7d'% 0,'%13.5f'% float(raw[2]),'%7d'% 0,'%13.5f'% float(raw[3]),'%7d'% 0,\
                        '%13.5f'% -888888.,'%7d'% 0,'%13.5f'% -888888.,'%7d'% 0,'%13.5f'% float(raw[5]),'%7d'%0 ,'%13.5f'% -888888.,'%7d'%0]
            
            end_record = ['%13.5f'% -777777.,'%7d'% 0,'%13.5f'% -777777.,'%7d'% 0,'%13.5f'% 1.,'%7d'% 0,'%13.5f'% -888888.,'%7d'% 0,'%13.5f'% -888888.,'%7d'% 0,'%13.5f'% -888888.,'%7d'% 0,\
                        '%13.5f'% -888888.,'%7d'% 0,'%13.5f'% -888888.,'%7d'% 0,'%13.5f'% -888888.,'%7d'%0 ,'%13.5f'% -888888.,'%7d'%0]
                        # No soundings used so I just hard-coded 1 observation per data-record
            tail_record = ['%7d'% 1,'%7d' % 0, '%7d' % 0]
            
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
        elif int(raw[1]) < int(endCheckTime):
            print "Total Observations =" , countTotal
            break
        
        
elapsed_time = t.time() - start_time
print t.strftime("%H:%M:%S", t.gmtime(elapsed_time))
