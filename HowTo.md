# Introduction #

Please see [Installation](Installation.md) for help on getting Figit to run on your system.

Check out WorkFlow for a visualization of the following process.

# The really short example #

```
mkdir /home/jake/figit
cd /home/jake/figit
figit.py init jake@server.domain.com:/etc etc-repo
cd /etc-repo
figit.py add passwd group sudoers
vi ./sudoers
figit.py addhost server2.domain.com
figit.py install
```

# Some explaination #

Create a directory to hold all your Figit repositories.
```
mkdir /home/jake/figit
cd /home/jake/figit
```

Direct Figit to initialize a new repository bound to the `etc` directory of the Source Host named server.domain.com:
```
figit.py init jake@server.domain.com:/etc etc-repo
```

Notice that Figit has created a directory using the name you specified `etc-repo`. You'll find that this directory contains two VCS branches. Within `etc-repo` you should find a new directory called `.figit` and possibly a `.ignore` file. There are a couple of files in the `.figit` directory that Figit uses to remember it's configuration. All these files are editable by hand and will be tracked by the VCS. Just be careful about the syntax when making changes. The initial state of this new directory has also been committed to the VCS repository. Take a second to have a look around to get a feel for what the init command has done. See [Configuration](Configuration.md) for further discussion of the configuration files.

If we want a list of what files are actually in `/etc` on the Source Host we can run `ls`.

```
cd etc-repo
figit.py ls
```

By default ls will list the directory you specified at init time but you can also pass a relative path to examine subdirectories.

```
figit.py ls security/
```

This will list the contents of `/etc/security` on the source host.

Next we ask Figit to get a copy of the `password`, `group` and `sudoers` files from server.domain.com:
```
figit.py get passwd group sudoers
```

You don't have to specify server.domain.com this time because your new repository was bound to server.domain.com when you ran init. Figit now considers server.domain.com to be the **Source Host** for the repository and will default to it as the source for all files whenever you run get. You'll notice that the three files are now in your working directory and that they have each been committed by Figit to the VCS. You may also notice that the file `.figit/manifest` has been modified. See [Manifest](Manifest.md) if you care for an explanation of what is going on with that file.

Next let's edit the `sudoers` file and make some random change.

Suppose you have a few more hosts called server2, and server3 who's `password`, `group` and `sudoers` files should be kept as identical copies of the files on server.domain.com. First I need to add the hosts to the distribution list so Figit will remember them.
```
figit.py addhost server2.domain.com server3.domain.com
```
Assuming that these host names are resolvable, Figit will append them to the end of `.figit/config` as **Distribution Hosts**. See [Terminology](Terminology.md).

Now to install the modified `sudoers` file from the working directory to server, server2 and server3:
```
figit.py install
```

Note that, for this step to work, the ssh user you specify may need certain sudo [Privileges](Privileges.md) configured on the remote hosts.

Figit will notice that `sudoers` has changed since you ran `get` to pull it into the working directory. It will then connect to the servers in your distribution list and check the remote version of `sudoers` to see if it is different then the version that was pulled from the Source Host. If it is not different, Figit will happily overwrite the file with your changes and set the ownership and mode to match what is recorded in the [Manifest](Manifest.md) file. If `sudoers` is different (a condition referred to as an **Out of Band Change**), then Figit will attempt to create a backup (`.bak`) of the file on the remote system before uploading the new version. It does this for each system in the distribution list including the **Source Host** which is always implicitly included as a **Distribution Host**.

Note that `figit.py install` will upload **all** changes it finds in your working directory. So if you changed `sudoers` and `passwd` but you really intended to upload only the change to `sudoers`, you should first revert `password` to a production state. Think of the `install` command as taking a snapshot of your entire working directory and then replicating that snapshot on all the hosts in your distribution list. This all or nothing behavior may be modified in a future version. Until then, if you're comfortable with branching in your VCS, branching would be one way to achieve selective updates.


# Reverting a file to a past version #

Ok, so the maybe a change we uploaded broke something. How do we get back to a know good state? The exact steps depend on the VCS backend you're using. In essence, we just call the VCS to revert or checkout the file in question to an older state. Figit automatically performs a VCS commit before it will upload anything so, even if you forget to commit changes yourself, the VCS should still contain a record of every state that was ever "installed" on the distribution hosts including the initial state of the file. Once the content of the current working directory matches what we'd like to see on the distribution hosts we just run `figit.py install` and Figit will try it's best to make it so.

# What Next? #

The preceeding info should get you started using Figit but if you have more questions please browse the other documents in the [Wiki](http://code.google.com/p/figit/w/list) and post to the [MailingList](http://groups.google.com/group/figit-users) which **is** monitored by the developer(s). Or just read the [Code](http://code.google.com/p/figit/source)
