#!/usr/bin/env python
# Copyright (C) 2007 Jake Davis <mrsalty0@gmail.com>
#
# This file is part of figit.
#
# Figit is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Figit is distrubuted in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Figit; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.

############################################################################
###############Some user editable variables ################################

VCSNAME = 'git'  # Version control backend to be used.
INSTALLBRANCH = 'install'  # Name of vcs branch which mirrors production.

# IGNORE's are gnored by Figit but may be tracked by the VCS.
IGNORE = ['.figit*','.git*', '.cvs*', '.svn*', '.bzr*']

############################################################################
############################################################################

"""
figit aims to provide:
Config file version control and ssh distribution for the impatient.
"""

import os
import sys
import sha
import getpass
from commands import getoutput as go
from os.path import join
from Figit import utils, manifest, channels, vcs, run

### You shouldn't have to touch anything below this line. ###

USAGE = """
Usage: figit COMMAND [ ARGS ]

ARGS:
    [WD]:    The path to the VCS working directory.
    [SRC]:   The host filesystem directory you want to manage
    [FILES]: The paths to one or more filenames seperated by spaces
    
COMMANDS with relevant ARGS:
    init        Create managed copy of [SRC] at [WD]
    get         Add/Update/Commit contents and meta data for [FILE] to the VCS
    remove      Purge [FILES] and associated meta data from the VCS
    ls          List content of [SRC] directory
    install     Apply all changes in the working directory to all hosts.
    run         Run an arbitrary command on all distribution Hosts.
    
"""  


if __name__=='__main__':
    try:
        args = sys.argv[1:]
        cmmd = args[0]
    except IndexError:
        print USAGE
        sys.exit(1)
            
    if cmmd == 'init':
        """Initialize the Figit working directory."""
        # TODO: test if src directory exists. For now we assume it does.
        wd = os.path.abspath(args[2])
        src = args[1]
        if src.count(':') < 1:
            utils.quit(USAGE)
        if os.path.abspath(src) == wd:
            utils.quit("Working directory and source cannot be the same.")           
        if not os.path.exists(join(wd, '.figit')):
            os.makedirs(join(wd, '.figit'))
        os.chdir(wd)
        confile = open(join(".figit", "config"), 'w')
        confile.write( "wd:%s\nsrc:%s\n" % (os.getcwd(), src) )
        confile.close()
        for node in ("manifest", "RunBefore", "RunAfter"):
            os.mknod(join(".figit", node))
        VCS = utils.get_vcs(VCSNAME, wd, INSTALLBRANCH)        
        print VCS.initdb()
        utils.quit()
    
    conf = utils.getconf()
    src = conf['src']
    port = conf['port']
    wd = conf['wd']
    user = conf['user']
    hosts = conf['hosts']
    
    os.chdir(wd)
    
    if cmmd == 'addhost':
        """Append a new distribution host's name to the config file."""
        import socket
        hostnames =  args[1:]
        confile = open( join(wd, ".figit", "config"), 'a' )
        for h in hostnames:
            if h in hosts:
                print "Host %s already tracked..." % h
                continue
            try:
                socket.getaddrinfo(h, None)
                confile.write("host:%s\n" % h)
            except socket.gaierror:
                print "Coudn't resolve host address: %s" % h
        confile.close()
        utils.quit()
    
    if cmmd == 'remove':
        """Removes file and meta data from the repository."""
        # note that remove does not effect distribution hosts          
        VCS = utils.get_vcs(VCSNAME, wd, INSTALLBRANCH)
        M = manifest.Manifest(wd, VCS.branch())
        raw_names = args[1:]
        fixed_names = []
        for f in raw_names:
            rp = utils.fixpath(f, src, wd)['rp']
            M.pop(rp)
            print "Removing file %s" % rp
            fixed_names.append(rp)
        print "removing %s" % utils.list2string(fixed_names)
        VCS.remove(utils.list2string(fixed_names))
        M.commit(VCS.branch())
        utils.quit()


    # The rest of these funtions may or may not require a sudo password.
    # It would be nice to know ahead of time so we could skip this if not.
    sudopw = getpass.getpass("Enter sudo password for %s: " % user)
                
                
    if cmmd == 'get':
        """
        Copy files from the Source Host into the INSTALLBRANCH 
        and update the manisfest.
        """
        # If the file currently resides in wd it will be overwritten.
        # 1. Switch to INSTALLBRANCH
        # 2. Create directories / download files / update manifest 
        # 3. add / commit new files to vcs INSTALLBRANCH
        # 4. switch back to _init_branch and merge in new files from install
        
        channel = utils.get_channel(user, hosts[0], port, sudopw)
        VCS = utils.get_vcs(VCSNAME, wd, INSTALLBRANCH)
        _init_branch = VCS.branch()
        assert _init_branch != INSTALLBRANCH
        VCS.checkout(INSTALLBRANCH)
        M = manifest.Manifest(wd, VCS.branch())
        filenames = args[1:]
        # We remove directories from the list to avoid potential commit errors.
        nondirectories = []
        for f in filenames:
            fp = utils.fixpath(f, src, wd)
            if not os.path.exists(os.path.dirname(fp['wp'])):
                os.makedirs(os.path.dirname(fp['wp']))
            uid, gid, mode, filetype, digest = channel.stats(fp['sp'])
            print "%s %s:%s %s %s" % (fp['rp'], uid, gid, mode, digest)
            if filetype.startswith('directory'):
                print "** Creating directory: %s **" % os.path.dirname(fp['wp'])
                os.mkdir(fp['wp'])  # Directories are created not copied.
            else:
                nondirectories.append(fp['rp'])
                channel.get(fp['sp'], fp['wp'])
            M.update( fp['rp'], "%s:%s %s %s" % (uid,gid,mode,digest) )
            print "** Writing manifest entry **" 
            print "** Adding file to '%s' **" % INSTALLBRANCH
            VCS.add(fp['rp'])
        print "** Writing manifest changes to disk **"
        M.commit(VCS.branch())
        commitfiles = utils.list2string(nondirectories)
        print "** Commiting new files to '%s' **" % INSTALLBRANCH
        VCS.commit("figit: Added %s" % commitfiles, commitfiles)
        VCS.checkout(_init_branch)
        print "** Merging %s to '%s' from '%s' **" % (commitfiles, _init_branch, 
                                                  INSTALLBRANCH)
        VCS.merge("figit: Merging added files %s to %s from %s" 
                % (commitfiles, _init_branch, INSTALLBRANCH),
                _init_branch, INSTALLBRANCH)
        
    elif cmmd == 'ls':
        channel = utils.get_channel(user, hosts[0], port, sudopw)
        try:
            dirpath = args[1]
        except IndexError:
            dirpath = src
        directory = utils.fixpath(dirpath, src, wd)['sp']
        print "Directory: %s" % directory
        for f in channel.ls(directory):
            print f

    elif cmmd == 'install':
        # 1. Diff the WD (_init_branch) and INSTALLBRANCH to determine changes.
        #    read in Manifest values to create an uploadlist dictionary.
        # 2. Connect to each host and check to see if the hashes have changed.
        #    If so, rename each file before uploading it. If not, just upload.
        # 3. Update _init_branch manifest with new hashes.
        # 4. Commit to _init_branch all the updates we just installed.
        # 5. Merge changes from _init_branch to INSTALLBRANCH.
          
        VCS = utils.get_vcs(VCSNAME, wd, INSTALLBRANCH)
        _init_branch = VCS.branch()
        assert _init_branch != INSTALLBRANCH
        M = manifest.Manifest(wd, VCS.branch()) 
        wdchanges = utils.wddiff(VCS, IGNORE)
        uploadlist = {}
        if wdchanges != []:
            for f in wdchanges:  # read in old stats for changed files.
                print "Changed since last install: %s" % f
                uploadlist[f] = M.manifest[ utils.fixpath(f,src,wd)['rp'] ]
            proceed = raw_input("Would you like to upload these changed " +
                                "files now? %s \n[y/N]: " 
                                 % utils.list2string(wdchanges))
            if proceed[0].lower() != 'y':
                utils.quit("Installation Aborted...")
            RunBefore = run.Run('RunBefore')
            RunAfter = run.Run('RunAfter')
            for h in hosts:  # Get a new channel and upload changes for each.
                channel = utils.get_channel(user, h, port, sudopw)
                remotechanges = utils.remotediff(M, src, wd, channel, wdchanges)
                if remotechanges != []:
                    for f in remotechanges:  # f should be in format fp['sp']
                        print "Trying to rename %s" % f
                        try:
                            channel.rename(f)  # Backup file on remote end.
                        except 'PermissionError':
                            print "Couldn't backup file %s" % f
                print "Uploading changes to %s." % h
                for f in uploadlist:
                    fp = utils.fixpath(f,src,wd)
                    ownership, mode, olddigest = uploadlist[f]
                    if fp['rp'] in RunBefore.keys():
                        channel.run(RunBefore[fp['rp']])
                    try:                        
                        channel.put(fp['wp'], fp['sp'], ownership, mode)
                    except 'PermissionError':
                        print "Couldn't change mode on %s" % fp['sp']
                    if fp['rp'] in RunAfter.keys():
                        channel.run(RunAfter[fp['rp']])
            for f in wdchanges:  # write new digests
                fp = utils.fixpath(f,src,wd)
                M.manifest[ fp['rp'] ][-1] = utils.wddigest( fp['wp'] )
            M.commit(VCS.branch())
            commit_msg = utils.get_message("Please supply a commit message: ")
            VCS.commitall(commit_msg)
            print "Merging to '%s' from '%s'" % (INSTALLBRANCH, _init_branch)
            VCS.merge("figit: Merging changed files " +
                      "%s to %s from %s for install operation."
                      % (utils.list2string(wdchanges), 
                      INSTALLBRANCH, _init_branch), 
                      INSTALLBRANCH, _init_branch)         
        else:
            print "No changes to upload"
    
    elif cmmd == 'run':
        """Run an arbatrary command on all Distribution Hosts."""
        try:
            command = utils.list2string(args[1:])
        except:
            utils.quit(USAGE)
        channel = utils.get_channel(user, hosts[0], port, sudopw)
        for line in channel.run(command):
            print line.strip()
        utils.quit()
        
    elif cmmd == 'shell':
        """Open an interactive shell on each consecutive distribution host."""
        raise "NotImplimentedError", "Sorry, shell is not yet implimented."
        
    else:
        utils.quit(USAGE)
