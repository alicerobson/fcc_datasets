#!/bin/bash

#the initial condor launch requires use of the condor python (or an error message occurs that says can't import os)
#now we need to point to the correct FCC python
export PYTHONHOME=$SAVEDPYTHONHOME
export PYTHONPATH=$SAVEDPYTHONPATH
#export TERM=linux

echo $HOSTNAME #useful for failed condor jobs.
python run.py $1 #invoke python executable
if [ $? -ne 0 ] ; then
exit 11
fi
