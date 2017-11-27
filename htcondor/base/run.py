#!/usr/bin/env python

import sys
import os
from fcc_datasets.dataset import Dataset
import fcc_datasets.basedir as basedir
from fcc_datasets.htcondor.condor_parameters import CondorParameters
import optparse

''' run.py is called once per run. It launches the fccsw script
    It should be run from a directory in which the condor work files are stored
    It requires that a parameters.yaml file has already been created (by start.py)
    '''

if __name__ == '__main__':
    
    print "start gaudi run"
    
    from optparse import OptionParser
    parser = OptionParser(
                          usage='%prog  job ',
                          description='do a condor run'
                          )
    (options,args) = parser.parse_args()
    
    if len(args) != 1:
        parser.print_usage()
        sys.exit(1)
    
    job=sys.argv[1]

    # read in the run parameters
    condor_pars= CondorParameters("parameters.yaml")
    outdir = '/'.join((condor_pars["base_outputdir"],condor_pars["subdirectory"]))


    filename= outdir + "/start_" +job + ".txt"
    print "started " + filename
    os.system("touch start.txt")
    move_command = 'xrdcp start.txt {}/{}/start_{}.txt'.format( condor_pars["condor_base_outputdir"], condor_pars["subdirectory"], job)
    os.system(move_command)

    #create the gaudi run command from the run parameters
    gaudi_command = eval(condor_pars["gaudi_command"])
    print gaudi_command
    sys.stdout.flush()

    #submit the command
    os.system(gaudi_command)
    
    #move the output files to the output directory
#xrdcp
    os.system("ls -al")
    move_command = 'xrdcp *.root {}/{}/output_{}.root'.format( condor_pars["condor_base_outputdir"], condor_pars["subdirectory"], job)
    print "move files:- ", move_command
    os.system(move_command)
    os.remove(filename)
    
    print "finish gaudi run"
    
