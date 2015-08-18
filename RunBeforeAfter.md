# RunBefore and RunAfter Jobs #

When you initialize a new Figit repository two configuration files are created named .figit/RunBefore and .figit/RunAfter. This is where you can tell figit about commands that you wish to be executed on distribution hosts when particular files are being changed. When you call `figit.py install` Figit builds a list of updated files that it will upload to distribution hosts. Figit then looks at the RunBefore/RunAfter files to see if they contain any entries that match the filenames in the upload list. If there is a match Figit will call the command specified either before or after the new version of the file is uploaded. It will do so on each distribution host. The simplest explanation is an example:

```
apache/httpd.conf   /etc/init.d/apache restart
```

If Figit sees this entry in RunAfter and an accompanying "apache/httpd.conf" entry in the manifest it will execute the `/etc/init.d/apache restart` command whenever a new version of the httpd.conf file is uploaded.