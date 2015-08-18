### WD (Working Directory): ###
> The version control system working directory where all files are edited.

### Figit Host: ###
> The Machine were Figit is installed. This host contains the WD.

### Source Host: ###
> The host that all files originate from. Figit populates the WD by retrieving
> files from the Source Host via SSH.

### Distribution Host: ###
> A host that is a target for file uploads. Any changes made to files in the
> WD will be copied to all Distribution Hosts in your Distribution List when
> you run the install command. Note that the Source Host is implicitly
> included in the Distribution List.

### INSTALLBRANCH: ###
> A VCS branch created and maintained automatically by Figit. INSTALLBRANCH
> files always mirror the expected condition of files on the Distribution
> Hosts. When adding a file it is first checked into INSTALLBRANCH. Then
> merged into DEVBRANCH for editing. Files should never be edited directly in
> the INSTALLBRANCH. Doing so will break Figit badly. When you're ready to
> install changes made in the DEVBRANCH to the Distribution Hosts, Figit will
> merge all changes from DEVBRANCH into INSTALLBRANCH immediately after
> uploading them to the Distribution Hosts.

### DEVBRANCH: ###
> Any VCS branch were file editing takes place. DEVBRANCH is any branch that's
> not the INSTALLBRANCH.