import commands

def make_file_list(folder,grep=False,verbose=True):
    """
    This function makes a list of files for a given folder
    """
    lsCommand =  'ls  %s' % folder
    if verbose: print "tools: === In Tools make_file_list"
    if verbose: print "tools: folder:      ",folder
    if verbose: print "tools: grep:        ",grep
    if verbose: print "tools: getting list of files"
    raw_fileList = commands.getoutput(lsCommand).split('\n')
    #print raw_fileList
    fileList = []
    for line in raw_fileList:
        if not len(line): continue
        if grep and grep not in line: continue
        fileList.append("%s/%s"%(folder,line))
        
    if verbose: print "tools: %d files found" % len(fileList)
    return fileList
