#!/bin/bash
#!/usr/bin/expect

# Eric Allen 2/4/2020
# allenea@udel.edu

#OVERVIEW: Prepares data for little R format.

echo "Importing software"
source /etc/profile.d/valet.sh
vpkg_rollback all
vpkg_require anaconda/5.2.0:python3
source activate /home/work/$WORKGROUP/sw/geo-py/20190511/
vpkg_require geo-py/20190511


MDIR=$PWD
BUOY=${MDIR}/BUOY_DATA/
DDOT=${MDIR}/DelDOT/
DEOS=${MDIR}/DEOS/
MESO=${MDIR}/Mesowest/
NCEI=${MDIR}/NCEI_LCD/
NJMET=${MDIR}/NJMET/
VERIFY=${MDIR}/Verify_Converted/
FERRY=${MDIR}/FERRY/
obsdir=/home/work/clouds_wind_climate/WRF4/DelWRF/observation_data/
seabreeze=/home/work/clouds_wind_climate/WRF4/DelWRF/observation_data/SeaBreeze_Data/

cd ${DEOS}
python DEOS_Prep.py
python CombineAll_DEOS.py
echo "Done with DEOS"

cd ${FERRY}
echo "CMLF Pre-Pre-Processing"
cd ${FERRY}/raw_transferred/
#echo "Getting Data From Aurora"
python latlonconversion.py
cd ${FERRY}/converted_data/
#qsub data_availability_figures.qs
python MonthlyFiles.py
cd ${FERRY}/monthly_data/
python CombineMonthly.py
cd ${FERRY}/yearly/
python CombineAll.py
cd ${FERRY}/all_data/
#THIS IS FOR INTERPOLATING FERRY LOCATION IN THE RARE-CASES
python QualityControl.py
echo "Done with CMLF Pre-Pre-Processing"

cd ${FERRY}
#indir = Merged
python CMLF_Prep.py
#outdir = Reformatted
python CombineAll_CMLF.py
#outdir = "/Verify_Converted/All_Sources/CMLF-verify-converted.csv"
echo "Done with CMLF"

cd ${BUOY}
#python ndbc_data_retrieval.py
python Buoy_Prep.py
python CombineAll_NDBC.py
echo "Done with NDBC"

cd ${DDOT}
python DelDOT_Prep.py
python CombineAll_DELDOT.py
echo "Done with DelDOT"

cd ${MESO}
python Mesowest_Prep.py
echo "Done with MESO"

cd ${NCEI}
python ReadData_Convert.py
python NCEI_Prep.py
echo "Done with NCEI"

cd ${NJMET}
python NJMET_Prep.py
python CombineAll_NJMET.py
echo "Done with NJMET"

cd ${VERIFY} 
python CombineAll_data.py
python Quality_Control.py
python Prep_4_r.py
echo "Done with Verification Data"

#UNTESTED
cd ${obsdir}
cp -r ${MDIR}/all_delaware_data_eric_thesis_10m.txt .
cp -r ${MDIR}/all_delaware_data_eric_thesis_OBS.txt .

cd ${seabreeze}
ln -sf ${obsdir}/all_delaware_data_eric_thesis_10m.txt all_delaware_data_eric_thesis_10m.txt
ln -sf ${obsdir}/all_delaware_data_eric_thesis_OBS.txt all_delaware_data_eric_thesis_OBS.txt


