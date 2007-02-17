# Some common funtions used by Figit.

import sys
import os
import sha
from os.path import join, sep
from fnmatch import fnmatch

def quit(msg="Done"):
    """Clean up and exit."""
    try:
        M.commit()
        channel.client.close()
        V.checkout(DEVBRANCH)
    except: pass
    print msg
    sys.exit(0)

    
def get_message(prompt):
    text = raw_input(prompt)
    text = text.replace('"', '')
    text = text.replace("'", '')
    return text
    

def fixpath(filename, src, wd):
    """
    Returns a three key dictionary of the following strings for filename:
    wp = fully qualified working directory path.
    sp = fully qualified source path (minus "user@hostname:").
    rp = relative path from base of wd or src.
    """
    if filename.startswith(src):
        return {'wp':filename.replace(src, wd), 
                'sp':filename, 
                'rp':filename.replace(src+sep,'')}
    elif filename.startswith(wd):
        return {'wp':filename, 
                'sp':filename.replace(wd,src), 
                'rp':filename.replace(wd+sep,'')}
    else:
        filename = os.path.abspath(filename)
        if filename.startswith(wd):
            return {'wp':filename, 
                    'sp':filename.replace(wd,src), 
                    'rp':filename.replace(wd+sep,'')}
        else:
            raise ('PathError', "%s is not a valid working directory path." 
                   % filename)


def list2string(filelist):
    """
    Converts a list object (presumably containing filenames) to a string 
    for use as a shell command line argument.
    """
    filenamestring = ''
    for f in filelist:
        filenamestring += f + ' '
    return filenamestring.rstrip()  # Chop off very last space.
    
    
def getconf():
    """Read in values from figit config files"""
    # TODO: Add provision for calling from a subdirectory of wd.
    # TODO: Add more error checking.
    confile = open( join(os.getcwd(), ".figit", "config"), 'r' )
    wd_config_line = confile.readline()
    assert wd_config_line.startswith('wd:')
    wd = wd_config_line[3:-1]
    src_config_line = confile.readline()
    assert src_config_line.startswith('src:')
    src = src_config_line[4:-1]
    if src.split(':').__len__() == 2:
        port = 22
    elif src.split(':').__len__() == 3:
        l = src[4:-1].split(':')
        src = l[0] + ':' + l[2]
        port = int(l[1])
    hostlist = []
    hosts = confile.readlines()
    if hosts != []:
        for h in hosts:
            assert h.startswith('host:')
            hostlist.append(h.split(':')[1].rstrip())
    if src.count(':') == 1:
        usersrchost, src = src.split(':')
        user, srchost = usersrchost.split('@')
    else:
        user, srchost = None, None
    hostlist.insert(0, srchost)  # I think Source Host should always be first.
    return {'src':src, 'port':port, 'wd':wd, 'user':user, 'hosts':hostlist}


def wddigest(filename):
    """Return the sha digest of a file in the working directory."""
    fobj = open(filename)
    m = sha.new()
    while True:
        d = fobj.read(8096)
        if not d:
            break
        m.update(d)
    fobj.close()
    return m.hexdigest()
      
        
def wddiff(VCS, IGNORE):
    """
    Compares WD files and INSTALLBRANCH files.
    Returns a list of files, other than figit ignore files, that have changed in
    the WD.
    """
    assert VCS.INSTALLBRANCH != VCS.branch()
    print "Diffing %s and %s" % (VCS.branch(), VCS.INSTALLBRANCH)
    changedfiles = VCS.diff()
    print "CHANGEDFILES: %s" % changedfiles
    cflist = []
    for f in changedfiles:
        cflist.append(f)
        # Remove Figit IGNORE files which should not be distributed.
        for pattern in IGNORE:
            if fnmatch(f, pattern):
                print "Removing %s from change list." % f
                cflist.remove(f)
    return cflist


def remotediff(manifest, src, wd, channel, filenames):
    """
    Compares new sha hashes of the files on the distribution host against the 
    sha hashes in the current manifest. Returns a list of files that have 
    changed on the distribution host.
    """
    changedfiles = []
    for f in filenames:
        fp = fixpath(f, src, wd)
        olddigest = manifest.manifest[fp['rp']][-1]
        try:
            # An IOError here probably means the file doesn't exist.
            channel.sftp.normalize(fp['sp'])
        except IOError:
            continue
        newdigest = channel.digest(fp['sp'])
        if olddigest == newdigest:
            print "Remote copy of %s appears consistent." % fp['rp']
        else:
            changedfiles.append(fp['sp'])
                
    return changedfiles


def get_channel(user, host, port, sudopw):
    """Return the appropriate class depending on the value of host."""
    # TODO: udpate the local.py so that we have a working local channel.
#     if host is None:
#         from Figit.channels import local
#         return local.LocalChannel()
#     else:
#         from Figit.channels import ssh
#         return ssh.SSHChannel(user, host, port, sudopw)
    from Figit.channels import ssh
    return ssh.SSHChannel(user, host, port, sudopw)
    

def get_vcs(vcsname, wd, INSTALLBRANCH):
    """Return the appropriate class depending on what VCSNAME is set to."""
    if vcsname.lower() == 'git': 
        from Figit.vcs import git
        return git.Git(wd, INSTALLBRANCH)
    else:
        # CVS, SVN, BZR....
        pass
