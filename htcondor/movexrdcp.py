import os
os.system('export EOS_MGM_URL=root://eospublic.cern.ch')

def move_xrdcp(command, nfails=10):
    print "moving file with: " + command
    for i in range(nfails):
        if i>0:
            print 'retry moving file attempt: ', i, ' : ' , command
        success = os.system(command)
        if success==0:
            print "successfully moved file with: " + command
            break

