#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Last Updated on March 8th, 2018

@author: Eric Allen, University of Delaware
allenea@udel.edu

Combines all months in a year into yearly data file (1 per year)

Change the directory.
Run from folder with monthly data files

"""

import numpy as np
import csv
import pandas as pd
import glob
import time as t
from itertools import islice

##CHANGE THIS
directory = "/home/work/clouds_wind_climate/ferry_data/yearly/"

#%%

fileTypes = ['MET','EXO']
for fType in fileTypes:
    print fType
    HEADERS = []
    
    for file in glob.glob("*-"+fType+".csv"):
        print file
        with open(file,'rU') as infile:
            raw = csv.reader(infile,dialect='excel',delimiter=',')
            count = 0
            for row in raw:
                row2 = row[0:15]
                if count <= 2:
                    HEADERS.append(row2)
                else:
                    break
                count = count +1
        break
    #print HEADERS
    
    HEADER = np.array(HEADERS)
    dtf = pd.DataFrame(HEADER,index=None)
    #%%              
    
                    
    for year in range(2011,int(t.ctime(t.time())[-4:])+1):
        sYear = str(year)
        #for month in range(1,13):
        print year
        allfiles = []
        outstring = directory+sYear+"-"+fType+".csv"
    
        for file in glob.glob("*-"+fType+".csv"):
            if file[:4] == sYear:
                allfiles.append(file)
        print allfiles

        #%%
        filecount = len(allfiles)
        print filecount
        output = []
        if filecount > 0:  
            outname = sYear +'-'+fType+'.csv'
            for i  in range(filecount):
                with open(allfiles[i],'rU') as infile:
                    raw = csv.reader(infile,dialect='excel',delimiter=',')
                    next(islice(raw, 3, 3), None)  
                    for row in raw:
                        row2 = row[0:15]
                        output.append(row2)
            df = pd.DataFrame(output,index=None)
            frames = [dtf,df]
            result  = pd.concat(frames)
        
            #result.to_csv(outstring, index=False,index_label=False)
            #del sYear, outstring, df, output, result
            result2 = np.array(result)
            with open(outstring,'wt') as outfile:
                dataout = csv.writer(outfile,dialect='excel',delimiter=',')
                # Loop through rows with new columns included, write to file
                for row in result2:
                    dataout.writerow(row)
                del result, dataout, sYear, outstring, df, output, result2
        else:
            continue
