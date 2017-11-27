#!/usr/bin/env python
import sys
import os
from fcc_datasets.dataset import Dataset
import fcc_datasets.basedir as basedir
from fcc_datasets.htcondor.condor_parameters import CondorParameters
import optparse 

'''Finish.py produces a summary output yaml file which will contain details of the root files in the output directory and will
amalgamate all other yaml files'''

if __name__ == '__main__':
    
    
    #read in the condor parameters from parameters.yaml so that we know the location of the output directory
    condor_pars= CondorParameters("parameters.yaml")
    
    curdir = os.getcwd()
    os.system('export EOS_MGM_URL=root://eospublic.cern.ch')
    
    #move to the base output directory
    os.chdir(condor_pars["base_outputdir"])
    
    os.system("touch " + condor_pars["subdirectory"]+"/finish.txt")
    
    '''base directory where outputs are stored'''
    basedir.set_basename(condor_pars["base_outputdir"])
    ds = Dataset(condor_pars["subdirectory"],
                     pattern="*.root",
                     xsection=None,
                     extract_info=True,
                     cache=False)
    ds.write()
    
    os.system("ls -al " +  condor_pars["base_outputdir"] + "/" +condor_pars["subdirectory"])
    #put a copy of info.yaml in the work directory for easy reference
    os.system("xrdcp " + condor_pars["subdirectory"] +"/info.yaml " + curdir  )
    os.system("ls -al " +  condor_pars["base_outputdir"] + "/" +condor_pars["subdirectory"])
    #remove the touch file
    os.system("rm " + condor_pars["subdirectory"]+"/finish.txt")
    
    #move back to the original directory
    os.chdir(curdir)
    print "finished creation of info.yaml"
