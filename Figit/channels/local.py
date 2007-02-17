# Local filesystem access channel for Figit.

# import os
# import sha


# class LocalChannel:
#     """
#     A Class with functions for examining and manipulating a source 
#     directory that resides on the local file system.
#     """
#     # Until someone thinks of a better way, we'll brute force permissions
#     # using sudo whenever the first write attempt fails.  
#     import pwd
#     import grp
#     from shutil import copyfile
#     from stat import S_ISDIR
#     from commands import getoutput as go
#     def __init__(self):
#         pass

#     def ls(self, rpath):
#         return os.listdir(rpath)

#     def digest(rpath, sudopw='No'):
#         """Returns a sha hash of the file content of remote path."""
#         try:
#             fobj = open(rpath)
#             chmodded = False
#         except IOError:
#              # Force world readableness
#             go("echo %s | sudo chmod o+r %s" % (sudopw, rpath))
#             chmodded = True
#             fobj = open(rpath)
#         m = sha.new()
#         while True:
#             d = fobj.read(8096)
#             if not d:
#                 break
#             m.update(d)
#         fobj.close()
#         if chmodded == True:
#              # Undo world readableness
#             go("echo %s | sudo chmod o-r %s" % (sudopw, rpath))
#         return m.hexdigest()
#                          
#     def stats(self, rpath, sudopw='No'):
#         """Returns (uid, gid, mode, filetype, sha1hash) for rpath."""
#         info = os.stat(rpath)
#         uid = pwd.getpwuid(info[4])[0]
#         gid = grp.getgrgid(info[5])[0]
#         mode = oct(info[0])[-4:]
#         if S_ISDIR(info.st_mode):
#             filetype = 'directory'
#         else:
#             filetype = 'file'
#         newdigest = self.digest(rpath, sudopw)
#         return (uid, gid, mode, filetype, newdigest)

#     def chmod(self, rpath, ownership, mode, sudopw='No'):
#         """Set file ownership and mode on the remote path."""
#         out = go("echo %s | sudo chown %s %s" % (sudopw, ownership, rpath))
#         out += go("echo %s | sudo chmod %s %s" % (sudopw, mode, rpath))
#         return out
#         
#     def get(self, rpath, localpath, sudopw='No'):
#         """download a file"""
#         try:
#             copyfile(rpath, localpath)
#         except IOError:
#             # Force world readableness
#             go("echo %s | sudo chmod o+r %s" % (sudopw, rpath)) 
#             copyfile(rpath, localpath)
#             # Undo world readableness
#             go("echo %s | sudo chmod o-r %s" % (sudopw, rpath)) 
#         
#     def put(self, localpath, rpath, sudopw='No'):
#         """Copy a file to the remote directory."""
#         try:
#             copyfile(localpath, rpath)
#         except IOError:
#             # force world readableness
#             go("echo %s | sudo chmod o+r %s" % (sudopw, rpath)) 
#             copyfile(localpath, rpath)
#             # undo world readableness
#             go("echo %s | sudo chmod o-r %s" % (sudopw, rpath)) 

#     def rename(self, rpath, sudopw='No'):
#         """Rename a file with a '.bak' extension."""
#         try:
#             os.rename(rpath, rpath+'.bak')
#         except IOError:
#             # force world readableness
#             go("echo %s | sudo chmod o+r %s" % (sudopw, rpath))
#             os.rename(rpath, rpath+'.bak')
