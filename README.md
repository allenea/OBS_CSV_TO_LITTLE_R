# OBS_CSV_TO_LITTLE_R

Eric Allen, University of Delaware, Last Updated: 2/4/2019
Contact allenea@udel.edu with any questions.

DISCLAIMER: 
If using this code or referencing it for your own project please acknowledge Eric Allen and the University of Delaware. Neither Eric Allen or the University of Delaware shall be liable for any damages direct, indirect, accidental, or otherwise and not responsible for any damages. This code is being released to help other students, researchers, and members of the community. This code shall not be used directly or modified for commercial sale or redistribution. Please contribute to the code if you have found a way to improve it so that your findings may benefit others. This code is open-source with the exception of commercial use. Please contact me with any questions, concerns, or contributions. Or if you find this benefitial.




Abbreviations and Data Sources:

DEOS = Delaware Environmental Observing System
Data available: http://www.deos.udel.edu/data/

CMLF = Cape May Lewes Ferry
Data Available: http://www.deos.udel.edu/Ferry/data.php




Notes how this works for me:

- Temporary sensor height for CMLF is 20m. Once we get an accurate measurement it needs to be updated and everything reprocessed. 20m is a good estimate and more representative of the conditions than leaving elevation as 0.




#### IMPORTANT #####

Directories/python programs:


DEOS_DATA: This holds a csv file with the metadata for all the DEOS stations. There is a file for FormattedData. That is how the data was obtained from DEOS. 

DEOS_DATA/FormattedData: This folder contains a DEOS_reformat.py file that parses the time, combines the metadata with the data, and places the data in the Reformatted folder.

DEOS_DATA/Reformatted: CombineALL_DEOS.py combines each DEOS station and it's data into one big csv file that will be placed in Prep4R. Where it will be combined with the CMLF data. This file does have one hardcoded variable that the user should be aware of. It is a simple switch to make it dynamic. But for speed the user might want to calculate that variable and hardcode it.




raw_transferred: Raw observation data is placed into this folder. The data has it's latitude and longitude converted into decimal degrees and placed into the converted_data folder. This is done by latlonconversion.py

converted_data: Takes daily data files and combines them into monthly files. This is done in MonthlyFiles.py. In this step I also have a program that creates a graphic to display when data is available. I am not sharing this script. The output files are placed in monthly_data


monthly_data: All monthly files are combined into yearly files by CombineMonthly.py. The outputs are placed in the yearly folder.


yearly: CombineAll.py takes yearly files for the CMLF and combines them into one file.That file is placed in all_data. 


all_data: QualityControl.py is an extra step to try to fill in the blank for some observations with missing locations. It checks near observations on each side (within an hour) to see if it can extrapolate the ferry location. If it can't the observation is left but with missing value flags. There might be a better way to save more observations. The output from this program is placed in Prep4R


Prep4R: prep_4_r_w_DEOS processes both types of data (CMLF and DEOS). It converts the time to UTC time from the local timezone. It does some reformatting like making sure the longitude is west (-1). Sets elevation values for CMLF (temporarily 20m). Reads in all the data. Gives missing values -888888.0 flag which is what OBSGRID expects. It also assigns metadata for the CMLF (elevation, ID_String, Name_String, FM_String, Source_String). It does the same for DEOS data but the metadata is attached to the input data for each station and that is used. The files are concatenated and sorted by time in chronological order. The output from this is a ASCII-TEXT FILE that is carefully formatted. BE VERY CAREFUL. ADD DEW POINT TEMPERATURE OR GEOPOTENTIAL HEIGHT INFO TO THE END.  This text file will be used to create little_r format data at model-run-time. 


text_to_little_r: iterLittle_R.py figures out which data needs to be converted to little R.  It takes the met_em files and calculates the interval (time-step) between the files. That helps it decide what to make the interval time. Between the interval time and analysis time any observations that are in the interval leading unto the analysis time are converted to little_r format and stored in the OBS: files. 


text_to_little_r/OBS: This is a sample output of iterLittle_R.py from one of my runs. The data is in Little_R format.




