import commands

def make_eos_file_list(folder,final_token=False,grep=False,verbose=True):
    """
    This function makes a list of files for a given eos folder
    """
    nslsCommand =  'xrd eosatlas dirlist  %s' % folder
    if verbose: print "eos  : === In EosTools make_eos_file_list"
    if verbose: print "eos  : folder:      ",folder
    if verbose: print "eos  : final_token: ",final_token
    if verbose: print "eos  : grep:        ",grep
    if verbose: print "eos  : getting list of files"
    raw_fileList = commands.getoutput(nslsCommand).split('\n')
    fileList = []
    for line in raw_fileList:
        if not len(line.split()): continue
        if grep and grep not in line: continue
        if final_token: fileList.append(line.split()[4].split("/").pop())
        else:           fileList.append(line.split()[4])
        #fileList.append(line.split())
        
    if verbose: print "eos  : %d files found" % len(fileList)
    return fileList
