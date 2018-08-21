#--------------------------------------------------
# Alex Schroth
# Last Updated: JAN 27 2018  -- Eric
#
# This script will take the monthly ExoSonde files
#  provided to DEOS and reformat the latitude and
#  longitude into a much more user-friendly format.
# Rather than overwriting original files, this
#  is set up to create new files to protect the
#  integrity of the originals.
#
# Run in the directory for files that need latitude and longitude corrected to decimal
#--------------------------------------------------

import csv
import glob
import os

count = 0
# Outer loop to do for each file
for file in glob.glob("*.csv"):
    print ("Editing " + file)
    # Store filename without '.csv'
    name = file[:-4]
    # New array to store all data
    data = []
    # Read data from file and save to use
    #ERIC: Changed 'rb' to 'rt' (read text)
    with open(file,'rt') as infile:
        raw = csv.reader(infile,dialect='excel',delimiter=',')
        print(raw)
        for row in raw:
            row2 = row[0:13]
            data.append(row2)
    #--------------------------
    #CREATE NEW LAT LON COLUMNS
    #--------------------------
            
 # Alex wrote this del row but it throw  and error that row not defined. It looks like row is only defined in the for loop
 # I would agree, so I do not think this is a problem.  -Eric
 
   # del row
    rowcount = 1
    for row in data:
        # First 3 rows are header text
        #if rowcount <= 3:
        #First row is the header (Monthly)
        if rowcount <= 1:

            rowcount = rowcount+1
            row.append(" ")
            row.append(" ")
            continue
        # All other rows
        else:
            dumblat = row[9] #Latitude column
            dumblon = row[10] #Longitude column
            # Need Try-Except because some rows DO NOT have lat/lon
            # and we can't convert blank spaces to numbers!
            try:
                # Latitude-In format ##.##.##.0
                latdeg = float(dumblat[0:2])
                latmin = float(dumblat[3:8])
                latmindec = latmin/60.0
                newlat = latdeg+latmindec
                # Longitude-In format ###.##.##.0
                londeg = float(dumblon[0:3])
                lonmin = float(dumblon[4:9])
                lonmindec = lonmin/60.0
                newlon = londeg+lonmindec

                # Append new lat/lon columns to each row
                row.append(newlat)
                row.append(newlon)
                rowcount = rowcount+1

            except:
                rowcount = rowcount+1
                row.append("NaN")
                row.append("NaN")
                continue

    # Construct new file name, open for writing
    outstring = name+"-latlon2.csv"
    #ERIC: Changed 'wb' to 'wt' (write text)
    with open(outstring,'wt') as outfile:
        dataout = csv.writer(outfile,dialect='excel',delimiter=',')
        # Loop through rows with new columns included, write to file
        for row in data:
            dataout.writerow(row)
    del data, dataout




