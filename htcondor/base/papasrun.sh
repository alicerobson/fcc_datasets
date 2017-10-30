#!/bin/bash
#The file moves necessary file to condor machine, runs the job and puts outputs in the maindirectory (eos)

source parameters.sh
ls -al
#create a file to mark that a job has started, useful to see what is running at the moment/unfinished
touch $maindirectory/$subdirectory/papas$1_$2.txt
export outputfilename=papasout.root

echo "copy across fccsw script"
cp $scriptsdirectory/$script .
echo "copy across pythia file"
ls $pythiadirectory
cp $pythiadirectory/$pythiafile .

#job details
echo "run"
echo "cluster: " $1
echo "job: " $2
echo "pythiafile: " $pythiafile
echo "script: " $script
echo "maxevents: " $nevents

echo "files before run starts" #(useful for debugging)
ls -al

#run papas
LD_PRELOAD=$fccswdirectory/build.$BINARY_TAG/lib/libPapasUtils.so $fccswdirectory/run fccrun.py $script --rpythiainput  $pythiafile --routput $outputfilename  --rmaxevents $nevents 2> /dev/null

if [ $? -eq 0 ]
then
    echo "Successfully ran fcc gaudi papas"
    echo "files after run finishes" #useful for debugging
    ls -al

    #echo $directory
    if [ ! -d $directory ]; then
        echo make $directory
        mkdir $directory
    fi
    echo "copy" xrdcp $outputfilename $maindirectory/$subdirectory/${outputfilename%.*}_$2.${outputfilename##*.}
    xrdcp $outputfilename $maindirectory/$subdirectory/${outputfilename%.*}_$2.${outputfilename##*.}

    echo "Cleaning"
    #remove the text file for the job
    rm $maindirectory/$subdirectory/papas*_$2.txt
    exit 0

else
    echo "Gaudi run failed" >&2
    rm $maindirectory/$subdirectory/papas*_$2.txt
    touch $maindirectory/$subdirectory/papasfailure$1_$2.txt
    exit 1
fi
