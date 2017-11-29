#!/bin/bash
#the initial condor launch requires use of the condor python (or an error message occurs that say can't import os)
#once the condor job starts we can point to the correct FCC python

#TODO check with colin about dealing with $FCCDATASETS

#export the python libs
export EOS_MGM_URL="root://eospublic.cern.ch"
export PYTHONHOME=/cvmfs/sft.cern.ch/lcg/releases/Python/2.7.13-597a5/x86_64-slc6-gcc62-opt
export PYTHONPATH=/afs/cern.ch/work/a/alrobson/fcc_datasets:/cvmfs/fcc.cern.ch/sw/0.8.1/podio/0.7/x86_64-slc6-gcc62-opt/python:/cvmfs/sft.cern.ch/lcg/releases/LCG_88/DD4hep/00-20/x86_64-slc6-gcc62-opt/python:/cvmfs/sft.cern.ch/lcg/releases/ROOT/6.08.06-c8fb4/x86_64-slc6-gcc62-opt/lib:/cvmfs/sft.cern.ch/lcg/views/LCG_88/x86_64-slc6-gcc62-opt/lib:/cvmfs/sft.cern.ch/lcg/views/LCG_88/x86_64-slc6-gcc62-opt/lib/python2.7/site-packages:/cvmfs/sft.cern.ch/lcg/views/LCG_88/x86_64-slc6-gcc62-opt/lib/python2.6/site-packages:$FCCDATASETS:$FCCDATASETS/..:
echo $HOSTNAME #useful for failed condor jobs.
python finish.py  #invoke python executable
