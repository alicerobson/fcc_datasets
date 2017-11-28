#!/bin/bash

#export the python libs
export PYTHONHOME=/cvmfs/sft.cern.ch/lcg/releases/Python/2.7.13-597a5/x86_64-slc6-gcc62-opt
export PYTHONPATH=/cvmfs/fcc.cern.ch/sw/0.8.1/podio/0.7/x86_64-slc6-gcc62-opt/python:/cvmfs/sft.cern.ch/lcg/releases/LCG_88/DD4hep/00-20/x86_64-slc6-gcc62-opt/python:/cvmfs/sft.cern.ch/lcg/releases/ROOT/6.08.06-c8fb4/x86_64-slc6-gcc62-opt/lib:/cvmfs/sft.cern.ch/lcg/views/LCG_88/x86_64-slc6-gcc62-opt/lib:/cvmfs/sft.cern.ch/lcg/views/LCG_88/x86_64-slc6-gcc62-opt/lib/python2.7/site-packages:/cvmfs/sft.cern.ch/lcg/views/LCG_88/x86_64-slc6-gcc62-opt/lib/python2.6/site-packages:$FCCDATASETS:$WORK

echo $HOSTNAME
echo $PYTHONHOME
echo $PYTHONPATH
python run.py $1 #invoke your python executable
