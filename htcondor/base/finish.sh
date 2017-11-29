#!/bin/bash

#the initial condor launch requires use of the condor python (or an error message occurs that says can't import os)
#now we need to point to the correct FCC python
export PYTHONHOME=$SAVEDPYTHONHOME
export PYTHONPATH=$SAVEDPYTHONPATH

echo $HOSTNAME #useful for failed condor jobs.
python finish.py  #invoke python executable
