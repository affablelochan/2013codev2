print "run  : === Skimmer, the 2013 version"
print "run  : Importing ROOT"
#from ROOT import TChain,gROOT,gSystem,TFile, TTree, TH1F, std, AddressOf
import ROOT
ROOT.gROOT.SetBatch(1)
print "run  : done"
import PyCintex
from optparse import OptionParser
#import D3PD_Tools as D3T
from math import fabs, sqrt, cosh
import Utilities

################################## Run time options
parser = OptionParser()
parser.add_option("-n", "--number_of_events", help="only run over a certain number of events", action="store",      type="int",    dest="n_events", default=False)
parser.add_option("-i", "--input_files",      help="formatted list of events to select",       dest="input_files",  default=False)
parser.add_option("-o", "--output_file",      help="output_file_name",                         action="store",      type="string", dest="output_file",  default="fat_jet.root")
parser.add_option("-m", "--mc_mode",          help="turn on MC mode",                          action="store_true", dest="mc",     default=False)
parser.add_option("-T", "--truth_type",       help="truth jet type to study",                  action="store",      type="string", dest="truth_type",   default="WithMuNoInt")
parser.add_option("-p", "--pileup_cut",       help="turn on MC pileup cut",                    action="store_true", dest="pu",     default=False)
parser.add_option("-t", "--trigger_mode",     help="turn on trigger mode",                     action="store_true", dest="trigger",default=True)
parser.add_option("-s", "--slim_mode",        help="turn on slim mode",                        action="store_true", dest="slim",   default=False)
parser.add_option("-j", "--jet_type",         help="jet type to study",                        action="store",      type="string", dest="jet_type",   default="AntiKt6TopoEM")
#parser.add_option("-y", "--rapidity_cut",     help="max jet y",                                action="store",      type="float",  dest="max_y",      default=1.0)
#parser.add_option("-N", "--multiplicity_cut", help="min jet n",                                action="store",      type="int",    dest="n_jets",     default=1)
parser.add_option("-r", "--recalibrate",      help="recalibrate jets",                         action="store",      type="string", dest="recalibrate",default="default")
parser.add_option("-g", "--no_grl_mode",      help="disable GRL",                              action="store_true", dest="no_grl", default=False)
parser.add_option("-v", "--verbose_mode",     help="turn on verbose mode",                     action="store_true", dest="verbose",default=False)
(options, args) = parser.parse_args()

print "run  : Options:"
print "run  :   number of events:  ",options.n_events
print "run  :   input files:       ",options.input_files
print "run  :   output file:       ",options.output_file
print "run  :   mc mode:           ",options.mc
print "run  :   pileup cut for mc: ",options.pu
print "run  :   slim mode:         ",options.slim
print "run  :   trigger mode:      ",options.trigger
print "run  :   recalibrate:       ",options.recalibrate
print "run  :   no grl:            ",options.no_grl
print "run  :   verbose mode:      ",options.verbose

################################## Setup up options
print "run  : === Setup"
JET_TYPE = options.jet_type
TRIGGER_RAW = 2
L1_TRIGGER_RAW = 4
RECALIBRATE = options.recalibrate
TRUTH_TYPE = options.truth_type
assert "Kt6" in JET_TYPE
if "TopoEM" in JET_TYPE: 
    SCALE = "emscale"
    RHO_NAME = "Eventshape_rhoKt4EM"
else:                    
    SCALE = "constscale"
    RHO_NAME = "Eventshape_rhoKt4LC"
    
print "run  : JET_TYPE:            ",JET_TYPE
print "run  :    SCALE:            ",SCALE
print "run  :      RHO:            ",RHO_NAME
print "run  : RECALIBRATE:         ",RECALIBRATE
print "run  : TRUTH_TYPE:          ",TRUTH_TYPE
######### input files
if options.input_files:
    if "*" in options.input_files:
        import glob
        print "run  : globing input files"
        d3pds = glob.glob(options.input_files)
    else:
        d3pds = options.input_files.split(",")
        print "run  : using commandline list of %i input files"%(len(d3pds))
    
    assert len(d3pds),"run  : no input files found"
    #chain_name = "trigger"
    chain_name = "qcd"
    chain = ROOT.TChain(chain_name)
    trigger_chain = ROOT.TChain(chain_name+"Meta/TrigConfTree")
    
    for d3pd in d3pds:
        print "run  :    - %s"%d3pd
        chain.Add(d3pd)
        trigger_chain.Add(d3pd)
        assert chain.GetEntries(), "run  : No entries in input file: %s, an error has probably occured"%d3pds
else:
    assert False,"run  : no input file given"


nevents = chain.GetEntries()
print "run  : Dataset: %i file(s) and %i events:"%(len(d3pds),nevents)
assert nevents,"run  : No entries in any input file(s), an error has probably occured"

for f in d3pds:
    print "run  :     - %s"%f
if options.n_events: 
    nevents = options.n_events
    print "run  : running on %i event(s)"%nevents
######## setup Tree Reader
from TreeReader import TreeReader
chainReader = TreeReader(chain)
#branches = ["RunNumber","lbn","EventNumber","larError","averageIntPerXing","vxp_n","vxp_nTracks","jet_%sTopoEM_*"%JET_TYPE]
#chain.SetBranchStatus("*",0)
#for branch in branches:
    #chain.SetBranchStatus(branch,1)
######## setup the tdt
print "run  : Loading the trigger decision tool"
ROOT.gSystem.Load( "libTrigRootAnalysis.so" )
tdt = ROOT.D3PD.PyTrigDecisionToolD3PD(chain,trigger_chain)
triggers = [
            ### L1
            "L1_J50",
            "L1_J75",
            ### L2
            "L2_j140_c4cchad",
            "L2_j165_c4cchad",
            ### EF
            "EF_j240_a10tcem",
            "EF_j360_a10tcem",
            ]            
print "run  :   %i triggers to study:"%len(triggers)
for trigger in triggers:
    print "run  :     - %s"%trigger
########### grl
print "run  : Setting up GRL"
#grlfile = "data12_8TeV.periodAllYear_DetStatus-v49-pro13-03_CoolRunQuery-00-04-08_SMjets.xml" ## A-B studies
#grlfile = "data12_8TeV.periodAllYear_DetStatus-v54-pro13-04_DQDefects-00-00-32_PHYS_StandardGRL_All_Good.xml" ### A-E
grlfile = "data12_8TeV.periodAllYear_DetStatus-v58-pro14-01_DQDefects-00-00-33_PHYS_StandardGRL_All_Good.xml" 
ROOT.gSystem.Load("libGoodRunsLists.so")
reader = ROOT.Root.TGoodRunsListReader()
reader.SetXMLFile(grlfile)
reader.Interpret()
grl = reader.GetMergedGoodRunsList()
############## jet calibration offset tool
if RECALIBRATE:
    assert RECALIBRATE in ["BCH","default","FAST_SIM_BCH","FAST_SIM_default"], "run  : Non configured recalibration: %s"%RECALIBRATE
    
    print "run  : Loading jet calibration tool"
    ROOT.gSystem.Load("ApplyJetCalibration-00-03-02/StandAlone/libApplyJetCalibration.so")
    use_data_calibration = not options.mc
    if "FAST_SIM" in RECALIBRATE: config_suffix ="_AFII"
    else:                         config_suffix =""
    JetCalibrationTool = ROOT.JetCalibrationTool("%s"%JET_TYPE.strip("Jets"),
                                                 "ApplyJetCalibration-00-03-02/data/CalibrationConfigs/JES_Full2012dataset_Preliminary_Jan13%s.config"%config_suffix,
                                                 use_data_calibration)
########## T2L1 Roi parser
if options.slim:
    print "run  : Importing tools needed for slim mode"
    from T2L1_RoIParser import ParseRoIWord
########## setup the output
running_total = 0    
cut_flow = ROOT.TH1D('cut_flow','cut_flow', 101, 0.5, 100.5) # cut flow histogram, this summarises the information in the counters)
treeCopy = ROOT.TTree('qcd','qcd')
print "run  : Made tree to save: ",treeCopy
branch_vectors = []
# ===== make the tree
jet_pt      = ROOT.std.vector( float )()
jet_e       = ROOT.std.vector( float )()
jet_eta     = ROOT.std.vector( float )()
jet_raw_eta = ROOT.std.vector( float )()
jet_phi     = ROOT.std.vector( float )()
jet_y       = ROOT.std.vector( float )()
jet_Badness = ROOT.std.vector( int )()      
jet_isUgly  = ROOT.std.vector( int )()
jet_jvtxf   = ROOT.std.vector( float )()        
jet_origin  = ROOT.std.vector( float )()        
treeCopy._jet_pt      = jet_pt
treeCopy._jet_e       = jet_e
treeCopy._jet_eta     = jet_eta
treeCopy._jet_raw_eta = jet_raw_eta
treeCopy._jet_phi     = jet_phi
treeCopy._jet_y       = jet_y
treeCopy._jet_Badness = jet_Badness
treeCopy._jet_isUgly  = jet_isUgly  
treeCopy._jet_jvtxf   = jet_jvtxf        
treeCopy._jet_origin  = jet_origin
treeCopy.Branch( 'jet_pt', jet_pt)
treeCopy.Branch( 'jet_e', jet_e)
treeCopy.Branch( 'jet_eta', jet_eta)
treeCopy.Branch( 'jet_raw_eta', jet_raw_eta)
treeCopy.Branch( 'jet_phi', jet_phi)
treeCopy.Branch( 'jet_y', jet_y)
treeCopy.Branch( 'jet_Badness', jet_Badness)   
treeCopy.Branch( 'jet_isUgly', jet_isUgly)    
treeCopy.Branch( 'jet_jvtxf', jet_jvtxf)
treeCopy.Branch( 'jet_origin', jet_origin)
branch_vectors.append(jet_pt)
branch_vectors.append(jet_e)
branch_vectors.append(jet_eta)
branch_vectors.append(jet_raw_eta)
branch_vectors.append(jet_phi)
branch_vectors.append(jet_y)
branch_vectors.append(jet_Badness)
branch_vectors.append(jet_isUgly)
branch_vectors.append(jet_jvtxf)
branch_vectors.append(jet_origin)

if options.mc:
    ROOT.gROOT.ProcessLine(\
        "struct EventDataStruct{\
        Int_t lbn;\
        Int_t RunNumber;\
        Int_t EventNumber;\
        Int_t n_pvtx;\
        Int_t good_pvtx;\
        Float_t mu;\
        Int_t mc_channel_number;\
        Float_t event_weight;\
        };")
else:
    ROOT.gROOT.ProcessLine(\
        "struct EventDataStruct{\
        Int_t lbn;\
        Int_t RunNumber;\
        Int_t EventNumber;\
        Int_t n_pvtx;\
        Int_t good_pvtx;\
        Float_t mu;\
        };")
from ROOT import EventDataStruct
struct = EventDataStruct()
treeCopy.Branch( 'lbn', ROOT.AddressOf(struct,'lbn'), "lbn/I")  
treeCopy.Branch( 'RunNumber', ROOT.AddressOf(struct,'RunNumber'), "RunNumber/I")  
treeCopy.Branch( 'EventNumber', ROOT.AddressOf(struct,'EventNumber'), "EventNumber/I")  
treeCopy.Branch( 'n_pvtx', ROOT.AddressOf(struct,'n_pvtx'), "n_pvtx/I")  
treeCopy.Branch( 'good_pvtx', ROOT.AddressOf(struct,'good_pvtx'), "good_pvtx/I")  
treeCopy.Branch( 'mu', ROOT.AddressOf(struct,'mu'), "mu/F")  

## add a trigger passed branch and a prescale branch to the final nTuple      
trigger_vector = ROOT.std.vector( ROOT.std.string )()
treeCopy._trigger_vector = trigger_vector
treeCopy.Branch( 'triggers', trigger_vector )
branch_vectors.append(trigger_vector)


if options.mc:
    print "run  : Adding in truth branches"
    #### Additional Truth information for MC
    truth_jet_pt = ROOT.std.vector( float )()
    truth_jet_eta = ROOT.std.vector( float )()
    truth_jet_phi = ROOT.std.vector( float )()
    truth_jet_e = ROOT.std.vector( float )()
    truth_jet_y = ROOT.std.vector( float )()
    
    treeCopy._truth_jet_pt = truth_jet_pt
    treeCopy._truth_jet_eta = truth_jet_eta
    treeCopy._truth_jet_phi = truth_jet_phi
    treeCopy._truth_jet_e = truth_jet_e
    treeCopy._truth_jet_y = truth_jet_y
    
    treeCopy.Branch( 'truth_jet_pt', truth_jet_pt)
    treeCopy.Branch( 'truth_jet_eta', truth_jet_eta)
    treeCopy.Branch( 'truth_jet_phi', truth_jet_phi)
    treeCopy.Branch( 'truth_jet_e', truth_jet_e)
    treeCopy.Branch( 'truth_jet_y', truth_jet_y)
    
    branch_vectors.append(truth_jet_pt)
    branch_vectors.append(truth_jet_eta)
    branch_vectors.append(truth_jet_phi)
    branch_vectors.append(truth_jet_e)
    branch_vectors.append(truth_jet_y)
    
    treeCopy.Branch( 'mc_channel_number', ROOT.AddressOf(struct,'mc_channel_number'), "mc_channel_number/I")  
    treeCopy.Branch( 'event_weight',      ROOT.AddressOf(struct,'event_weight'),      "event_weight/F")  
    #treeCopy.Branch( 'pileup_weight', ROOT.AddressOf(struct,'pileup_weight'), "pileup_weight/F")  

if options.trigger:
    trigger_emulated_vector = ROOT.std.vector( ROOT.std.string )()
    treeCopy._trigger_emulated_vector = trigger_emulated_vector
    treeCopy.Branch( 'triggers_emulated', trigger_emulated_vector )
    branch_vectors.append(trigger_emulated_vector)
    import TriggerEmulatorD as TE
    trigger_emulator = TE.TriggerEmulatorD(triggers,verbose=options.verbose)
        
trigger_counter_dictionary = {}
trigger_emulated_counter_dictionary = {}
for trigger in triggers:
    trigger_counter_dictionary[trigger] = 0 # [passed]
    trigger_emulated_counter_dictionary[trigger] = 0 # [passed]

################################## Setup output file
print "run  : Adding output tree to an OutputFile using name: ",options.output_file
OutputFile = ROOT.TFile(options.output_file,"RECREATE")

################################## Run analysis
print "run  : === Beginning Analysis"
print "run  : Beginning event loop"
if options.verbose: print_every_n_events = 1
else: print_every_n_events = 100

for event in xrange(nevents):
    cut_flow.Fill(1)    
    chainReader.SetEntry(event)
    #if event < 8200: continue
    
    if tdt.GetEntry(event) <= 0:
        print "run  :   tdt couldn't get entry: ",event
        print "run  :   Run: %i, lb: %i, event number: %i"%\
          (chainReader.ReadBranch("RunNumber"),chainReader.ReadBranch("lbn"),chainReader.ReadBranch("EventNumber"))
        cut_flow.Fill(15)
        continue
   
    if event%print_every_n_events == 0:
        print 'run  : === Event #%i'%(event)
        if options.verbose: 
            print "run  :   Run: %i, lb: %i, event number: %i"%(chainReader.ReadBranch("RunNumber"),chainReader.ReadBranch("lbn"),chainReader.ReadBranch("EventNumber"))
            if options.mc: 
                print "run  :   MC channel number: %i"%(chainReader.ReadBranch("mc_channel_number"))
                print "run  :   event weight:      %f"%chainReader.ReadBranch("mcevt_weight")[0][0]
    
    
    ## Trigger
    overall_pass = False
    trigger_decisions = []
    if options.verbose: print "run  :   Trigger Information"
    for t in triggers:
        trigger_pass = tdt.IsPassed(t,0)
        if options.verbose: print "run  :     %-30s pass: %i"%(t,trigger_pass)
        if trigger_pass:
            trigger_decisions.append(t)
            trigger_counter_dictionary[t]+=1
            if t[:2] == "EF":
                overall_pass = True
    
    if not options.mc:
        DQ_pass=False
        if grlfile:
          if grl.HasRunLumiBlock(chainReader.ReadBranch("RunNumber"),chainReader.ReadBranch("lbn")):
              DQ_pass = True        
        else:
            DQ_pass = True
        if options.verbose: print "run  :   DQ_pass:    %i"%DQ_pass
        if ((not DQ_pass) and (not options.no_grl)): continue    
    cut_flow.Fill(2)
    
    if not (overall_pass or options.mc): continue
    cut_flow.Fill(3)
    
    
    for branch in branch_vectors:
        branch.clear()
    
    for decision in trigger_decisions:
        trigger_vector.push_back(decision)
    
    ## LAr error
    if not options.mc:
        LAr_error = chainReader.ReadBranch("larError")
        if options.verbose: print "run  :   LAr error:  %i"%LAr_error
        if (LAr_error==2): continue
    cut_flow.Fill(4)
     
    ## tile error
    if not options.mc:
        tile_error = chainReader.ReadBranch("tileError")
        if options.verbose: print "run  :   tile error: %i"%tile_error
        if (tile_error==2): continue
    cut_flow.Fill(5)
    
    ## TTC error
    if not options.mc:
        core_flags = chainReader.ReadBranch("coreFlags")
        if options.verbose: print "run  :   core flags: %i"%core_flags
        if ((core_flags&0x40000) != 0): continue
    cut_flow.Fill(6)
     
    ## vertex requirments
    good_verticies = 0
    verticies_for_offset = 0
    verticies = chainReader.ReadBranch("vxp_n")
    if options.verbose: print "run  :   Primary vertex candidates: %i"%verticies
    
    for vertex in range(verticies):
        n_tracks = chainReader.ReadBranch("vxp_nTracks")[vertex]
        if options.verbose: print "run  :      - vertex[%2i]: %3i tracks"%(vertex,n_tracks)
        if ( (vertex==0) and (n_tracks>1) ): good_verticies +=1
        if ( n_tracks>=2 ): verticies_for_offset +=1
    if options.verbose: print "run  :      - good verticies: ",good_verticies
    if options.verbose: print "run  :      - verticies for offset: ",verticies_for_offset
    if not (good_verticies or options.mc): continue    
    cut_flow.Fill(7)
    mu = chainReader.ReadBranch("averageIntPerXing")
    if options.verbose: print "run  :   <mu>: %.2f"%mu
    rho = chainReader.ReadBranch(RHO_NAME)
    if options.verbose: print "run  : %s: %.2f"%(RHO_NAME,rho)
    
    ### These are the final events to be stored
    struct.lbn = chainReader.ReadBranch("lbn")
    struct.RunNumber = chainReader.ReadBranch("RunNumber")
    struct.EventNumber = chainReader.ReadBranch("EventNumber")
    struct.n_pvtx = verticies_for_offset
    struct.good_pvtx = good_verticies
    struct.mu = mu   
    
 
    if options.mc: 
        struct.mc_channel_number = chainReader.ReadBranch("mc_channel_number")
        struct.event_weight = chainReader.ReadBranch("mcevt_weight")[0][0]
        #struct.pileup_weight = 1.
        
    jet_n = len(chainReader.ReadBranch("jet_%s_E"%JET_TYPE))
    jets= []
    if options.verbose: 
        print "run  :  %i jets"%jet_n
        if RECALIBRATE:
            if "FAST_SIM" in RECALIBRATE:   print "run  :    - recalibrating ATL-Fast II jets"
            if "BCH" in RECALIBRATE:        print "run  :    - recalibrating jets with bad channel offset eta JES"
            elif "default" in RECALIBRATE:  print "run  :    - recalibrating jets with offset eta JES"
        else:                           print "run  :    - using out-of-the-box calibration"
    
    for iJet in range(jet_n):          
        cut_flow.Fill(8) 
        if RECALIBRATE:           
            if "BCH" in RECALIBRATE:
                #jet = JetCalibrationTool.ApplyBadChnOffsetEtaJES(\
                    #chainReader.ReadBranch("jet_%s_%s_E"%(JET_TYPE,SCALE))[iJet],
                    #chainReader.ReadBranch("jet_%s_%s_eta"%(JET_TYPE,SCALE))[iJet],
                    #chainReader.ReadBranch("jet_%s_%s_eta"%(JET_TYPE,SCALE))[iJet],
                    #chainReader.ReadBranch("jet_%s_%s_phi"%(JET_TYPE,SCALE))[iJet],
                    #chainReader.ReadBranch("jet_%s_%s_m"%(JET_TYPE,SCALE))[iJet],
                    ##chainReader.ReadBranch("jet_%s_EtaOrigin"%(JET_TYPE))[iJet],
                    ##chainReader.ReadBranch("jet_%s_PhiOrigin"%(JET_TYPE))[iJet],
                    ##chainReader.ReadBranch("jet_%s_MOrigin"%(JET_TYPE))[iJet],
                    #chainReader.ReadBranch("jet_%s_BCH_CORR_CELL"%JET_TYPE)[iJet],
                    #chainReader.ReadBranch("jet_%s_BCH_CORR_JET"%JET_TYPE)[iJet],
                    #mu,
                    #verticies_for_offset)
                #jets.append(jet)
                assert False, "run  : BCH calibration not validated yet for v3"
            elif "default" in RECALIBRATE:
                jet = JetCalibrationTool.ApplyJetAreaOffsetEtaJES(\
                    chainReader.ReadBranch("jet_%s_%s_E"%(JET_TYPE,SCALE))[iJet],
                    chainReader.ReadBranch("jet_%s_%s_eta"%(JET_TYPE,SCALE))[iJet],
                    chainReader.ReadBranch("jet_%s_%s_phi"%(JET_TYPE,SCALE))[iJet],
                    chainReader.ReadBranch("jet_%s_%s_m"%(JET_TYPE,SCALE))[iJet],
                    chainReader.ReadBranch("jet_%s_ActiveAreaPx"%(JET_TYPE))[iJet],
                    chainReader.ReadBranch("jet_%s_ActiveAreaPy"%(JET_TYPE))[iJet],
                    chainReader.ReadBranch("jet_%s_ActiveAreaPz"%(JET_TYPE))[iJet],
                    chainReader.ReadBranch("jet_%s_ActiveAreaE"%(JET_TYPE))[iJet],
                    rho,
                    mu,
                    verticies_for_offset)


                jets.append(jet)
        else:
            jet = ROOT.TLorentzVector()
            jet.SetPtEtaPhiE(chainReader.ReadBranch("jet_%s_pt"%JET_TYPE)[iJet],
                             chainReader.ReadBranch("jet_%s_eta"%JET_TYPE)[iJet],
                             chainReader.ReadBranch("jet_%s_phi"%JET_TYPE)[iJet],
                             chainReader.ReadBranch("jet_%s_E"%JET_TYPE)[iJet])
            jets.append(jet)  ## store jet for kinematic skim
            
        jet_em_pt = chainReader.ReadBranch("jet_%s_%s_pt"%(JET_TYPE,SCALE))[iJet]
        jet_em_e  = chainReader.ReadBranch("jet_%s_%s_E"%(JET_TYPE,SCALE))[iJet]
        jetpt = jet.Pt()
        jete = jet.E()
        jeteta = jet.Eta()
        jetphi = jet.Phi()
        jety = jet.Rapidity()
        
        jetjvtxf = chainReader.ReadBranch("jet_%s_jvtxf"%JET_TYPE)[iJet]
        jetorigin = chainReader.ReadBranch("jet_%s_OriginIndex"%JET_TYPE)[iJet]
        jetugly = chainReader.ReadBranch("jet_%s_isUgly"%JET_TYPE)[iJet]
        
        ### Cleaning
        #larq = chainReader.ReadBranch("jet_%s_LArQuality"%JET_TYPE)[iJet]
        #negE = chainReader.ReadBranch("jet_%s_NegativeE"%JET_TYPE)[iJet]
        emf = chainReader.ReadBranch("jet_%s_emfrac"%JET_TYPE)[iJet]
        #hecf = chainReader.ReadBranch("jet_%s_hecf"%JET_TYPE)[iJet]
        #jet_time = chainReader.ReadBranch("jet_%s_Timing"%JET_TYPE)[iJet]
        fmax = chainReader.ReadBranch("jet_%s_fracSamplingMax"%JET_TYPE)[iJet]
        smax = chainReader.ReadBranch("jet_%s_SamplingMax"%JET_TYPE)[iJet]
        #em_eta = fabs(chainReader.ReadBranch("jet_%s_%s_eta"%JET_TYPE)[iJet])
        sumpttrk = chainReader.ReadBranch("jet_%s_sumPtTrk"%JET_TYPE)[iJet]
        #pt = chainReader.ReadBranch("jet_%s_pt"%JET_TYPE)[iJet]
        
        if jetpt:
            chf = sumpttrk/jetpt
            
        else:
            chf = 0
        #if options.verbose: 
            #print "run  :    - jet[%i]: Pt: %7.2f GeV (em scale: %7.2f), E: %7.2f GeV (em scale: %7.2f), eta: %+.2f, y: %+.2f, phi: %+.2f, ugly: %i"%(iJet,jetpt/1000.,jet_em_pt/1000.,jete/1000.,jet_em_e/1000.,jeteta,jety,jetphi,jetugly)
            #print "run  :           - jvf: %.2f"%jetjvtxf
            #print "run  :           - chf = %.2f/%.2f: %.2f"%(sumpttrk,jetpt,chf)
        #hecq = chainReader.ReadBranch("jet_%s_HECQuality"%JET_TYPE)[iJet]
        #AvgLArQ   = chainReader.ReadBranch("jet_%s_AverageLArQF"%JET_TYPE)[iJet]
        #LArQmean  = AvgLArQ/65535.
            
        jet_pt.push_back(jetpt)
        jet_e.push_back(jete)
        jet_eta.push_back(jeteta)
        jet_raw_eta.push_back(chainReader.ReadBranch("jet_%s_%s_eta"%(JET_TYPE,SCALE))[iJet])
        jet_phi.push_back(jetphi)
        jet_y.push_back(jety)
        jet_jvtxf.push_back(jetjvtxf)
        jet_origin.push_back(jetorigin)
        jetugly = jetugly + Utilities.TileHotSpotCleaning(chainReader.ReadBranch("RunNumber"),jeteta,jetphi,fmax,smax, verbose=False)
        jetugly = jetugly + Utilities.ChfCleaning(jetpt,jeteta,chf,emf,verbose=False)
        jet_isUgly.push_back(jetugly)            
                    
        # === Jet cleaning
        #isBadLooser,isBadLooserReason = Utilities.JetID("LooserBad", larq, negE, emf, hecf, jet_time, fmax, em_eta, chf, hecq, LArQmean)
        #isBadLoose,isBadLooseReason   = Utilities.JetID("LooseBad",  larq, negE, emf, hecf, jet_time, fmax, em_eta, chf, hecq, LArQmean)
        #isBadMedium,isBadMediumReason = Utilities.JetID("MediumBad", larq, negE, emf, hecf, jet_time, fmax, em_eta, chf, hecq, LArQmean)
        #isBadTight,isBadTightReason   = Utilities.JetID("TightBad",  larq, negE, emf, hecf, jet_time, fmax, em_eta, chf, hecq, LArQmean)
        
        isBadLooser = chainReader.ReadBranch("jet_%s_isBadLooseMinus"%JET_TYPE)[iJet]
        isBadLoose  = chainReader.ReadBranch("jet_%s_isBadLoose"%JET_TYPE)[iJet]
        isBadMedium = chainReader.ReadBranch("jet_%s_isBadMedium"%JET_TYPE)[iJet]
        isBadTight  = chainReader.ReadBranch("jet_%s_isBadTight"%JET_TYPE)[iJet]
            
        if isBadLooser:     jet_Badness.push_back(4)
        elif isBadLoose:    jet_Badness.push_back(3)
        elif isBadMedium:   jet_Badness.push_back(2)
        elif isBadTight:    jet_Badness.push_back(1)          
        else:  jet_Badness.push_back(0)
        
        if isBadLooser: cut_flow.Fill(9)
        if isBadLoose:  cut_flow.Fill(10)
        if isBadMedium: cut_flow.Fill(11)
        if isBadTight:  cut_flow.Fill(12)
        if jetugly:     cut_flow.Fill(13)
        
        if options.verbose: 
            if RECALIBRATE:
                print "run  :    - jet[%i]: Pt: %7.2f GeV (em scale: %7.2f), E: %7.2f GeV (em scale: %7.2f), eta: %+.5f (em scale: %.5f), y: %+.2f, phi: %+.2f, ugly: %i"%\
                    (iJet,jetpt/1000.,jet_em_pt/1000.,jete/1000.,jet_em_e/1000.,jeteta,chainReader.ReadBranch("jet_%s_%s_eta"%(JET_TYPE,SCALE))[iJet],jety,jetphi,jetugly)
                print "run  :       - active area x: %.2f, y: %.2f, z: %.2f, E: %.2f, rho: %.2f"%(chainReader.ReadBranch("jet_%s_ActiveAreaPx"%(JET_TYPE))[iJet],
                                                                                                  chainReader.ReadBranch("jet_%s_ActiveAreaPy"%(JET_TYPE))[iJet],
                                                                                                  chainReader.ReadBranch("jet_%s_ActiveAreaPz"%(JET_TYPE))[iJet],
                                                                                                  chainReader.ReadBranch("jet_%s_ActiveAreaE"%(JET_TYPE))[iJet],
                                                                                                  rho)
                print "run  :       - default  Pt: %7.2f GeV eta: %+.2f, phi: %+.2f, Mass: %7.2f GeV"%(chainReader.ReadBranch("jet_%s_pt"%JET_TYPE)[iJet]/1000., chainReader.ReadBranch("jet_%s_eta"%JET_TYPE)[iJet],chainReader.ReadBranch("jet_%s_phi"%JET_TYPE)[iJet], chainReader.ReadBranch("jet_%s_m"%JET_TYPE)[iJet]/1000.)
            else:
                print "run  :    - jet[%i]: Pt: %7.2f GeV (em scale: %7.2f), E: %7.2f GeV (em scale: %7.2f), eta: %+.2f, y: %+.2f, phi: %+.2f, ugly: %i"%(iJet,jetpt/1000.,jet_em_pt/1000.,jete/1000.,jet_em_e/1000.,jeteta,jety,jetphi,jetugly)
            #if isBadLooser:   print "run  :        - bad looser: %s"%isBadLooserReason
            #elif isBadLoose:  print "run  :        - bad loose:  %s"%isBadLooseReason
            #elif isBadMedium: print "run  :        - bad medium: %s"%isBadMediumReason 
            #elif isBadTight:  print "run  :        - bad tight:  %s"%isBadTightReason 
            if isBadLooser:   print "run  :        - bad looser"
            elif isBadLoose:  print "run  :        - bad loose"
            elif isBadMedium: print "run  :        - bad medium" 
            elif isBadTight:  print "run  :        - bad tight" 
            
        
    #if not options.mc:
        #skim_results = Utilities.N_or_more_good_jets(jets,JET_MIN_PT,JET_MAX_Y,MULTIPLICITY)
        #if options.verbose: print "run  : Skimming for %i of more jets, pT > %.2f GeV, |y| < %.2f: "%(MULTIPLICITY, JET_MIN_PT/1000.,JET_MAX_Y),skim_results
        #if not skim_results: continue
    
    
    
    ##stored_entries")[4]+=1   
    ##cut_flow.Fill(4)
    if options.mc:
        if options.verbose: print "run  : Filling truth jet information"
        
        ### Now fill for truth jets
        #print "py: Looking at truth jets now"
        if "AntiKt4" in JET_TYPE:   truth_jet_n = chainReader.ReadBranch("AntiKt4Truth%s_n"%TRUTH_TYPE)
        elif "AntiKt6" in JET_TYPE: truth_jet_n = chainReader.ReadBranch("AntiKt6Truth%s_n"%TRUTH_TYPE)
        if options.verbose: print "run  :  %i truth jets"%truth_jet_n
        truth_pts = []
        for iJet in range(truth_jet_n):          
            cut_flow.Fill(17)
            if "AntiKt4" in JET_TYPE:                      
                truth_jetpt = chainReader.ReadBranch("AntiKt4Truth%s_pt"%TRUTH_TYPE)[iJet]
                truth_jeteta = chainReader.ReadBranch("AntiKt4Truth%s_eta"%TRUTH_TYPE)[iJet]
                truth_jetphi = chainReader.ReadBranch("AntiKt4Truth%s_phi"%TRUTH_TYPE)[iJet]
                truth_jete = chainReader.ReadBranch("AntiKt4Truth%s_E"%TRUTH_TYPE)[iJet]
            elif "AntiKt6" in JET_TYPE:                      
                truth_jetpt = chainReader.ReadBranch("AntiKt6Truth%s_pt"%TRUTH_TYPE)[iJet]
                truth_jeteta = chainReader.ReadBranch("AntiKt6Truth%s_eta"%TRUTH_TYPE)[iJet]
                truth_jetphi = chainReader.ReadBranch("AntiKt6Truth%s_phi"%TRUTH_TYPE)[iJet]
                truth_jete = chainReader.ReadBranch("AntiKt6Truth%s_E"%TRUTH_TYPE)[iJet]
            else: assert False
            
            truth_jet_4V = ROOT.TLorentzVector(0, 0, 0, 0) 
            truth_jet_4V.SetPtEtaPhiE(truth_jetpt,truth_jeteta,truth_jetphi,truth_jete)
            truth_jety = truth_jet_4V.Rapidity()
            
            truth_pts.append(truth_jetpt)

            truth_jet_pt.push_back(truth_jetpt)
            truth_jet_eta.push_back(truth_jeteta)
            truth_jet_phi.push_back(truth_jetphi)
            truth_jet_e.push_back(truth_jete)
            truth_jet_y.push_back(truth_jety)
            
            if options.verbose: 
                print "run  :    - truth jet[%i]: Pt: %7.2f GeV, E: %7.2f GeV, eta: %+3.5f, y: %+.2f, phi: %+.2f"%(iJet,truth_jetpt/1000.,truth_jete/1000.,truth_jeteta,truth_jety,truth_jetphi)
    
    ## MC - skim out events where pileup is too high
    if options.mc and options.pu:
        if options.verbose: print "run  : Checking for too much pileup"   
        good_pileup = Utilities.good_pileup(jets,truth_pts,chainReader.ReadBranch("mcevt_pdf_scale")[0],verbose=options.verbose)
        #assert good_pileup
        if options.verbose: print "run  : Too much pileup: ",good_pileup        
        if not good_pileup: continue
    
    if options.trigger:
        #### get RAW trigger decision for efficiency evaluation
        if options.verbose: print "run  : Saving trigger objects"
        RAW_trigger_decisions = trigger_emulator.EmulateTriggers(chainReader,cut_flow=cut_flow,trigger_decisions=trigger_decisions)
        if options.verbose: 
            print "run  :   Emulated trigger decisions"
            for t in triggers: print "run  :     %-30s pass: %i"%(t,t in RAW_trigger_decisions)
            
        for t in RAW_trigger_decisions:
            trigger_emulated_counter_dictionary[t]+=1
            trigger_emulated_vector.push_back(t)
            
    cut_flow.Fill(14)
    
    if options.verbose: print "run  : Filling treeCopy from entry: ",event
    if options.verbose: print "run  : treeCopy.GetEntries(): ",treeCopy.GetEntries()
    if options.verbose: print "run  : trigger decisions:                  ",trigger_decisions
    #if options.verbose: print "run  : trigger before prescale decisions:  ",TBP_trigger_decisions
    try:
        #if entry%10 == 0:
        treeCopy.Fill()
        if options.verbose: print "run  : treeCopy.Fill succeded, new entries: ",treeCopy.GetEntries()
        #pass
    except:
        print "run  : Error in Tree filling"
        assert False

print "run  : === Done, saving output tree"

print "run  : === Summary"
print "run  :    Events:            %i"%cut_flow.GetBinContent(1)
print "run  :     - corrupt qcd     %i"%cut_flow.GetBinContent(15)
print "run  :     - corrupt qcdMeta %i"%cut_flow.GetBinContent(16)
print "run  :    GRL:               %i"%cut_flow.GetBinContent(2)
print "run  :    Trigger:           %i"%cut_flow.GetBinContent(3)
print "run  :    LAr:               %i"%cut_flow.GetBinContent(4)
print "run  :    tile:              %i"%cut_flow.GetBinContent(5)
print "run  :    ttc:               %i"%cut_flow.GetBinContent(6)
print "run  :    Vertex:            %i"%cut_flow.GetBinContent(7)
print "run  :    Jets:              %i"%cut_flow.GetBinContent(8)
print "run  :       -looser:        %i"%cut_flow.GetBinContent(9)
print "run  :       -loose:         %i"%cut_flow.GetBinContent(10)
print "run  :       -medium:        %i"%cut_flow.GetBinContent(11)
print "run  :       -tight:         %i"%cut_flow.GetBinContent(12)
print "run  :       -ugly:          %i"%cut_flow.GetBinContent(13)
print "run  :    Skim:              %i"%cut_flow.GetBinContent(14)
if options.trigger:
    print "run  :    All L1 jets:       %i"%cut_flow.GetBinContent(18)
    print "run  :    All L2 jets:       %i"%cut_flow.GetBinContent(19)
    print "run  :         - c4cc:       %i"%cut_flow.GetBinContent(20)
    print "run  :         - l2fs:       %i"%cut_flow.GetBinContent(21)
    print "run  :    All EF jets:       %i"%cut_flow.GetBinContent(22)
    print "run  :         - good:       %i"%cut_flow.GetBinContent(23)
if options.mc:
    print "run  :    Truth jets:        %i"%cut_flow.GetBinContent(17)

offset = 24
print "run  : By physics trigger"
for t in triggers:
    print "run  :       - %25s %i"%(t+":",trigger_counter_dictionary[t])
    cut_flow.Fill(offset,trigger_counter_dictionary[t])
    offset+=1
    
print "run  : Emulated trigger"
for t in triggers:
    print "run  :       - %25s %i"%(t+":",trigger_emulated_counter_dictionary[t])
    cut_flow.Fill(offset,trigger_emulated_counter_dictionary[t])
    offset+=1

### Make an outputfile to put this in
print "run  :    Final tree entries: %i"%treeCopy.GetEntries()
treeCopy.Write()
cut_flow.Write()
#OutputFile.Write()
OutputFile.Close()
        

print "run  : === All finished"

    
