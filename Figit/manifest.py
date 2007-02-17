# Class for managing the manifest repository file.

from os import rename
from os.path import join


class Manifest:
    """
    Class for managing the manifest repository file.
    Always pass relative paths to these functions. [see: utils.fixpath()]
    """
    # Since the manifest file is intended as part of the user interface we try 
    # to handle hand editing of it gracefully. 
    # Note that uid and gid, which may be different from machine to machine, 
    # must _not_ be recorded numerically. Names are used instead.
    def __init__(self, wd, init_branch):
        """Initialize a dictionary object with data from the manifest file."""
        self.init_branch = init_branch
        self.wd = wd
        self.manifest = {}
        manifile = open(join(".figit", "manifest"), 'r')
        for line in manifile:
            if line[0] not in (';','#', '"', "'"):  # Ignore comments
                try:
                    filename = line.split()[0]
                    stats = line.split()[1:]
                    self.manifest[filename] = stats
                except IndexError:
                    pass
        manifile.close()
        
    def update(self, filename, stats):  # update is synonymous with add.
        """Add filename to manifest."""
        if type(stats) == type(''):
            self.manifest[filename] = stats.split()
        else:
            self.manifest[filename] = stats
            
    def pop(self, filename):
        """Remove filename from manifest."""
        try:
            self.manifest.pop(filename)
        except KeyError:
            raise KeyError, "%s not found in the manifest." % filename
            
    def commit(self, current_branch):
        """Commit the in-memory manifest dictionary to disk."""
        # Note that if we were not on the same branch we initialized form, 
        # commiting now would really f*ck sh*t up.
        try:
            assert current_branch == self.init_branch 
        except AssertionError:
            print "init_branch = %s \ncurrent_branch = %s" % (self.init_branch,
                                                              current_branch)
        L = self.manifest.keys()
        L.sort()
        # Backup old file. first
        rename(join(".figit", "manifest"), "%s" % join(".figit", "manifest") + ".bak")
        manifile = open(join(".figit", "manifest"), 'w')
        for key in L:
            # Write (filename, ownership, mode, digest)
            manifile.write("%s %s %s %s\n" % (key, self.manifest[key][0], 
                                              self.manifest[key][1], 
                                              self.manifest[key][2]))
        manifile.close()
