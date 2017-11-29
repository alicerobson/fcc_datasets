#!/bin/bash
#Usage: fcc_condor_submit.py  -p parameters_yaml_file -e events -r runs

#Example:
#fcc_condor_submit.py -p papas_parameters.yaml


echo "run fcc condor submission script"
#make sure environment variables are set
#TODO discuss best way with Colin
export "PYTHONHOME=/cvmfs/sft.cern.ch/lcg/releases/Python/2.7.13-597a5/x86_64-slc6-gcc62-opt"
export "PYTHONPATH=/afs/cern.ch/work/a/alrobson/fcc_datasets:/cvmfs/fcc.cern.ch/sw/0.8.1/podio/0.7/x86_64-slc6-gcc62-opt/python:/cvmfs/sft.cern.ch/lcg/releases/LCG_88/DD4hep/00-20/x86_64-slc6-gcc62-opt/python:/cvmfs/sft.cern.ch/lcg/releases/ROOT/6.08.06-c8fb4/x86_64-slc6-gcc62-opt/lib:/cvmfs/sft.cern.ch/lcg/views/LCG_88/x86_64-slc6-gcc62-opt/lib:/cvmfs/sft.cern.ch/lcg/views/LCG_88/x86_64-slc6-gcc62-opt/lib/python2.7/site-packages:/cvmfs/sft.cern.ch/lcg/views/LCG_88/x86_64-slc6-gcc62-opt/lib/python2.6/site-packages:$FCCDATASETS:$FCCDATASETS/..:$FCCDATASETS/htcondor:"

echo $@
curdir=$PWD
pythonouttext=$(fcc_condor_setup.py $@)
#crude way to pick up the directory name that has been created (last output from python)
directory=$(echo $pythonouttext | awk {'print $NF'})
#move to directory to submit condor dag
cd $directory
#the condor jobs give an error if we still have FCC python environment set, so we unset it, then submit the jobs
#then these paths will be set inside the condor runs
SAVEDPYTHONHOME=$PYTHONHOME
SAVEDPYTHONPATH=$PYTHONPATH
unset PYTHONHOME
unset PYTHONPATH
condor_submit_dag -update_submit run.dag
cd $curdir

export PYTHONHOME=$SAVEDPYTHONHOME
export PYTHONPATH=$SAVEDPYTHONPATH
export SAVEDPYTHONHOME=$SAVEDPYTHONHOME
export SAVEDPYTHONPATH=$SAVEDPYTHONPATH
