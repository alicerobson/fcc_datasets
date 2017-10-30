#!/usr/bin/env bash
#set up directories needed by condor plus an output directory to store outputs on eos
#create initial software.yaml
source ./parameters.sh
mkdir $maindirectory/$subdirectory
mkdir log
mkdir error
mkdir output
curdir=$PWD
cd $fccswdirectory
source init.sh
cd $curdir
echo "move parameters.sh to output directory"
xrdcp parameters.sh $maindirectory/$subdirectory/
echo "create software yaml"
python papassoftware.py -b $maindirectory/$subdirectory/


