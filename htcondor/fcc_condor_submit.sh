#!/bin/bash
echo "run condor script"
export "PYTHONHOME=/cvmfs/sft.cern.ch/lcg/releases/Python/2.7.13-597a5/x86_64-slc6-gcc62-opt"
export "PYTHONPATH=/afs/cern.ch/work/a/alrobson/fcc_datasets:/cvmfs/fcc.cern.ch/sw/0.8.1/podio/0.7/x86_64-slc6-gcc62-opt/python:/cvmfs/sft.cern.ch/lcg/releases/LCG_88/DD4hep/00-20/x86_64-slc6-gcc62-opt/python:/cvmfs/sft.cern.ch/lcg/releases/ROOT/6.08.06-c8fb4/x86_64-slc6-gcc62-opt/lib:/cvmfs/sft.cern.ch/lcg/views/LCG_88/x86_64-slc6-gcc62-opt/lib:/cvmfs/sft.cern.ch/lcg/views/LCG_88/x86_64-slc6-gcc62-opt/lib/python2.7/site-packages:/cvmfs/sft.cern.ch/lcg/views/LCG_88/x86_64-slc6-gcc62-opt/lib/python2.6/site-packages::/afs/cern.ch/work/a/alrobson/fcc_datasets:/afs/cern.ch/work/a/alrobson:/afs/cern.ch/work/a/alrobson/fcc_datasets/htcondor:"

echo $@
curdir=$PWD
pythonouttext=$(fcc_condor_setup.py $@)
#crude way to pick up the directory name that has been created (last output from python)
directory=$(echo $pythonouttext | awk {'print $NF'})
#move to directory to submit condor dag
cd $directory
unset PYTHONHOME
unset PYTHONPATH
condor_submit_dag -update_submit run.dag
cd $curdir

