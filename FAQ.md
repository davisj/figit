## What is figit? ##

Figit is primarily intended for management of configuration files across multiple systems. Figit is basically a wrapper. It extends the core file content tracking capabilities of VCS software like SVN, CVS, GIT, BZR, Mercurial, etc... by adding the ability to track per-file metadata such as file mode and ownership and providing helper functions for distributing file changes from a central repository to multiple systems using ssh.

Core design goals include:
  * **Modular integration with powerful version control backends**: Use a modern VCS to provide the ability to revert a file to any previous state and see what changed, when it changed and who changed it, etc.
  * **Easy of maintenance**: Provide the ability to add systems and files to the repository quickly and easily. Avoid requirements to install or maintain extra software on client systems beyond common OS utilities (like ssh, sudo and a command shell). The version control repository and related software utilities should only reside on one central management server.
  * **Ease of use**: Our goal is that anyone with basic Unix admin skills should be able to get Figit up and running in less then five minutes.


## Why would I use Figit instead of cfengine, puppet or bcfg2? ##
In a word; **simplicity**. Figit does not pretend to compete with these systems in terms of functionality. If you need to do the sort of things that make those systems necessary, then Figit is probably not for you. If you're looking for something a little more light weight, then Figit might be just the thing. The config file syntax for Figit is intended to remain extremely simple.


## How is Figit pronounced? ##
Like the word `fidget`.
```
fidget  (n.)
1674, as the fidget "uneasiness," later the fidgets, from a 16c. v. fidge "move restlessly," from M.E. fiken "to fidget, hasten," from O.N. fikjask "to desire eagerly" (cf. Ger. ficken "to move about briskly;" see fuck). The v. fidget is first attested 1672 (implied in fidgetting).
```


## How is Figit better then RCS plus SSH scripts? ##
Well, it's more fun to say ;)  It also tracks and sets ownership and file mode settings for you automatically. Other then that, there's this project page you're reading right now which will hopefully encourage others to contribute and improve Figit. So that, one day, it may be even more better then rcs and a ssh script. _(yes, I just said "more better")_


## Why didn't you write Figit as a plug in for <git/bzr/hg/svn>? ##
The method for extending any one of these systems is fairly different from all the others. We came at it from the other direction reasoning that it'd be a lot easier for us to wrap a dozen VCS's with Figit then it would be to wrap Figit with a dozen VCS's.


## Why the bias towards <not my favorite VCS>? ##
We like to think there's not a bias. We tried to make the VCS interface generic enough as to be easily extended to support many VCS backends. If you feel a particular VCS is under represented, please consider contributing a patch or joining the project.
