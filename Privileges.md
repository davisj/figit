When you initialize a new Figit repository, you must specify the username that Figit will connect as to all Source and Distribution Hosts. If this user account lacks the proper permissions to read or modify the files that you intend to manage with Figit then you will want to setup [sudo](http://en.wikipedia.org/wiki/Sudo) on the Distribution Hosts to allow the account to run `chown`, `chmod`, `mkdir`, and `mv`.

Whenever Figit encounters a permission problem or needs to adjust the ownership or mode of remote files it will attmept to do so by calling `sudo` on the remote system. Figit supports this by prompting the user for a sudo password that will be used to perform any function on the remote system that can not be performed with the normal privileges of the specified account.

For example, if the I initialize a repo like so: `figit.py init figit@remotehost:/etc ./remote-etc`. I may might need to add a user named `figit` to remotehost and add a line to `/etc/sudoers` on remotehost that looks something like this:

```
figit   ALL=(ALL) /bin/mv, /bin/chown, /bin/chmod, /bin/mkdirmo
```