
#import os
from fcc_datasets.env_versions import EnvVersions


if __name__ == '__main__':
    
    #import sys
    #import os
    from optparse import OptionParser
    
    parser = OptionParser(
        usage='%prog  [options]',
        description='publish software versions'
    )
    parser.add_option(
        "-b","--basedir", dest="basedir",
        default=".",
        help="base directory containing all samples."
    )
    (options,args) = parser.parse_args()
    
    if len(args) != 0:
        parser.print_usage()
        sys.exit(1)

    basedir = options.basedir
    env_versions =EnvVersions({ 'fccsw': "FCCSWBASEDIR",
                               'fccedm': "FCCEDM",
                               'fccswstack': "FCCSWPATH",
                               'fccphysics': "FCCPHYSICS",
                               'pythia8': "PYTHIA8_DIR",
                               'podio': "PODIO",
                               'fccdag': "FCCDAG",
                               'junk': 'FCCJUNK',
                               'root': 'ROOTSYS',
                               'fccpapas':'FCCPAPASCPP'})
    #print env_versions
    fname = 'software.yaml'
    print '/'.join([basedir,fname])
    env_versions.write_yaml('/'.join([basedir,fname]))
    print "finished creation of software.yaml"
