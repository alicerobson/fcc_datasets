#!/bin/bash
export PATH=$PWD/scripts:$PATH
export FCCDATASETS=$PWD
export PATH=$FCCDATASETS:$PATH
export PATH=$FCCDATASETS/htcondor:$PATH
export PYTHONPATH=$FCCDATASETS:$PYTHONPATH
export EOS_MGM_URL=root://eospublic.cern.ch
