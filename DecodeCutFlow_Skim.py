print "\n:: Decode cut flow of an L1.5 Forward Study \n"
#from ROOT import *
print ":: Importing ROOT"
from ROOT import TH1D,TFile,TChain
print ":: done"
from EosTools import make_eos_file_list

############## setup option parser
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file",         help="file to study",        action="store", type="string",  dest="file",    default=False)
parser.add_option("-e", "--eos_folder",   help="eos folder to study",  action="store", type="string",  dest="eos_dir", default=False)
parser.add_option("-r", "--by_run",       help="split study by run",   action="store_true",            dest="by_run",  default=False)
parser.add_option("-t", "--grep_token",   help="token to grep for",    action="store", type="string",  dest="token",   default="")

(options, args) = parser.parse_args()

print ":: Options"
print "   file:         ",options.file
print "   eos folder:   ",options.eos_dir
print "   token:        ",options.token
print "   by run:       ",options.by_run

assert options.file or options.eos_dir, "No file specified, use -f, no eos folder specified, use -e"

print ":: Get cut flow"
if options.file:
    print '\n:: Opening: ',options.file
    root_file = TFile.Open( options.file )    
    assert root_file.IsOpen()
    print ":: Root File "+options.file+" is open"    
    cut_flow = root_file.Get("cut_flow")
    assert cut_flow, "couldn't get cut flow"
    #chain = TChain("qcd")
    #chain.Add(root_file)
    #n_entries = chain.GetEntries()
    
    
else:
    file_list = make_eos_file_list(options.eos_dir,grep=options.token)
    print "Got %i files from eos"%len(file_list)
    cut_flow = False
    for file in file_list:
        
        if not cut_flow:
            first_root_file = TFile.Open( "root://eosatlas/"+file )    
            assert first_root_file.IsOpen()
            print "   - root file "+file+" is open"
            cut_flow = first_root_file.Get("cut_flow").Clone("compressed_cut_flow")
            #first_chain = TChain("qcd")
            #first_chain.Add("root://eosatlas/"+file)
            #n_entries =first_chain.GetEntries()
        else:
            root_file = TFile.Open( "root://eosatlas/"+file )    
            assert root_file.IsOpen()
            print "   - root file "+file+" is open"
            cut_flow.Add(root_file.Get("cut_flow"))
            chain = TChain("qcd")
           # #chain.Add("root://eosatlas/"+file)
            #n_entries+=chain.GetEntries()
            #root_file.Close()
            
#print "\n=== Raw cut flow"
#for i in range(cut_flow.GetNbinsX()+1):
    #print "Bin[%2i]: %i"%(i,cut_flow.GetBinContent(i))
offset = 1
print "\n=== Summary"
#print "    Entries:           %i"%n_entries
print "    Events:            %i"%cut_flow.GetBinContent(1)
print "     - corrupt qcd     %i"%cut_flow.GetBinContent(13)
print "     - corrupt qcdMeta %i"%cut_flow.GetBinContent(14)
print "    GRL:               %i"%cut_flow.GetBinContent(2)
print "    Trigger:           %i"%cut_flow.GetBinContent(3)
print "    LAr:               %i"%cut_flow.GetBinContent(4)
print "    Vertex:            %i"%cut_flow.GetBinContent(5)
print "    Jets:              %i"%cut_flow.GetBinContent(6)
print "       -looser:        %i"%cut_flow.GetBinContent(7)
print "       -loose:         %i"%cut_flow.GetBinContent(8)
print "       -medium:        %i"%cut_flow.GetBinContent(9)
print "       -tight:         %i"%cut_flow.GetBinContent(10)
print "       -ugly:          %i"%cut_flow.GetBinContent(11)
print "    Skim:              %i"%cut_flow.GetBinContent(12)
print "    Truth jets:        %i"%cut_flow.GetBinContent(15)

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

cut_flow_offset = 16
print " By physics trigger"
for t in triggers:
    print "       - %20s %i"%(t+":",cut_flow.GetBinContent(cut_flow_offset))    
    cut_flow_offset+=1
    
print " RAW trigger"
for t in triggers:
    print "       - %20s %i"%(t+":",cut_flow.GetBinContent(cut_flow_offset))    
    cut_flow_offset+=1



