import os
import pprint
import fnmatch
import re
import git
import yaml

########################################################################
class EnvVersions(object):
    """
    Look in specified environment variables to find out which software version was used
    If it has a git repository then record the commit id.
    If not then the directory that it is in
    """

    #----------------------------------------------------------------------
    def __init__(self, to_track_dict):
   
        self.tracked = dict()
        self.environ = os.environ
        for key, envname in to_track_dict.iteritems():
            envval =self._get_env(envname)
            #remove anything in path after install otherwise git repo not found
            if envval:
                envval =envval.split("/install")[0]
                self._analyze(key, envval)

    def _analyze(self, key, envval):
        ''' Find the software version '''
        #set info to be the env path name
        info = envval
        #see if there is a git repository here and if so pick up the commit id
        if self._is_git_repo(envval):        
            repo = git.Repo(envval)
            if not repo.bare:
                info = dict()
                info['commitid'] = repo.head.commit.hexsha  
        self.tracked[key] = info

    def _is_git_repo(self, path):
        '''test to see if this is a git repo'''
        try:
            _ = git.Repo(path).git_dir
            return True
        except git.exc.InvalidGitRepositoryError:
            return False

    def _get_env(self, name):
        ''' check if name is found in the env variables and return'''
        if name in self.environ:
            return self.environ[name]
        return None

    #----------------------------------------------------------------------
    def write_yaml(self, path):
        '''write the versions to a yaml file'''
        data = dict(software=dict())
        # write out either the directory or the git commit if this was found
        for package, info in self.tracked.iteritems():
            if isinstance(info, dict) and 'commitid' in info:
                data['software'][package] = info['commitid']
            else:
                data['software'][package] = info
        with open(path, mode='w') as outfile:
                yaml.dump(data, outfile,
                          default_flow_style=False)    

    def __str__(self):
        return pprint.pformat(self.tracked)
