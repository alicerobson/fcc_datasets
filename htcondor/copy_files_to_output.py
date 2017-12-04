import os


def move_xrdcp(command, nfails=10):
    print "moving file with: " + command
    for i in range(nfails):
        if i>0:
            print 'retry moving file attempt: ', i, ' : ' , command
        success = os.system(command)
        if success==0:
            print "successfully moved file with: " + command
            break

def copy_files_to_output(infile, outfile, eos_base=None):
    if eos_base:
        #xrdcp is more direct for EOS
        move_xrdcp('xrdcp  {} {}/{}'.format( infile, eos_base, outfile))
    else:
        #for local stuff move directly
        os.system('cp  {} {}'.format( infile, outfile))

