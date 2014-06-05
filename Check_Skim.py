print "\n:: Check Skim \n"
#from ROOT import *
print ":: Importing ROOT"
from ROOT import TH1D,TFile,TChain
print ":: done"
from EosTools import make_eos_file_list

############## setup option parser
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file",       help="file to study",       action="store", type="string",  dest="file",  default=False)
parser.add_option("-e", "--eos_folder", help="eos folder to study", action="store", type="string",  dest="eos_dir",  default=False)
parser.add_option("-n", "--number_of_events", help="only run over a certain number of events",      action="store", type="int",    dest="n_events", default=False)
parser.add_option("-m", "--mc_mode",          help="turn on MC mode",                          action="store_true", dest="mc",     default=False)
parser.add_option("-t", "--trigger_mode",     help="turn on trigger",                          action="store_true", dest="trigger",     default=False)
parser.add_option("-v", "--verbose_mode",     help="turn on verbose mode",                     action="store_true",           dest="verbose",  default=False)


(options, args) = parser.parse_args()

print ":: Options"
print "   file:         ",options.file
print "   eos folder:   ",options.eos_dir
print "   n events:     ",options.n_events
print "   trigger mode: ",options.trigger
print "   mc mode:      ",options.mc
print "   verbose:      ",options.verbose
assert options.file or options.eos_dir, "No file specified, use -f, no eos folder specified, use -e"

chain = TChain("qcd")
print ":: Get cut flow"
if options.file:
    print '\n:: Opening: ',options.file
    chain.Add(options.file)
    n_entries = chain.GetEntries()
    
    
else:
    file_list = make_eos_file_list(options.eos_dir)
    print "Got %i files from eos"%len(file_list)
    cut_flow = False
    for file in file_list:
        chain.Add("root://eosatlas/"+file)
    n_entries = chain.GetEntries()

nevents = chain.GetEntries()
n_all = nevents
print "\n:: Entries: %i"%nevents
if options.n_events: 
    nevents = int(options.n_events)
    print "   running on %i of these"%nevents
print ":: Beginning event loop"

counters = [0,0,0,0,0,0,0,0,0,0,0,0]
trigger_counters = {}

if options.verbose: print_every_n_events = 1
else: print_every_n_events = 1000
for event in range(nevents):
    if event%print_every_n_events == 0:
        if options.verbose: print "\n"
        print '=== Event #%i'%(event)
        
    counters[0]+=1
    if not chain.GetEntry(event):
        print "Couldn't get event %i"%event
    
    n_jets = len(chain.jet_pt)
    counters[1]+=n_jets
    
    assert len(chain.jet_pt) == n_jets
    assert len(chain.jet_e) == n_jets
    assert len(chain.jet_eta) == n_jets
    assert len(chain.jet_raw_eta) == n_jets
    assert len(chain.jet_phi) == n_jets
    assert len(chain.jet_y) == n_jets
    assert len(chain.jet_Badness) == n_jets
    assert len(chain.jet_isUgly) == n_jets
    assert len(chain.jet_jvtxf) == n_jets
    assert len(chain.jet_origin) == n_jets
    
    if options.verbose: print "   RunNumber:       ",chain.RunNumber
    if options.verbose: print "   lbn:             ",chain.lbn
    if options.verbose: print "   EventNumber:     ",chain.EventNumber
    if options.verbose: print "   n_pvtx:          ",chain.n_pvtx
    if options.verbose: print "   good_pvtx:       ",chain.good_pvtx
    if options.verbose: print "   mu:              ",chain.mu
    
    if options.verbose: print "   %i jets found"%n_jets
    for i in range(n_jets):
        if options.verbose: print "   jet[%i]:"%i
        if options.verbose: print "      - jet_pt:      ",chain.jet_pt[i]
        if options.verbose: print "      - jet_e:       ",chain.jet_e[i]
        if options.verbose: print "      - jet_eta:     ",chain.jet_eta[i]
        if options.verbose: print "      - jet_raw_eta: ",chain.jet_raw_eta[i]
        if options.verbose: print "      - jet_phi:     ",chain.jet_phi[i]
        if options.verbose: print "      - jet_y:       ",chain.jet_y[i]
        if options.verbose: print "      - jet_Badness: ",chain.jet_Badness[i]
        if options.verbose: print "      - jet_isUgly:  ",chain.jet_isUgly[i]  
        if options.verbose: print "      - jet_jvtxf:   ",chain.jet_jvtxf[i]        
        if options.verbose: print "      - jet_origin:  ",chain.jet_origin[i]
        
        if chain.jet_Badness[i] >= 4: counters[2]+=1
        if chain.jet_Badness[i] >= 3: counters[3]+=1
        if chain.jet_Badness[i] >= 2: counters[4]+=1
        if chain.jet_Badness[i] >= 1: counters[5]+=1
        if chain.jet_isUgly[i]: counters[6]+=1
        
    if options.verbose: print "   %i trigger passed"%len(chain.triggers)
    for t in chain.triggers:
        if options.verbose: print "      - ",t
        if t not in trigger_counters.keys():
            trigger_counters[t] = [1,0]
        else:
            trigger_counters[t][0]+=1
    
    #if options.verbose: print "   %i RAW trigger passed"%len(chain.triggers_RAW)
    #for t in chain.triggers_RAW:
    #    if options.verbose: print "      - ",t
    #    if t not in trigger_counters.keys():
    #        trigger_counters[t] = [0,1]
    #    else:
    #        trigger_counters[t][1]+=1

    if options.mc:
        truth_n_jets = len(chain.truth_jet_pt)
        counters[7]+=truth_n_jets
    
        assert len(chain.truth_jet_pt)  == truth_n_jets
        assert len(chain.truth_jet_e)   == truth_n_jets
        assert len(chain.truth_jet_eta) == truth_n_jets
        assert len(chain.truth_jet_phi) == truth_n_jets
        assert len(chain.truth_jet_y)   == truth_n_jets
    
    
    
        if options.verbose: 
            print "   %i truth jets found"%truth_n_jets
            for i in range(truth_n_jets):
                print "   truth jet[%i]:"%i
                print "      - truth jet_pt:      ",chain.truth_jet_pt[i]
                print "      - truth jet_e:       ",chain.truth_jet_e[i]
                print "      - truth jet_eta:     ",chain.truth_jet_eta[i]
                print "      - truth jet_phi:     ",chain.truth_jet_phi[i]
                print "      - truth jet_y:       ",chain.truth_jet_y[i]
            
    
    if options.trigger:
        if options.verbose: print "   %i emulated trigger passed"%len(chain.triggers_emulated)
        for t in chain.triggers_emulated:
            if options.verbose: print "      - ",t
            if t not in trigger_counters.keys():
                trigger_counters[t] = [1,0]
            else:
                trigger_counters[t][0]+=1
        #l1_n_jets = len(chain.l1_jet_et)
        #counters[8]+=l1_n_jets
        #assert len(chain.l1_jet_eta) == l1_n_jets
        #assert len(chain.l1_jet_phi) == l1_n_jets
        #assert len(chain.l1_jet_roi_word) == l1_n_jets
        #assert len(chain.l1_jet_thresholds) == l1_n_jets
        
        
        #l2_n_jets = len(chain.l2_jet_et)
        #counters[9]+=list(chain.l2_jet_l2fs).count(0)
        #counters[10]+=list(chain.l2_jet_l2fs).count(1)
        #assert len(chain.l2_jet_eta) == l2_n_jets
        #assert len(chain.l2_jet_phi) == l2_n_jets
        #assert len(chain.l2_jet_roi_word) == l2_n_jets
        
        #ef_n_jets = len(chain.ef_jet_et)
        #counters[11]+=ef_n_jets    
        #assert len(chain.ef_jet_eta) == ef_n_jets
        #assert len(chain.ef_jet_phi) == ef_n_jets
        
        #if options.verbose: 
            #print "   %i l1 jets found"%l1_n_jets
            #for i in range(l1_n_jets):
                #print "   l1 jet[%i]:"%i
                #print "      - l1 jet_et:           ",chain.l1_jet_et[i]
                #print "      - l1 jet_eta:          ",chain.l1_jet_eta[i]
                #print "      - l1 jet_phi:          ",chain.l1_jet_phi[i]
                #print "      - l1 jet_roi_word:     ",chain.l1_jet_roi_word[i]
                #print "      - l1 jet_thresholds:   ",chain.l1_jet_thresholds[i]
            #print "   %i l2 jets found"%l2_n_jets
            #for i in range(l2_n_jets):
                #print "   l2 jet[%i]:"%i
                #print "      - l2 jet_et:       ",chain.l2_jet_et[i]
                #print "      - l2 jet_eta:      ",chain.l2_jet_eta[i]
                #print "      - l2 jet_phi:      ",chain.l2_jet_phi[i]
                #print "      - l2 jet_l2fs:     ",chain.l2_jet_l2fs[i]
                #print "      - l2 jet_roi_word: ",chain.l2_jet_roi_word[i]
            #print "   %i ef jets found"%ef_n_jets
            #for i in range(ef_n_jets):
                #print "   ef jet[%i]:"%i
                #print "      - ef jet_et:      ",chain.ef_jet_et[i]
                #print "      - ef jet_eta:     ",chain.ef_jet_eta[i]
                #print "      - ef jet_phi:     ",chain.ef_jet_phi[i]
                
        
        
        
        
if options.file:
    print '\n:: Opening: ',options.file
    root_file = TFile.Open( options.file )    
    assert root_file.IsOpen()
    print ":: Root File "+options.file+" is open"    
    cut_flow = root_file.Get("cut_flow")
    assert cut_flow, "couldn't get cut flow"  
else:
    file_list = make_eos_file_list(options.eos_dir)
    print "Got %i files from eos"%len(file_list)
    cut_flow = False
    for file in file_list:
        if not cut_flow:
            first_root_file = TFile.Open( "root://eosatlas/"+file )    
            assert first_root_file.IsOpen()
            print "   - root file "+file+" is open"
            cut_flow = first_root_file.Get("cut_flow").Clone("compressed_cut_flow")
        else:
            root_file = TFile.Open( "root://eosatlas/"+file )    
            assert root_file.IsOpen()
            print "   - root file "+file+" is open"
            cut_flow.Add(root_file.Get("cut_flow"))
            root_file.Close()
    
#print "\n=== Raw cut flow"
#for i in range(cut_flow.GetNbinsX()+1):
    #print "Bin[%2i]: %i"%(i,cut_flow.GetBinContent(i))
offset = 1
print "\n=== Summary"
print "    Entries:           %i"%n_entries
print "    Events:            %i"%cut_flow.GetBinContent(1)
print "     - corrupt qcd     %i"%cut_flow.GetBinContent(13)
print "     - corrupt qcdMeta %i"%cut_flow.GetBinContent(14)
print "    GRL:               %i"%cut_flow.GetBinContent(2)
print "    Trigger:           %i"%cut_flow.GetBinContent(3)
print "    LAr:               %i"%cut_flow.GetBinContent(4)
print "    tile:              %i"%cut_flow.GetBinContent(5)
print "    ttc:               %i"%cut_flow.GetBinContent(6)
print "    Vertex:            %i"%cut_flow.GetBinContent(7)
print "    Jets:              %6i  (%6i)"%(cut_flow.GetBinContent(8), counters[1])
print "       -looser:        %6i  (%6i)"%(cut_flow.GetBinContent(9), counters[2])
print "       -loose:         %6i  (%6i)"%(cut_flow.GetBinContent(10), counters[3])
print "       -medium:        %6i  (%6i)"%(cut_flow.GetBinContent(11), counters[4])
print "       -tight:         %6i  (%6i)"%(cut_flow.GetBinContent(12),counters[5])
print "       -ugly:          %6i  (%6i)"%(cut_flow.GetBinContent(13),counters[6])
print "    Skim:              %6i  (%6i)"%(cut_flow.GetBinContent(14),counters[0])
if options.mc:
    print "    Truth Jets         %6i  (%6i)"%(cut_flow.GetBinContent(17),counters[7])
if options.trigger:
    print "    All L1 jets:       %6i  (%6i)"%(cut_flow.GetBinContent(18),counters[8])
    print "    All L2 jets:       %6i       "%cut_flow.GetBinContent(19)
    print "         - c4cc:       %6i  (%6i)"%(cut_flow.GetBinContent(20),counters[9])
    print "         - l2fs:       %6i  (%6i)"%(cut_flow.GetBinContent(21),counters[10])
    print "    All EF jets:       %6i       "%cut_flow.GetBinContent(22)
    print "         - good:       %6i  (%6i)"%(cut_flow.GetBinContent(23),counters[11])
triggers = [
            ### L1
            "L1_RD0_FILLED",
            "L1_J10",
            "L1_J15",
            "L1_J30",
            "L1_J50",
            "L1_J75",
            ### L2
            "L2_rd0_filled_NoAlg",
            "L2_j40_c4cchad",
            "L2_j50_c4cchad",
            "L2_j75_c4cchad",
            "L2_j105_c4cchad",
            "L2_j140_c4cchad",
            "L2_j165_c4cchad",
            ### EF
            "EF_j15_a4tchad",
            "EF_j25_a4tchad",
            "EF_j35_a4tchad",
            "EF_j45_a4tchad",
            "EF_j55_a4tchad",
            "EF_j80_a4tchad",
            "EF_j110_a4tchad",
            "EF_j145_a4tchad",
            "EF_j180_a4tchad",
            "EF_j220_a4tchad",
            "EF_j280_a4tchad",
            "EF_j360_a4tchad",
            "EF_j460_a4tchad",
            ]      

cut_flow_offset = 21
print " By physics trigger"
for t in triggers:
    if t not in trigger_counters.keys():
        trigger_counters[t] = [0,0]
    print "       - %20s %6i  (%6i)"%(t+":",cut_flow.GetBinContent(cut_flow_offset),trigger_counters[t][0])    
    cut_flow_offset+=1
    
#print " RAW trigger"
#for t in triggers:
#    print "       - %20s %6i  (%6i)"%(t+":",cut_flow.GetBinContent(cut_flow_offset),trigger_counters[t][1])    
#    cut_flow_offset+=1



