#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Updated March 8th 2018

@author: Eric Allen
allenea@udel.edu

Converts daily files into monthly files (once lat/lon has been converted)
"""

import numpy as np
import csv
import pandas as pd
import glob
import time as t
from itertools import islice
import os
#%%
outdir = os.path.abspath('../monthly_data/')

fileTypes = ['MET','EXO']
for fType in fileTypes:
    print (fType)
    HEADERS = []
    for file in glob.glob("*"+fType+"-latlon2.csv"):
        print (file)
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
        for month in range(1,12+1):
            print (year,month)
            allfiles = []
            if month<10:
                sMonth = '0'+str(month);
            else:
                sMonth = str(month);
            wantfiles = sYear + sMonth
            outstring = outdir+"/"+wantfiles+"-"+fType+".csv"
    
            for file in glob.glob("*-"+fType+"-latlon2.csv"):
                if file[:6] == sYear + sMonth:
                    allfiles.append(file)
            
            #%%
            filecount = len(allfiles)
            print (filecount)
            output = []
            if filecount > 0:  
                outname = wantfiles +'-'+fType+'.csv'
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
            
                #del wantfiles, outstring, df, output, result
                result2 = np.array(result)
                with open(outstring,'wt') as outfile:
                    dataout = csv.writer(outfile,dialect='excel',delimiter=',')
                    # Loop through rows with new columns included, write to file
                    for row in result2:
                        dataout.writerow(row)
                    del result, dataout, wantfiles, outstring, df, output, result2
            else:
                continue
