"""
Created on Wed Aug  7 10:04:27 2019

@author: Eric Allen
allenea@udel.edu
Clouds_Wind_Climate Workgroup, University of Delaware
Last Updated: 2/6/2020

OBSGRID considers within 30 mins as same time - merged. Option commented out to
 do 5-minute. New OBSGRID treats with provided time instead of analysis time.
 For now leave as 30 minute (considered for any analysis time), but only give
 20 minutes of data. Therefore shortening the window. Future try the 5-minute
 option with a longer subtime.

 Multiple observations are assigned but with both seq_num (lower numbers more recent)
 and the time stamp the closest one should be used. If it's missing data/observation
 then it can pull from one of the other times.

Read in all of the met_em files from the scratch directory and store as a list...
 Identify the interval between the two files.
 Determine what the time range should be for each file. This value is preset.
"""
#IMPORTS
import os
import sys
import getopt
import glob
import time as t
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

def main(argv):
    """doc-string"""
    version = ''
    try:
        opts, _args = getopt.getopt(argv, "hv:", ["version="])
    except getopt.GetoptError:
        print('little_r_converter_v2.py -v <version>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('little_r_converter_v2.py  -v <version>')
            sys.exit()
        elif opt in ("-v", "--version"):
            version = arg
        else:
            sys.exit(0)
    print('Version is ', version)

    deos_assimilation_list = ['DADV', 'DBBB', 'DBLK', 'DBNG', 'DBRG', 'DDFS',\
                              'DELN', 'DGES', 'DGUM', 'DHAR', 'DIRL', 'DJCR',\
                              'DLAU', 'DMIL', 'DRHB', 'DSEA', 'DSJR', 'DSMY',\
                              'DSND', 'DWAR']
    #GET FARBER LOCATION
    curdir = os.getcwd()

    # ACCEPTABLE MARINE FM CODES
    marine_list = ["FM-13 SHIP", "FM-18 BUOY", "FM-19 BUOY"]
    terrestrial_list = ["FM-12 SYNOP", "FM-15 METAR", "FM-16 SPECI",\
                        "FM-32 PILOT", "FM-35 TEMP"]

    acceptable_list = []
    if version == "CMLF":
        acceptable_list = ["FM-13 SHIP"]
    elif version == "DEOS":
        acceptable_list = ["FM-35 TEMP"]
    elif version == "BOTH":
        acceptable_list = ["FM-35 TEMP"] + ["FM-13 SHIP"]
    elif version == "BUOY":
        acceptable_list = marine_list
    elif version == "LAND":
        acceptable_list = terrestrial_list
    elif version == "ALL":
        #SET LATER WITH ALL FM CODES IN THE DATASET
        pass
    else:
        print("NOT AN ACCEPTABLE CODE. USING ALL")
        acceptable_list = terrestrial_list + marine_list

    # INITIALIZE CONSTANT VARIABLES. MISSING OR DON'T CHANGE THROUGHOUT
    is_sounding = 'F'
    is_bogus = 'F'
    discard = 'F' # False- Booleans

    # Relative Humidity as set with too few percision in the pre-processing program
    dtypes_dict = {"ID_String":str, "DATE":np.float64, "Wind_Speed (m/s)":str,\
                "Wind_Direction (deg)":str, "Air_Temperature (K)":str,\
                "Dewpoint_Temperature (K)":str, "Relative_Humidity (%)":np.float64,\
                "Pressure (Pa)":str, "Latitude":str, "Longitude" :str,\
                "Elevation_SensorHeight (m)":str, "Name_string":str, "FM_string":str,\
                "FM_Code":str, "Source_string":str}

    header_in = ["ID_String", 'DATE', 'Wind_Speed (m/s)', 'Wind_Direction (deg)',\
                 'Air_Temperature (K)', "Dewpoint_Temperature (K)",\
                  'Relative Humidity (%)', 'Pressure (Pa)', 'Latitude',\
                  'Longitude', 'Elevation (m)', 'Name_string', 'FM_string',\
                  'FM_Code', 'Source_string']


    # IDENTIFY FIRST INSTANCE OF THE MET_EM FILE... AKA THE START TIME/ End Time.
    outdir = os.path.abspath('../scratch-dir')
    directory = outdir+'/met_em.d01.'
    length = len(directory)
    allfiles = glob.glob(directory+"*.nc")
    allfiles.sort()

    #Second - First
    interval_time = datetime.strptime(allfiles[1][length:length+19], "%Y-%m-%d_%H:%M:%S")\
                - datetime.strptime(allfiles[0][length:length+19], "%Y-%m-%d_%H:%M:%S")
    interval_time = interval_time.total_seconds()

    ## OBSGRID considers within 30 mins as same time - merged.
    #Option commented out to do 5-minute.
    if int(interval_time//60) < 60: ## Minutes
        delta_interval = int(interval_time//60)
        subtime = 4
        print(delta_interval, "- MINUTE DATA")
    elif int(interval_time//(60*60)) < 24: ## Hour(s)
        delta_interval = int(interval_time//(60*60))
        print(delta_interval, "-HOURLY DATA")
        if delta_interval == 1:
            subtime = 20
        elif delta_interval == 3:
            subtime = 30
        else:
            subtime = 55
    else:
        print("This data is at a greater interval than daily")
        sys.exit(0)

    #Last - First
    total_time = datetime.strptime(allfiles[-1][length:length+19], "%Y-%m-%d_%H:%M:%S")\
                - datetime.strptime(allfiles[0][length:length+19], "%Y-%m-%d_%H:%M:%S")
    total_time = total_time.total_seconds()

    # DEALING WITH TIME RANGE
    tdelta = timedelta(seconds=total_time)
    start_object = datetime.strptime(allfiles[0][length:length+19], "%Y-%m-%d_%H:%M:%S")
    start_time = datetime.strftime(start_object, '%Y%m%d%H%M') +'00'
    end_object = start_object+tdelta
    end_time = datetime.strftime(end_object, '%Y%m%d%H%M') +'00'
    obj_diff = end_object-start_object

    #print("Interval Time: ",interval_time)
    print("Total Model Time (sec): ", total_time)
    print("Case:", datetime.strptime(allfiles[0][length:length+19], "%Y-%m-%d_%H:%M:%S"))
    print("START TIME: ", start_time)
    print("END TIME: ", end_time)
    print(start_time, "   ", end_time, "   ", obj_diff.total_seconds()/(60*60), "hours")
    print("SUBTRACT TIME (each step): ", subtime)


    ## READ IN DATA - CHANGE FOR FLORIDA
    data_file = curdir+'/all_delaware_data_eric_thesis_OBS.txt'
    #data_file = curdir+'/all_florida_data_eric_thesis_OBS.txt'

    print(data_file)

    infile = pd.read_csv(data_file, delim_whitespace=True, dtype=dtypes_dict, header=None,\
                                                                         names=header_in)
    infile["FM_string"] = infile["FM_string"] +" "+ infile["FM_Code"]
    codes_found = list(set(infile["FM_string"]))
    if version == "ALL":
        acceptable_list = codes_found

    print("CODES FOUND: ", codes_found)
    print()
    print("ACCEPTABLE FM CODES FOR THIS SIMULATION:", acceptable_list)

    infile["DATE"] = infile["DATE"].astype(int)
    infile["DATE"] = infile["DATE"].astype(str)
    infile["Relative Humidity (%)"] = infile["Relative Humidity (%)"].astype(str)
    lst_time = list(infile["DATE"])
    startpt = lst_time.index(start_time)
    print("Starting Point:", startpt)
    del lst_time
    read_data = infile.drop(['FM_Code'], axis=1)
    del infile
    data = np.array(read_data)
    del read_data

    master_key = []
    for idx in range(startpt, len(data)):
        time_1 = str(data[idx][1])
        year = int(time_1[0:4])
        month = int(time_1[4:6])
        day = int(time_1[6:8])
        if year != start_object.year:
            continue
        elif (start_object.month == 12 or start_object.month == 1):
            print("*************YEAR TROUBLE*********************")

        if month < start_object.month:
            continue
        elif (start_object.month == 2 and (start_object.day == 28 or\
                start_object.day == 29)) or start_object.day == 30 or\
                                           start_object.day == 31:
            print("*************END MONTH TROUBLE*********************")

        if day < start_object.day:
            continue
        if day > end_object.day:
            break
        if start_time <= time_1 <= end_time:
            master_key.append(data[idx])

    del data
    #%%
    count_total = 0

    for file in allfiles:
        total = 0
        # TIME RANGE FOR GIVEN FILE
        tstep = timedelta(minutes=subtime)
        eobject = datetime.strptime(file[length:length+19], "%Y-%m-%d_%H:%M:%S")
        estep = datetime.strftime(eobject, '%Y%m%d%H%M') +'00'
        sobject = eobject-tstep
        sstep = datetime.strftime(sobject, '%Y%m%d%H%M') +'00'
        print("\nSTART: ", sstep, ", END: ", estep, ", Interval:", tstep, ", subtime:", subtime)

        #Set and open the output file where the obs will be written
        directory2 = curdir + '/OBS/OBS:'
        output_file = directory2 + eobject.strftime("%Y")+'-'+eobject.strftime("%m")+\
                            '-'+eobject.strftime("%d")+'_'+eobject.strftime("%H")
        print(output_file)
        outfile = open(output_file, 'w+')

        #Iterate through the data.
        seq_num = len(master_key)
        for raw in master_key:
            seq_num -= 1

# =============================================================================
#           # No data for Dew Point (td), Geopotential Height (z)
#
#            array([
#            0: 'DJCR',                                     #ID
#            1: '20140603145500',                           #Date
#            2: '2.40000',                                  #Wind Speed
#            3: '251.00000',                                #Wind Direction
#            4: '299.65000',                                #Air Temperature
#            5: '289.85000',                                #Dewpoint Temperature
#            6: '-888888.00000',                            #Relative Humidity
#            7: '-888888.00000',                            #Pressure
#            8: '38.59472',                                 #Latitude
#            9: '-75.43667',                                #Longitude
#            10: 22.29,                                     #Elevation (BOTH Sensor HGT + Elevation)
#            11: 'Jones_Crossroads,_DE-SSWMC',              #Name String
#            12: 'FM-12 SYNOP',                             #FM String
#            13: 'Delaware_Environmental_Observing_System'  #Source String
#            ], dtype=object),
# =============================================================================

            ttime = datetime.strptime(raw[1], "%Y%m%d%H%M%S")

            #Does it fall between the time range we want? Yes.
            #print(raw[12])
            if sobject <= ttime <= eobject and raw[12] in acceptable_list:
                if version == "DEOS" and\
                    (raw[13] != 'Delaware_Environmental_Observing_System' or\
                    raw[0] not in deos_assimilation_list):
                    pass
                elif version == "BOTH" and raw[12] == "FM-35 TEMP" and\
                    (raw[13] != 'Delaware_Environmental_Observing_System' or\
                    raw[0] not in deos_assimilation_list):
                    pass
                else:
                    #print(raw[0], raw[12], raw[13])
                    count_total += 1
                    total += 1
                    num_vld_fields = 7 - list(raw).count("-888888.00000")

                    #CAREFULLY FORMATTING CONNECTED WITH DATA req. 4 Little_R fmt in OBSGRID & WRFDA

                    header = ['%20.5f' % float(raw[8]), '%20.5f' % float(raw[9]),\
                              '%40s'%str(raw[0]), '%40s'%str(raw[11]), '%40s'%str(raw[12]),\
                               '%40s'%str(raw[13]), '%20.5f'%float(raw[10]),\
                               '%10d'%num_vld_fields, '%10d'%0,\
                               '%10d'%0, '%10d' % seq_num, '%10d' % 0, '%10s' % is_sounding,\
                               '%10s'% is_bogus, '%10s'%discard, '%10d'%-888888.,\
                               '%10d'%-888888., '%20s' % str(raw[1]), '%13.5f'% float(raw[7]),\
                               '%7d'% 0, '%13.5f'%-888888., '%7d'%0, '%13.5f'%-888888., '%7d'%0,\
                               '%13.5f'%-888888., '%7d'%0, '%13.5f'%-888888., '%7d'%0,\
                               '%13.5f'%-888888., '%7d'%0, '%13.5f'%-888888., '%7d'%0,\
                               '%13.5f'%-888888., '%7d'%0, '%13.5f'%-888888.,\
                               '%7d'%0, '%13.5f'%-888888., '%7d'%0, '%13.5f'%-888888.,\
                               '%7d'%0, '%13.5f'%-888888., '%7d'%0, '%13.5f'%-888888., '%7d'%0]


                    data = ['%13.5f'% float(raw[7]), '%7d'% 0, '%13.5f'% float(raw[10]), '%7d'% 0,\
                            '%13.5f'% float(raw[4]), '%7d'% 0, '%13.5f'% float(raw[5]), '%7d'% 0,\
                            '%13.5f'% float(raw[2]), '%7d'% 0, '%13.5f'% float(raw[3]), '%7d'% 0,\
                                '%13.5f'% -888888., '%7d'% 0, '%13.5f'% -888888., '%7d'% 0,\
                                '%13.5f'% float(raw[6]), '%7d'%0, '%13.5f'% -888888., '%7d'%0]


                    end_record = ['%13.5f'% -777777., '%7d'% 0, '%13.5f'% -777777.,\
                                  '%7d'% 0, '%13.5f'% 1., '%7d'% 0, '%13.5f'% -888888.,
                                  '%7d'% 0, '%13.5f'% -888888., '%7d'% 0, '%13.5f'% -888888.,\
                                  '%7d'% 0, '%13.5f'% -888888., '%7d'% 0, '%13.5f'% -888888.,\
                                  '%7d'% 0, '%13.5f'% -888888., '%7d'%0, '%13.5f'% -888888.,\
                                  '%7d'%0]


                    tail_record = ['%7d'% num_vld_fields, '%7d' % 0, '%7d' % 0]

                    #WRITE TO THE FILE
                    outfile.writelines(header)
                    outfile.writelines('\n')

                    outfile.writelines(data)
                    outfile.writelines('\n')

                    outfile.writelines(end_record)
                    outfile.writelines('\n')

                    outfile.writelines(tail_record)
                    outfile.writelines('\n')
                    del data, header, end_record, tail_record

            elif ttime > eobject:
                print("Number of Observations = " + str(total))
                break

    print("\n\nTotal Observations = " + str(count_total))

if __name__ == "__main__":
    START_TIME = t.time()
    print(sys.argv)
    try:
        ARG1 = sys.argv[1]
    except IndexError:
        print("Usage: " + os.path.basename(__file__) +\
              " -v <arg1>" + "   ...   provide the type (DEOS/CMLF/BOTH/BUOY/LAND/ALL)")
        sys.exit(1)

    main(sys.argv[1:])
    ELAPSED_TIME = t.time() - START_TIME
    print(t.strftime("%H:%M:%S", t.gmtime(ELAPSED_TIME)))
