#!/bin/bash
#for example:
#source execute.sh ee_ZZ.txt  simple_papas_condor.py  10 6

#todo add help info on options

#todo make next part a function
#create a new directory for everything in this run and copy base files into it
#find todays date
datestr=$(date +%Y%m%d)
fullfile=$1
filename=$(basename "$fullfile")
extension="${filename##*.}"
filename="${filename%.*}"
subdirectory="condor_"$filename"_"$datestr"_e"$3"_r"$4

#automatically number the directory so it is unique
x=0
maxdirs=100000
while [ $x -lt  $maxdirs ]
do
    echo $subdirectory"_$x"
    if [ -d $subdirectory"_$x" ]; then
        x=$(( $x + 1 ))
    else
        subdirectory=$subdirectory"_$x"
        mkdir $subdirectory
        echo "made subdirectory" $subdirectory
        break
    fi
done
if  [ "$x" -eq "$maxdirs" ]
    then
        echo "Error Too many directories"
fi

#move the scripts needed for the dag job to the subdirectory
cp ../papasdag/base/* $subdirectory
cd $subdirectory

#create a run parameter file
echo "create parameter file:"
echo "maindirectory=\"/eos/experiment/fcc/ee/datasets/papas/\"" > parameters.sh
echo "fccswdirectory=\"/afs/cern.ch/work/a/alrobson/FCCSW/\"" >> parameters.sh
echo "pythiadirectory=\"/afs/cern.ch/work/a/alrobson/papasdag/pythiafiles/\"" >> parameters.sh
echo "scriptsdirectory=\"/afs/cern.ch/work/a/alrobson/papasdag/scripts/\"" >> parameters.sh
echo "subdirectory=\"$subdirectory\"" >> parameters.sh
echo "pythiafile=\"$1\"" >> parameters.sh
echo "script=\"$2\"" >> parameters.sh
echo "nevents=$3" >> parameters.sh
echo "nruns=$4" >> parameters.sh

cat parameters.sh

#create all the jobs needed in dag file
for (( c=0; c<$4; c++ ))
do
echo "Job A$c papas.sub" >> papas.dag
echo "VARS A$c runnumber=\"$c\"" >> papas.dag
done
echo "FINAL FO papasfinish.sub " >> papas.dag

#try to automatically choose queue
flavour="expresso"
rate=100000 #how many per hour
if ((($3)>$((8*$rate))))
    then
        flavour="tomorrow"
elif ((($3)>$((2*$rate))))
    then
        flavour="workday"
elif ((($3)>$rate))
    then
        flavour="longlunch"
elif (($3>$(($rate/3))))
    then
        flavour="microcentury"
fi
echo $flavour

echo "+JobFlavour = \"$flavour\"" >> papas.sub
echo "Queue" >> papas.sub

#create log directories and an eos directory (and eventually a yaml)
source papasstart.sh
#submit the run
condor_submit_dag -update_submit papas.dag
cd ..
