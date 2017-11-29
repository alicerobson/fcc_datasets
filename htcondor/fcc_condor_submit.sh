#!/bin/bash
#Usage: fcc_condor_submit.sh  -p parameters_yaml_file -e events -r runs

#Example:
#fcc_condor_submit.sh -p papas_parameters.yaml

echo "run fcc condor submission script:"
curdir=$PWD
#call python setup and collect the output text
pythonouttext=$(fcc_condor_setup.py $@)
#crude way to pick up the directory name that has been created (last output from python)
directory=$(echo $pythonouttext | awk {'print $NF'})
#move to this directory to submit condor dag
cd $directory
#the condor jobs give an error if we still have FCC python environment set,
#so we unset it, then submit the jobs
#then these paths will be set inside the condor runs
export SAVEDPYTHONHOME=$PYTHONHOME
export SAVEDPYTHONPATH=$PYTHONPATH
unset PYTHONHOME
unset PYTHONPATH
condor_submit_dag -update_submit run.dag
export PYTHONHOME=$SAVEDPYTHONHOME
export PYTHONPATH=$SAVEDPYTHONPATH
#return to original directory
cd $curdir
