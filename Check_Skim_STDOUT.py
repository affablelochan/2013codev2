from glob import glob
import EosTools
file_list = glob("*/STDOUT")
print "\nFound %i files"%len(file_list)

RANGE = len(file_list)
VERBOSE=False

bad_jobs = {}

for i in range(RANGE):
    lines = open(file_list[i],"r").readlines()
    delta_phi = False
    input_files = False
    dname = False
    dq2_error = False
    dq2_files = False
    id = False
    corrupt_event = False
    for ii,line in enumerate(lines):
        line = line.strip()
        if VERBOSE: print "line[%6i]: %s"%(ii,line)
        
        if "RETRIEVING FROM DQ2 THE INPUT BS FILE TO WORK WITH:" in line:
            input_files = line.split(": ")[1]
        if "** Some files failed transfer, reached maximum re-trial times, please try again later **" in line:
            dq2_error = True
        if "Number of successful file download attempts:" in line:
            dq2_files = int(line.split(": ")[1])
        if ":: Beginning Delta Phi Study" in line:
            delta_phi = True
        if "run  :   output file:        ./dpd-" in line:
            id = line.split("./dpd-")[1][:-5]
        if "Querying DQ2 central catalogues to resolve datasetname " in line:
            dname=line.split("datasetname ")[1]
        
        if "couldn't get entry" in line:
            corrupt_event = True
            
    if delta_phi: continue
    
    if corrupt_event:
        print " -- corrupt event %s %s %s" % (dname, input_files, id)
        
    fileList=EosTools.make_eos_file_list("/eos/atlas/user/t/tamsett/skims_30GeV",grep=id+".",verbose=False)
    if not len(fileList):
        print " -- ouput file not found: ",id
        
    #if VERBOSE: 
        #print "Found %i input files: "%(len(input_files.split(","))),input_files
        #print "Found id:             ",id
        #print "Found dname:          ",dname
        #print "DQ2 error:            ",dq2_error
        #print "DQ2 files:            ",dq2_files
    #if (not input_files) or (not dq2_files):
        #for ii,line in enumerate(lines):
            #line = line.strip()
            #print "line[%6i]: %s"%(ii,line)
        #print "Found id:             ",id
        #print "Found dname:          ",dname
        #print "DQ2 error:            ",dq2_error
        #print "DQ2 files:            ",dq2_files
        #assert False
   
    if ((not input_files) or (not dq2_files) or (len(input_files.split(",")) != dq2_files)):
        if not dname: 
            print " -- No datasetname found: ",id
        
        bad_job_line = "bsub -q 8nh run_bsub_skim_dq2.sh %s %s %s" % (dname, input_files, id)
        bad_jobs[id] = bad_job_line
        print "  - %i bad jobs found so far"%len(bad_jobs.keys())

print "\n=== %i bad files found\n"%len(bad_jobs.keys())
keys = bad_jobs.keys()
keys.sort()
for job in keys:
    print "=== Bad job for run: %s\n"%job
    print "xrd eosatlas rm /eos/atlas/user/t/tamsett/skims_30GeV/%s"%job
    print "%s\n"%bad_jobs[job]
    
    
