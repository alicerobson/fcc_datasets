#!/usr/bin/env python

import os
import sys
from fcc_datasets.env_versions import EnvVersions
from filename_handler import FilenameHandler
from condor_parameters import CondorParameters, setup_condor_parser
from subprocess import call

''' Start.py is used to setup all files and directories needed for a condor batch run
    #NB You can run this under Mac and it will do everything but not make a condor submission

    Usage: fcc_condor_submit.py  -p parameters_yaml_file -e events -r runs
    
    Example:
    fcc_condor_start.py -p papas_parameters.yaml
    Tutorial:
    #Source init.sh for
    - FCCSW
    - heppy
    - fcc_datasets
    
    #make a directory to contain condor working directories
    mkdir condor_runs
    cd condor_runs
    #create an input parameters file (example in working directoy)
    #simple small test run
    fcc_condor_submit.py -p papas_parameters.yaml
    #bigger run
    fcc_condor_submit.py -p papas_parameters.yaml -e 100 -r 4
    
    Details:
    A subdirectory name will be automatically created based on the run parameters.
    A working subdirectory of this name will be created in the current directory.
    Log/output/error subdirectories needed for condor are created in the working directory.
    The working directory will receive outputs/logs/errors
    from the condor_dag and condor submissions, and can be referred to to uncover any issues.
    Some scipts and submission files are copied into the working directory from $FCCSDATASET/htcondor/base
    Some submission files are written/added to by fcc_condor_submit.py according to run parameters
    
    An output subdirectory of the same name will be created in the base output directory (usually EOS) to hold root and yaml outputs
    
    The run is submitted to condor. This executes run.dag which will execute the individual runs and, when these have completed, a finish.sub which
    creates a final info.yaml summary. When a run is underway an empty start_N.txt file will be created in the output directory.
    This file is removed when the run finishes and is replaced by the output root file. It allows a user to see how much of the job is underway/completed.'''

def setup_condor_directories(subdir, base_outputdir):
    '''Creates a subdirectory in the current directory and in the output directory.
    The subdirectory in the current directory will be used to contain:-
        various scripts such as finish.sh, finish.sub etc
        the dag log and output files
        output/log/error directories used for the condor runs,
    @param: the nameof the subdirectory which will be used to contain the errors and logs etc
    @param: the name of the output directory (base) where a subdir will also be created to hold 
    the outputs.
    '''
    #make the working directory (inside the current directory)
    call(["mkdir", subdir])
    print "made subdirectory " +  subdir 
    #make the log output and error directories needed for condor
    call(["mkdir", subdir+"/log"]) 
    call(["mkdir", subdir+"/output"]) 
    call(["mkdir", subdir+"/error"]) 
    #create a subdirectory in the base output directory
    basedir = ''.join((base_outputdir, subdir))
    print basedir
    call(["mkdir", basedir])
    print basedir
    #copy the files in $FCCDATASETS/htcondor/base/ into the working directory to be used for the condor run
    os.system("cp -R $FCCDATASETS/htcondor/base/* " + subdir)
    os.system("ls " + subdir)
    print "made dirs"

def write_condor_software_yaml(subdir, filename="software.yaml"):
    ''' works out and writes a software.yaml file containing 
    details of software versions
    It uses the env variables to search for software.
    For software on fcc stack the stack path will be used.
    For software with a git version, the git details will be used
    '''
    env_versions =EnvVersions({ 'fccsw': "FCCSWBASEDIR",
                                'fccedm': "FCCEDM",
                                'fccswstack': "FCCSWPATH",
                                'fccphysics': "FCCPHYSICS",
                                'pythia8': "PYTHIA8_DIR",
                                'podio': "PODIO",
                                'fccdag': "FCCDAG",
                                'heppy': "HEPPY",
                                'root': "ROOTSYS",
                                'fccpapas':"FCCPAPASCPP"})
    env_versions.write_yaml('/'.join([subdir,filename]))
    
def setup_condor_dag_files(subdir, events, runs, rate = 100000):
    '''
    writes dag job information to the run.dag file
    @param events: how many events per fcc papas run
    @param runs: how many fcc papas runs
    @param rate: number of events that could (easily) be run in a hour
    '''
    #create a dag file which will list all the jobs needed
    outfile =  subdir + "\/run.dag"
    for c in range(runs):
        os.system('echo Job A{} run.sub >> {} '.format(str(c), outfile))
        os.system('echo Vars A{} runnumber=\\\"{}\\\"  >> {}' .format( str(c) , str(c) , outfile))
    os.system('echo FINAL FO finish.sub >> {}'.format(outfile))
    
    #automatically choose queue based on rate,
    flavour="espresso"  
    if events>8*rate: #
        flavour="tomorrow" # 1 day
    elif events>2*rate:
        flavour="workday" # 8 hours
    elif events>rate:
        flavour="longlunch" # 2 hours
    elif events>rate/3:
        flavour="microcentury"  # 1 hour
    print "job is flavour: " + flavour

    outfile =  subdir + "\/run.sub"
    os.system("cat " + outfile)
    print outfile
    print "echo +JobFlavour = \\\"" + flavour +"\\\" >> " + outfile
    os.system("echo +JobFlavour = \\\"" + flavour +"\\\" >> " + outfile)
    os.system("echo Queue >> " + outfile)


if __name__ == '__main__':
    '''
    Usage: fcc_condor_start.py -p parameters_yaml_file -e events -r runs
    '''
    #read in the command line options
    parser = setup_condor_parser()
    (options,args) = parser.parse_args()
    if len(args) != 0:
        parser.print_usage()
        sys.exit(1)
    os.system('export EOS_MGM_URL="root://eospublic.cern.ch"')

#experiment


    #extract options and create condor_parameters class to hold the run parameters
    #this will also construct a unique subdirectory name
    condor_parameters = CondorParameters(options)
   
    #create work and output directories 
    setup_condor_directories(condor_parameters["subdirectory"], condor_parameters["base_outputdir"])
    #create the dag files needed for the run
    setup_condor_dag_files(condor_parameters["subdirectory"], condor_parameters["events"], condor_parameters["runs"], condor_parameters["rate"])
    #write parameters to working directory
    condor_parameters.write_yaml(condor_parameters["subdirectory"])    
    #write software and paramater yaml files to the output location 
    outputsub= condor_parameters["base_outputdir"] + "/" + condor_parameters["subdirectory"]    
    write_condor_software_yaml(condor_parameters["subdirectory"] )

    # move to the working directory and launch the dag job
    os.chdir(condor_parameters["subdirectory"])
    move_command = 'xrdcp *.yaml {}/{}/'.format(condor_parameters["condor_base_outputdir"], condor_parameters["subdirectory"])
    os.system(move_command)
    #condor_parameters.write_yaml(outputsub)
    print "wrote yaml files to: " + outputsub
    exit=1
    from sys import platform
    print platform
    
    #os.system('env | grep PYTHON')

    print "finished setup"
    #do not remove this final print as it is required by fcc_condor_submit.sh
    print condor_parameters["subdirectory"]
