print "\n:: Decode cut flow of a QCD skim. This version doesn't include TTC or tile error checks \n"
#from ROOT import *
print ":: Importing ROOT"
from ROOT import TH1D,TFile,TChain
print ":: done"
from EosTools import make_eos_file_list
from Tools import make_file_list

############## setup option parser
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--files",          help="files to study",                          action="store", type="string",  dest="files",   default=False)
parser.add_option("-e", "--eos_folder",     help="eos folder to study",                     action="store", type="string",  dest="eos_dir", default=False)
parser.add_option("-t", "--token",          help="grep token",                              action="store", type="string",  dest="token",   default="")
parser.add_option("-n", "--number_of_runs", help="only run over a certain number of runs",  action="store", type="int",     dest="n_runs",  default=False)
parser.add_option("-v", "--verbose_mode",   help="turn on verbose mode",                    action="store_true",            dest="verbose", default=False)
parser.add_option("-g", "--glados",         help="run on glados",                           action="store_true",            dest="glados",  default=False)
parser.add_option("-r", "--runs",           help="only study these runs",                   action="store", type="string",  dest="runs",    default=False)
parser.add_option("-s", "--strip",          help="strip leading zeros from run names",      action="store_true",            dest="strip",   default=False)


(options, args) = parser.parse_args()

print ":: Options"
print "   files:        ",options.files
print "   eos folder:   ",options.eos_dir
print "   token:        ",options.token
print "   n runs:       ",options.n_runs
print "   runs:         ",options.runs
print "   glados:       ",options.glados
print "   strip:        ",options.strip
print "   verbose:      ",options.verbose

assert options.eos_dir, "no eos folder specified, use -e"

if options.files:
    file_list = open(options.files,"r").readlines()
    print "Got %i runs from file_list"%(len(file_list))
    runs = []
    for file in file_list:
        print file
        run = file.split(".")[1]
        if options.strip: run = run[2:]
        runs.append(run)
elif options.runs:
    runs = options.runs.split(",")
    print "Got %i runs from augments"%len(runs)

runs.sort()
print "Got %i runs"%len(runs)

nevents = len(runs)
if options.n_runs: 
    nevents = int(options.n_runs)
    print "   running on %i of these"%nevents
    
print "Making files list"
if options.glados:  file_list = make_file_list(options.eos_dir,grep=options.token,verbose=options.verbose)
else:               file_list = make_eos_file_list(options.eos_dir,grep=options.token,verbose=options.verbose)
print "Got %i files"%len(file_list)


if options.glados:  prefix = ""
else:               prefix = "root://eosatlas/"

run_information = {}
bad_runs = []
zero_entry_runs = []
for i,run in enumerate(runs):
    if options.runs and (run not in options.runs): continue
    if i == nevents: 
        print "Reached run limit"
        break
    this_file_list = []
    for file in file_list:
        if run in file: this_file_list.append(file)
    #file_list = make_eos_file_list(options.eos_dir,grep=run,verbose=options.verbose)
    print "[%3i/%3i] - got %i files from eos for run: %s"%(i+1,len(runs),len(this_file_list),run)
    if not len(this_file_list): 
        run_information[run] = [0 for i in range(35)]
        continue
    cut_flow = False
    for file in this_file_list: 
        try:            
            if not cut_flow:
                first_root_file = TFile.Open( prefix+file )    
                assert first_root_file.IsOpen()
                if options.verbose: print "   - root file "+file+" is open"
                cut_flow = first_root_file.Get("cut_flow").Clone("compressed_cut_flow")
                if options.verbose: print "    - cut flow[1]: %i"%cut_flow.GetBinContent(1)
                first_chain = TChain("qcd")
                first_chain.Add(prefix+file)
                n_entries =first_chain.GetEntries()
                
                if cut_flow.GetBinContent(1)==0: zero_entry_runs.append(file)
            else:
                root_file = TFile.Open( prefix+file )    
                assert root_file.IsOpen()
                if options.verbose: print "   - root file "+file+" is open"
                this_cut_flow = root_file.Get("cut_flow")
                if options.verbose: print "    - cut flow[1]: %i"%this_cut_flow.GetBinContent(1)
                cut_flow.Add(this_cut_flow)
                chain = TChain("qcd")
                chain.Add(prefix+file)
                n_entries+=chain.GetEntries()
                if this_cut_flow.GetBinContent(1)==0: zero_entry_runs.append(file)
                root_file.Close()    
        except:
            print "Failure on run: %s, file: %s"%(run,file)
            bad_runs.append(file)
            print "   - %i bad runs so far"%len(bad_runs)
            #cut_flow = False
            #assert False
        
    #if not cut_flow: continue
    offset = 1
    if options.verbose: 
        print "\n=== Summary"
        print "    Entries:     %i"%n_entries
        print "    Events:            %i"%cut_flow.GetBinContent(1)
        print "     - corrupt qcd     %i"%cut_flow.GetBinContent(13)
        print "     - corrupt qcdMeta %i"%cut_flow.GetBinContent(14)
        print "    GRL:               %i"%cut_flow.GetBinContent(2)
        print "    Trigger:           %i"%cut_flow.GetBinContent(3)
        print "    LAr:               %i"%cut_flow.GetBinContent(4)
        print "    tile:              %i"%cut_flow.GetBinContent(5)
        print "    ttc:               %i"%cut_flow.GetBinContent(6)
        print "    Vertex:            %i"%cut_flow.GetBinContent(7)
        print "    Jets:              %i"%cut_flow.GetBinContent(8)
        print "       -looser:        %i"%cut_flow.GetBinContent(9)
        print "       -loose:         %i"%cut_flow.GetBinContent(10)
        print "       -medium:        %i"%cut_flow.GetBinContent(11)
        print "       -tight:         %i"%cut_flow.GetBinContent(12)
        print "       -ugly:          %i"%cut_flow.GetBinContent(13)
        print "    Skim:              %i"%cut_flow.GetBinContent(14)
        print "    Truth jets:        %i"%cut_flow.GetBinContent(17)
        #print "    Vertex:            %i"%cut_flow.GetBinContent(5)
        #print "    Jets:              %i"%cut_flow.GetBinContent(6)
        #print "       -looser:        %i"%cut_flow.GetBinContent(7)
        #print "       -loose:         %i"%cut_flow.GetBinContent(8)
        #print "       -medium:        %i"%cut_flow.GetBinContent(9)
        #print "       -tight:         %i"%cut_flow.GetBinContent(10)
        #print "       -ugly:          %i"%cut_flow.GetBinContent(11)
        #print "    Skim:              %i"%cut_flow.GetBinContent(12)
        #print "    Truth jets:        %i"%cut_flow.GetBinContent(15)
    triggers = [
                ### new naming convention triggers
                "EF_j10_a4tc_EFFS",
                "EF_j15_a4tc_EFFS",
                "EF_j20_a4tc_EFFS",
                "EF_j30_a4tc_EFFS",
                "EF_j40_a4tc_EFFS",
                "EF_j55_a4tc_EFFS",
                "EF_j75_a4tc_EFFS",
                "EF_j100_a4tc_EFFS",
                "EF_j135_a4tc_EFFS",
                "EF_j180_a4tc_EFFS",
                "EF_j240_a4tc_EFFS",
                ### old naming convention triggers were used pre-period D, I don't think we'll need these
                ]      
    
    cut_flow_offset = 23 # pre truth offset was 15, was 16 13/11/12
    if options.verbose: print " By physics trigger"
    for t in triggers:
        if options.verbose: print "       - %20s %i"%(t+":",cut_flow.GetBinContent(cut_flow_offset))    
        cut_flow_offset+=1
        
    if options.verbose: print " RAW trigger"
    for t in triggers:
        if options.verbose: print "       - %20s %i"%(t+":",cut_flow.GetBinContent(cut_flow_offset))    
        cut_flow_offset+=1
        
    run_information[run] = []
    for i in range(34):
        run_information[run].append(cut_flow.GetBinContent(i))
        
    run_information[run].append(len(this_file_list))
    
    first_root_file.Close()
    
if len(bad_runs):
    print "\n=== Bad runs"
    for run in bad_runs:
        command = "xrd eosatlas rm %s"%run
        print command
if len(zero_entry_runs):
    print "\n=== Zero entry runs"
    for run in zero_entry_runs:
        command = "xrd eosatlas rm %s"%run
        print command


print "\n=== Full overall summary"
print "%-10s %15s %15s %15s %15s %15s %15s %15s %15s %15s"%("run","Events","GRL", "Trigger", "LAr", "tile", "ttc", "vertex", "Skim", "files")

for i,run in enumerate(runs):
    if i == nevents: break
    print "%-10s %15i %15i %15i %15i %15i %15i %15i %15i %15i"%\
     (run,run_information[run][1],run_information[run][2],run_information[run][3],run_information[run][4],0,0,run_information[run][5],run_information[run][12],run_information[run][34])
    
    
        
print "\n=== Overall summary"
print "%-10s %15s %15s %10s"%("run","seen by skim","skimmed","files")
all = [0,0,0]
for i,run in enumerate(runs):
    if i == nevents: break
    print "%-10s %15i %15i %10i"%(run,run_information[run][1],run_information[run][14],run_information[run][34])
    all[0]+=run_information[run][0]
    all[1]+=run_information[run][1]
    all[2]+=run_information[run][2]



