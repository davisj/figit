# The .figit directory #

  * .figit
  * .figit/config
  * .figit/manifest
  * .figit/manifest.bak*** .figit/RunAfter
  * .figit/RunBefore**


# config #

Figit stores most of what it needs to remember in this file which is automatically generated during initialization.

It probably looks something like this.

```
wd:/home/jake/etc-repo
src:jake@server.domain.com:/etc
host:server2.domain.com
host:server3.domain.com
```

The first line tells Figit were your **Working Directory** is located.
The second tells Figit what username to use when connecting to remote machines over SSH. It also tells Figit the name of the **Source Host** and the directory where tracked files live.


# manifest #

[Manifest](Manifest.md)


# RunBefore/After #

[RunBeforeAfter](RunBeforeAfter.md)