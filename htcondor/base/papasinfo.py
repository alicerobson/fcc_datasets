import sys
from fcc_datasets.dataset import Dataset
import fcc_datasets.basedir as basedir


def process_dataset(dsname, options):
    '''Process the directory containing output files and write summary information to info.yaml'''
    ds = Dataset(dsname,
                 pattern=options.wildcard,
                 xsection=options.xsection, 
                 cache=False)
    ds.write_yaml()


if __name__ == '__main__':

    from optparse import OptionParser
    #import fcc_datasets
    
    parser = OptionParser(
        usage='%prog <dataset_name> [options]',
        description='publish a dataset'
    )
    parser.add_option(
        "-b","--basedir", dest="basedir",
        default=basedir.basename,
        help="base directory containing all samples."
    )
    parser.add_option(
        "-w","--wildcard", dest="wildcard",
        default="*.root",
        help="wildcard to select files in the dataset"
    )
    parser.add_option(
        "-x","--xsection", dest="xsection", type=float, 
        default=None,
        help="cross section to be assigned to the sample."
    )
    (options,args) = parser.parse_args()
    
    if len(args) != 1:
        parser.print_usage()
        sys.exit(1)
        
    dsname = sys.argv[1]
    '''base directory where outputs are stored'''
    basedir.basename = options.basedir
    process_dataset(dsname, options)
    print "finished creation of info.yaml"
