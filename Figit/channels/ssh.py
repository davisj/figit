# SSH remote filesystem access channel for Figit.

import os
import sha
import getpass
from paramiko import SSHClient, SSHException
from paramiko.util import log_to_file, load_host_keys

class SSHChannel:
    """
    A Class with functions for examining and manipulating a source directory 
    that resides on a remote system.
    """
    # Until someone thinks of a better way, we'll brute force permissions
    # using sudo whenever the first write attempt fails.
    def __init__(self, user, host, port, sudopw):
        log_to_file('/var/tmp/figit-ssh.log')  # TODO: make this os agnostic.
        self.port = int(port)
        self.sudopw = sudopw
        self.client = SSHClient()
        self.client.load_system_host_keys()
        try:  # 1st try an ssh key
            self.client.connect(host, port, user)
            # Versions of paramiko prior to 1.7 fail here. If you have v1.6.4 
            # or earlier, specifying key_filename should fix the problem.
            # key_filename=os.path.expanduser('~/.ssh/id_rsa')
        except SSHException:
            try:  # next try the sudo password
                password = sudopw
                self.client.connect(host, port, user, password)
            except SSHException:  # finally ask the user for a password.
                password = getpass.getpass("Enter ssh password for %s: " % user)
                self.client.connect(host, port, user, password)
        self.sftp = self.client.open_sftp()

    def run(self, command):
        """Run a command on the remote host."""
        stdin, stdout, stderr =  self.client.exec_command(command)
        errors = stderr.readlines()
        out = stdout.readlines()
        stdin.close()
        stdout.close()
        stderr.close()
        if errors != []:
            return errors
        else:
            return out

    def ls(self, rpath):
        return self.sftp.listdir(rpath)

    def digest(self, rpath):
        """Returns a sha1 hash of the file content of remote path."""
        try:
            fobj = self.sftp.open(rpath)
            chmodded = False
        except IOError:
            # Force world readableness
            self.run("echo %s | sudo chmod o+r %s" % (self.sudopw, rpath))
            chmodded = True
            fobj = self.sftp.open(rpath)
        m = sha.new()
        while True:
            d = fobj.read(8096)
            if not d:
                break
            m.update(d)
        fobj.close()
        if chmodded == True:
            # Undo world readableness
            self.run("echo %s | sudo chmod o-r %s" % (self.sudopw, rpath)) 
        return m.hexdigest()
        
    def stats(self, rpath):
        """Returns (uid, gid, mode, filetype, sha1hash) for rpath."""
        newdigest = self.digest(rpath)
        stdin, stdout, stderr =  self.client.exec_command(
                                 """stat -c %U:%G:%a:%F """ + rpath)
        uid, gid, mode, filetype = stdout.read().split(':')
        stdin.close()
        stdout.close()
        stderr.close()
        # The stat shell command often returns a three digit mode, e.g. "644"
        # so zfill is used to pad the result with leading zeros, e.g. "0644".
        return (uid, gid, mode.zfill(4), filetype.strip(), newdigest)
  
    def chmod(self, rpath, ownership, mode):
        """Set file ownership and permissions mode on remote path"""
        out = self.run("echo %s | sudo chown %s %s" 
                       % (self.sudopw, ownership, rpath))
        out +=  self.run("echo %s | sudo chmod %s %s" 
                         % (self.sudopw, mode, rpath))
        return out
        
    def get(self, rpath, localpath):
        """download a file"""
        try:
            self.sftp.get(rpath, localpath)
        except IOError:
            # Force world readableness
            out = self.run("echo %s | sudo chmod o+r %s" % (self.sudopw, rpath)) 
            self.sftp.get(rpath, localpath)
            # Undo world readableness
            out = self.run("echo %s | sudo chmod o-r %s" % (self.sudopw, rpath))
        
    def put(self, localpath, rpath, ownership, mode):
        """Upload a file to the remote host."""
        try:  # make sure the file exists
            self.sftp.normalize(rpath)
        except IOError:
            try:  # make sure the directory exists before creating file.
                self.sftp.normalize(os.path.dirname(rpath))
            except IOError:
                self.run("echo %s | sudo mkdir %s" % (self.sudopw, 
                                                      os.path.dirname(rpath)))
            self.run("echo %s | sudo touch %s" % (self.sudopw, rpath))
        try:
            self.sftp.put(localpath, rpath)
        except IOError:
            # Remember permissions of parent directory, then upload file.
            dmode = self.run("stat -c %a " + os.path.dirname(rpath))[0].strip()
            if dmode[-1] < 7:
                self.run("echo %s | sudo chmod %s %s" % (self.sudopw, 'o+rwx',
                                                        os.path.dirname(rpath)))
                dirmodded = True
            else:
                dirmodded = False
            self.run("echo %s | sudo chmod %s %s" % (self.sudopw, '666', rpath))
            self.sftp.put(localpath, rpath)
            if dirmodded:  # Change parent mode back to what it was.
                self.run("echo %s | sudo chmod %s %s" % (self.sudopw, dmode,
                                                        os.path.dirname(rpath)))
        return self.chmod(rpath, ownership, mode)
    
    def rename(self, rpath):
        """rename a file .bak"""
        try:
            self.sftp.rename(rpath, rpath+'.bak')
        except IOError:
            return self.run("echo %s | sudo mv %s %s" 
                            % (self.sudopw, rpath, rpath+'.bak'))
                            
    def close(self):
        self.client.close()
