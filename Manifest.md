The manifest file is were the metadata for each file live. When figit is used to add a file to your VCS working directory it writes a single line to the manifest with four peices of information.
  1. relative filename
  1. ownership information.
  1. file mode in 4 digit octal format
  1. sha hash of the file content.

**Example**: given a source directory of `/usr/local`, if we added
`/usr/local/file`, `/usr/local/bin/myprog` and `/usr/local/etc/configfile` to
the repository, lines similar to the following would be generated in manifest:

```
file root:users 0644 584c41b5b85ac6a8c782224c47d4205ff006645c
bin/myprog bob:users 0755 584c41b5b85ac6a8c782224c47d4205ff0066abc
etc/configfile root:root 0640 584c41b5b85ac6a8c782224c47d4205ff0066xyz
```

The manifest is intended to be editable by a human using a standard text editor. Editing the sha1 hash, though, will probably not be very usefull in practice. It is there for figit's own internal comparison functions which allow it to determine if a file has been altered since the last time figit recorded the state.
_(note for git users: these sha hashes have no relation to git's hashes)_

Whenever changes are written to a target systems by figit, the manifest is used as the input for how the ownership and mode should be set on the target system. If I edited the manifest by hand and changed the mode line for `bin/myprog` to 0644, then that mode would be set on that file on each target system the next time I ran figit install.

Have a look at FileModes for a description of the possiblbe values of the 4 digit octal file mode field.

**Note**: The uid and gid, which may differ from machine to machine for a given user, must **NOT** be recorded numerically.