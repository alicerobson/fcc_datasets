Batch submission scripts for Condor
==================================

## Contents:

* [Overview](#overview)
* [Introduction](#introduction)
* [Installation Procedure](#installation-procedure)
* [Example](#example)
* [Papas Algorithm in FCCSW](#papas-algorithm-in-fccsw)
* [Running Papas in FCCSW](#running-papas-in-fccsw)
* [Papas Detectors](#papas-detectors)
* [Running PAPAS under htcondor](#running-papas-under- htcondor)
* [Work not yet done](#work-not-yet-done)


## Overview

The submission scripts described here support the generation of large sample sets using the FCCSW software on the CERN htcondor machines.

## Introduction

Fcc_datasets is a python repository that has been created to support large fcc datasets. TODO Link to further documentation by Colin.

The scripts described here support the generation of large samples for FCC. Note that Heppy already supports batch submission of python scripts to generate large event samples on lxbatch (and the subsequent analysis of the generated root files). Sample generation via FCCSW and htcondor allows larger sample sets to be produced more quickly. The outputs are designed to be ready for heppy analyses.

In order to generate a large number of events, a group of root output files is created via batch. The fcc_condor_submit.sh call a python script to set up directories and files it then creates a condor DAG submission. The DAG submission allows multiple runs to be easily executed on htcondor. Each individual run produces an output root file. Once all individual runs are complete, a final script is executed. This creates a summary file (info.yaml) documenting run details and the output root files.

Usage: fcc_condor_submit.sh -p input_parameters.yaml


## Installation Procedure

You will need to install

(1) FCCSW
(2) heppy (to discuss with Colin)
(3) fcc_datasets.

Before using fcc_datasets remember to run

cd FCCSW_directory_name
source init.sh
cd FCC_datasets_directory_name
source init.sh

## Example

First make a directory which will contain the condor working directories

mkdir condor_runs
cd condor_runs

Now create an input parameters file in the working directory. For example, copy
$FCCDATASETS/htcondor/examples/papas/papas_parameters.yaml. Check that the locations of the directories are correct and amend if needed. Make sure you have permissions to write to the base_output_dir (eg eos directory)

Note that the condor_base.... needs to be set

Then submit the run eg

fcc_condor_submit.py -p papas_parameters.yaml

or adjust the number of events or the number of runs

fcc_condor_submit.py -p papas_parameters.yaml -e 100 -r 4

##  Details

A unique subdirectory name will be automatically created based on the run parameters.This subdirectory will be created in the current working directory and also in the outputs directory.

Log/output/error subdirectories needed for condor are created in the working directory. These will receive outputs/logs/errors from the condor_dag and condor submissions, and can be referred to to uncover any issues.

Some scripts and submission files are copied into the working directory from $FCCSDATASET/htcondor/base. Some submission files are written/added to by fcc_condor_submit.py according to run parameters, for example see dag.sub and run.sub.

The run is automatically submitted to condor. This executes run.dag which will in turn submit the individual runs. When a run is underway an empty started_N.txt file will be created in the output directory. This file is removed when the run finishes and is replaced by the output root file. It allows a user to see how much of the job is underway/completed. When all the runs have completed (successfully or failed) a finish.sub executes which creates a final info.yaml summary
