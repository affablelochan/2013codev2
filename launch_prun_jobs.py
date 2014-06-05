print "\nrun  : launch prun jobs \n"
import os

############## setup option parser
from optparse import OptionParser
parser = OptionParser()
### input options
parser.add_option("-f", "--filelist",       help="input file list",                         action="store", type="string",  dest="file_list",      default=False)
parser.add_option("-t", "--token",          help="input grep token",                        action="store", type="string",  dest="token",          default=False)
parser.add_option("-d", "--dataset",        help="the type of dataset to use",              action="store", type="string",  dest="dataset",        default=False)
### runtime options
parser.add_option("-n", "--number_of_files",help="only run over a certain number of files", action="store", type="int",     dest="n_files",        default=False)
parser.add_option("-s", "--submit_mode",    help="turn on submit mode",                     action="store_true",            dest="submit",         default=False)
#parser.add_option("-m", "--mc_mode",        help="turn on MC mode",                         action="store_true",            dest="mc",             default=False)

(options, args) = parser.parse_args()

print "run  : === Options"
print "run  : Input options:"
print "run  :    file list:       ",options.file_list
print "run  :    token:           ",options.token
print "run  :    dataset:         ",options.dataset
print "run  : Runtime options:"
print "run  :    number of files: ",options.n_files
#print "run  :    mc mode:         ",options.mc
print "run  :    submit mode:     ",options.submit

assert options.dataset, "No dataset given, this is used to configure th prun options, use -d to specify"
assert options.dataset in [
                           #"JZX", "JZX_LC",
                           #"JZXW",
                           "JZXW_LC", "JZXW_LC_SMQCD",
                           #"data",
                           #"c_data","s_data",
                           "data_LC",
                           "data_LC_SMQCD",
                           #"HERWIG",
                           "HERWIG_LC",
                           "HERWIG_LC_SMQCD",
                           ],\
                           "This dataset %s is not configured"%options.dataset

includes = "./libGoodRunsLists.so,./libTrigRootAnalysis.so,./ApplyJetCalibration-00-03-02/Root/ApplyJetCalibration.o,./ApplyJetCalibration-00-03-02/StandAlone/ApplyJetCalibrationCint.o,./ApplyJetCalibration-00-03-02/StandAlone/libApplyJetCalibration.so,./ApplyJetCalibration-00-03-02/data/CalibrationConfigs/JES_Full2012dataset_Preliminary_Jan13.config,./ApplyJetCalibration-00-03-02/data/CalibrationFactors/AbsoluteJES_Rel17.2_AreaSubtracted_0.config,./ApplyJetCalibration-00-03-02/data/InsituCalibration/InsituCalibration_Dec21_2012.root"

base_commands = {
    #"JZX"       :   "prun --exec 'python Skimmer_2012.py -i %%IN -o dpd-%s.root -m -p -t -r BCH' --inDS %s --outDS user.tamsett.mc12_JZX_antikt_6_EMJES_pileup_cut_09012013 --outputs dpd-%s.root --nFilesPerJob 1 --athenaTag=17.2.4 --noBuild --extFile %s",
    #"JZX_LC"    :   "prun --exec 'python Skimmer_2012.py -i %%IN -o dpd-%s.root -m -p -t -r BCH -j AntiKt6LCTopo' --inDS %s --outDS user.tamsett.mc12_JZX_antikt_6_LCJES_pileup_cut_10012013 --outputs dpd-%s.root --nFilesPerJob 1 --athenaTag=17.2.4 --noBuild --extFile %s",
    #"JZXW"      :   "prun --exec 'python Skimmer_2012.py -i %%IN -o dpd-%s.root -m -p -t -r BCH' --inDS %s --outDS user.tamsett.mc12_JZXW_antikt_6_EMJES_pileup_cut_18122012_v2 --outputs dpd-%s.root --nFilesPerJob 1 --athenaTag=17.2.4 --noBuild --extFile %s --site SLACXRD_PHYS-SM",
    "JZXW_LC"           :   "prun --exec 'python Skimmer_2013.py -i %%IN -o dpd-%s.root -m -p -j AntiKt6LCTopo' --inDS %s --outDS user.tamsett.mc12_JZXW_antikt_6_LCJES_pileup_cut_23012013_from_JETMET_p1344 --outputs dpd-%s.root --nFilesPerJob 4 --athenaTag=17.2.4 --noBuild --extFile %s",
    "JZXW_LC_SMQCD"     :   "prun --exec 'python Skimmer_2013.py -i %%IN -o dpd-%s.root -m -p -j AntiKt6LCTopo' --inDS %s --outDS user.tamsett.mc12_JZXW_antikt_6_LCJES_pileup_cut_23012013_from_SMQCD_p1344 --outputs dpd-%s.root --nFilesPerJob 4 --athenaTag=17.2.4 --noBuild --extFile %s",
    #"HERWIG"    :   "prun --exec 'python Skimmer_2012.py -i %%IN -o dpd-%s.root -m -p -t -r BCH' --inDS %s --outDS user.tamsett.mc12_Herwig_JZXW_antikt_6_EMJES_pileup_cut_18122012 --outputs dpd-%s.root --nFilesPerJob 1 --athenaTag=17.2.4 --noBuild --extFile %s",
    "HERWIG_LC"         :   "prun --exec 'python Skimmer_2013.py -i %%IN -o dpd-%s.root -m -p -j AntiKt6LCTopo' --inDS %s --outDS user.tamsett.mc12_herwig_JZXW_antikt_6_LCJES_pileup_cut_23012013_from_JETMET_p1344 --outputs dpd-%s.root --nFilesPerJob 10 --athenaTag=17.2.4 --noBuild --extFile %s",
    "HERWIG_LC_SMQCD"   :   "prun --exec 'python Skimmer_2013.py -i %%IN -o dpd-%s.root -m -p -j AntiKt6LCTopo' --inDS %s --outDS user.tamsett.mc12_herwig_JZXW_antikt_6_LCJES_pileup_cut_23012013_from_SMQCD_p1344 --outputs dpd-%s.root --nFilesPerJob 10 --athenaTag=17.2.4 --noBuild --extFile %s",
    #"data"      :   "prun --exec 'python Skimmer_2012.py -i %%IN -o dpd-%s.root -t -r BCH' --inDS %s --outDS user.tamsett.data12_A-E_antikt_6_EMJES_09012013_from_JETMET_p1230 --outputs dpd-%s.root --nFilesPerJob 1 --athenaTag=17.2.4 --noBuild --extFile %s",
    "data_LC"           :   "prun --exec 'python Skimmer_2013.py -i %%IN -o dpd-%s.root -j AntiKt6LCTopo' --inDS %s --outDS user.tamsett.data12_%s_antikt_6_LCJES_23012013_from_JETMET_p1344 --outputs dpd-%s.root --nFilesPerJob 1 --athenaTag=17.2.4 --noBuild --extFile %s --mergeOutput",
    "data_LC_SMQCD"     :   "prun --exec 'python Skimmer_2013.py -i %%IN -o dpd-%s.root -j AntiKt6LCTopo' --inDS %s --outDS user.tamsett.data12_%s_antikt_6_LCJES_23012013_from_SMQCD_p1344 --outputs dpd-%s.root --nFilesPerJob 1 --athenaTag=17.2.4 --noBuild --extFile %s --mergeOutput",
    #"s_data"    :   "prun --exec 'python Skimmer_2012.py -i %%IN -o dpd-%s.root -r BCH' --inDS %s --outDS user.tamsett.data12_A-E_antikt_6_EMJES_pileup_cut_no_trigger_28122012 --outputs dpd-%s.root --nFilesPerJob 1 --athenaTag=17.2.4 --noBuild --extFile %s",
    #"c_data"    :   "prun --exec 'python Skimmer_2012.py -i %%IN -o dpd.root -t -r BCH' --inDS %s --outDS user.tamsett.data12_%s_antikt_6_EMJES_pileup_cut_19122012 --outputs dpd.root --nFilesPerJob 1 --athenaTag=17.2.4 --noBuild --extFile %s",
}
#if options.mc: options_string = "-m -p "
#else:          options_string = ""

tmp_files = open(options.file_list,"r").readlines()
files = []
for tmp_file in tmp_files:
    if tmp_file[0] == "#": continue
    files.append(tmp_file)
    
print "run  : found %i files"%len(files)
for i,file in enumerate(files):
    print "run  :     - %s"%file.strip()

if options.token:
    print "run  : Only using files matching token: %s"%options.token
    final_files = []
    for file in files: 
        if options.token in file: 
            final_files.append(file)
            print "run  :     - %s"%file.strip()
    files = final_files
    print "run  : using %i files"%len(files)
    
n_all = len(files)
if options.n_files: n_all = options.n_files

print "run  : === Submitting"
for i,file in enumerate(files):
    if options.n_files and (i >= options.n_files): break
    print "\nrun  : === file[%i/%i]: %s"%(i+1,len(files),file.strip())
    if options.dataset == "s_data": id = file.split(".")[4]
    else:                           id = file.split(".")[1]
    #command = "prun --exec 'python Skimmer_2012.py -i %%IN -o dpd-%s.root %s-t -r BCH' --inDS %s --outDS user.tamsett.mc12_JZX_antikt_6_EMJES_pileup_cut_origin_09112012 --outputs dpd-%s.root --nFilesPerJob 1 --mergeOutput --athenaTag=AtlasProduction,16.6.5.1 --noBuild --extFile ./libGoodRunsLists.so,./libTrigRootAnalysis.so,./ApplyJetCalibration-00-02-07/Root/ApplyJetCalibration.o,./ApplyJetCalibration-00-02-07/StandAlone/ApplyJetCalibrationCint.o,./ApplyJetCalibration-00-02-07/StandAlone/libApplyJetCalibration.so,./ApplyJetCalibration-00-02-07/data/InsituCalibration/InsituCalibration_July7_2012.root --site SLACXRD_PHYS-SM"%\
    #command = "prun --exec 'python Skimmer_2012.py -i %%IN -o dpd-%s.root %s-t' --inDS %s --outDS user.tamsett.mc12_JZXW_fast_sim_antikt_6_EMJES_pileup_cut_17112012 --outputs dpd-%s.root --nFilesPerJob 1 --athenaTag=AtlasProduction,16.6.5.1 --noBuild --extFile ./libGoodRunsLists.so,./libTrigRootAnalysis.so,./ApplyJetCalibration-00-02-07/Root/ApplyJetCalibration.o,./ApplyJetCalibration-00-02-07/StandAlone/ApplyJetCalibrationCint.o,./ApplyJetCalibration-00-02-07/StandAlone/libApplyJetCalibration.so,./ApplyJetCalibration-00-02-07/data/InsituCalibration/InsituCalibration_July7_2012.root"%\
    if "data" in options.dataset:
        command = base_commands[options.dataset]%(id,file.strip(),id,id,includes)
    else:
        command = base_commands[options.dataset]%(id,file.strip(),id,includes)
    
    print "run  :   - %s"%command
    if options.submit:
        print "run  :   - submitting"
        os.system(command)

print "run  : === Done"
print "run  :   submitted %i/%i jobs"%(n_all,len(files))
if not options.submit:
    print "run  :   - but nothing was really done"

print "\n"
