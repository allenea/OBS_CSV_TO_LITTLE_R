# OBS_CSV_TO_LITTLE_R

Eric Allen, University of Delaware, Last Updated: 2/10/2020
Contact allenea@udel.edu with any questions.

DISCLAIMER: 
If using this code or referencing it for your own project please acknowledge Eric Allen and the University of Delaware. This is research code. It may take some work to fit your needs.

The data-processing code for the Delaware and New Jersey Mesonet Data, NDBC, Local Climate Data, Mesowest, DelDOT, and more will be released after I have finished my thesis.

This can be very memory intensive reading it large text files (>10gb) and when working with 10's of millions of observations it is best to run on a HPC.

process_data.sh shows some of the workflow in processing the observations.

The input data should be located in the root directory.

Inside the data directory the folder "All_Sources" holds all of the processed data for each source of data. These csv files are all formatted the same.

Then combine and qc the data before writing to a text file in a uniform format that can then be used in the little_r_converter_v2.py and for other purposes.


#### IMPORTANT #####

Directories/python programs:


little_r_converter_v2.py is used to take all the data that has been processed, extracts the relevant data and creates the appropriate files. This program requires the met_em files.

OBS: This is where the outputs are located.

Data: Where all the data is processed and stored. The final output of this is moved to the root directory in process_data.sh