## Installation Requirments ##
  * [Python](http://www.python.org) 2.4 or greater - Figit has not been tested with other version of Python.
  * [Paramiko](https://launchpad.net/paramiko) 1.7 or greater - 1.6.4 will work if you impliment the workaround for this [bug](https://launchpad.net/paramiko/+bug/80295).
  * Install the [VCS](http://en.wikipedia.org/wiki/List_of_revision_control_software) you intend to use with Figit. At the time of this writing (Jan. 27 2007) Figit has incorporated support for the following VCS's:
    * [git](http://git.or.cz/)

There are at least two ways to install Figit.

## Setup.py Method ##
If you don't intend to make changes to Figit, or update to newer versions frequently, this is probably the method you want to use.
  * Unzip the Figit-

&lt;version&gt;

.tar.gz on your system and cd to the newly created figit directory.
  * As root run `python ./setup.py install`

## Alternate Method ##
  * [Checkout](http://code.google.com/p/figit/source) the subversion repository trunk to a folder on your system.
  * Create a symlink to the `figit/Figit` folder under your site-packages directory `ln -s /path/to/figit/Figit /usr/lib/python2.4/site-packages/Figit`
  * Add the the newly created `figit/bin` folder to your $PATH. `export PATH=$PATH:/path/to/figit/bin`