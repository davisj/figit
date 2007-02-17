# Class for reading the RunBefore/Runafter files.


from os.path import join


def Run(runfile):
    """
    Run creates a dictionary which is a mapping of filenames and command lines.
    This dictionary is read when figit.install() is called in order to determine
    what, if any runbefore or runafter scripts need to be run on the 
    distribution hosts. If a filename in the upload list matches a name in the
    dictionary returned by this class, then the script name is run.
    """
    # Since the RunBefore/After files are intended as part of the user interface
    # we try to handle hand editing of them gracefully. 
    run = {}
    fd = open(join(".figit", runfile), 'r')
    for line in fd.readlines():
        if line[0] not in (';','#', '"', "'"):  # Ignore comments
            i = line.replace('\t', ' ').index(' ') # convert tabs to space
            filename = line[:i]
            cmmd = line[i:].strip()
            try:
                comment = cmmd.index('#')  # Chop off any EOL user comments.
                run[filename] = cmmd[:comment].strip()
            except ValueError:
                run[filename] = cmmd
    fd.close()
    return run
