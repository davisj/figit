# Git VCS wrapper/backend for FIgit.

import os
from commands import getoutput as go
from os.path import join, sep        
        
class Git:

    def __init__(self, wd, INSTALLBRANCH):
        self.ignorefile = '.gitignore'
        self.ignore_patterns = ['*~', '*.pyc', 'manifest.bak'] 
        self.wd = wd
        self.installdir = wd        
        self.INSTALLBRANCH = INSTALLBRANCH
        self._init_branch = self.branch()
        assert self._init_branch != INSTALLBRANCH

    def initdb(self):
        """Initialize a vcs working directory."""
        out = go('git init-db')  + '\n'
        vcsignorefile = open(self.ignorefile, 'w')
        for pattern in self.ignore_patterns:
            vcsignorefile.write("%s\n" % pattern)
        vcsignorefile.close()
        out += go('git add .')
        out += go("git commit -a -m 'figit: Initial commit.'")
        out += go('git branch %s' % self.INSTALLBRANCH)
        return out
        
    def branch(self, branchname=None):
        """Create a new branch or report the current branch name."""
        if branchname is None:  # Just report the current branch name.
            try:          
                return open(join(".git", "HEAD")).read().split(sep)[-1].strip()
            except IOError:
                return None
        else:  # Create the named branch.
            return go('git branch %s' % branchname)
            
    def checkout(self, branchname):
        """Switch working directory to branchname."""
        return go('git checkout %s' % branchname)
        
    def add(self, files):
        """Add new files to the INSTALLBRANCH"""     
        try:
            br = self.branch()
            assert br == self.INSTALLBRANCH
        except AssertionError:
            self.checkout(self.INSTALLBRANCH)
        return go("git add %s" % files)

    def remove(self, files):
        """Remove files from the repository."""
        self.checkout(self.INSTALLBRANCH)
        out = go("git rm -f %s" % files)
        out += go("git commit -m 'figit: deleted %s'" % files)
        self.checkout(self._init_branch)
        out += self.merge("figit: merging deletion of %s" % files,
                          self._init_branch, self.INSTALLBRANCH)
        return out
        
    def diff(self):
        """Return one filename per line. Ignore Added files."""
        return go('git diff --name-only --diff-filter=MRC %s' 
                  % self.INSTALLBRANCH).split()

    def merge(self, message, to_branch, from_branch):
        self.checkout(to_branch)
        out = go('git merge "%s" %s %s' 
                  % (message, to_branch, from_branch))
        if self.branch() != self._init_branch:
            self.checkout(self._init_branch)
        return out
        
    def commit(self, message, files):
        return go("git commit -m '%s' %s" % (message, files))
        
    def commitall(self, message):
        return go("git commit -a -m '%s'" % message)
