from math import cosh,fabs

def GetL2EFThreshold(name):
    if name[3] != "j":
        multiplicity = float(name.split("_")[1][0])
        threshold = float(name.split("_")[1][2:])
    else:
        multiplicity = 1
        threshold = float(name.split("_")[1][1:])
    return threshold,multiplicity

def GetEFHTInclusiveThreshold(name):
    # e.g. EF_j170_a4tchad_ht700
    return float(name.split("_")[1][1:])

def GetEFHTHTThreshold(name):
    return float(name.split("_")[3][2:])
    
trigger_configurations = {
            ### L2
            "L2_j140_c4cchad"       :"L1_J75",
            "L2_j165_c4cchad"       :"L1_J75",
            ### EF
          
            "EF_j240_a10tcem"      :"L2_j165_c4cchad",
            "EF_j360_a10tcem"      :"L2_j165_c4cchad",
          
}


class TriggerEmulatorD:
    def __init__ (self,triggers,verbose=False):
        self.triggers = triggers
        self.verbose = verbose
        print "TE   : === Initalising trigger emulator"
        print "TE   :     Triggers:"
        for t in self.triggers:
            print "TE   :        - %s"%t
            if t[:2]!="L1":
                assert t in trigger_configurations.keys(), "TE   : trigger %s has no configuration information"%t
        print "TE   :    verbose:   ",self.verbose
        pass
    
    def EmulateTriggers(self,chainReader,cut_flow=False, trigger_decisions=False):
        if self.verbose: print "TE   : === EmulateTriggers"
        passed_triggers = []
        ### loop over (and print) the trigger objects
        good_l2_jets = []
        good_ef_jets = []
        ### L1 objects
        n_l1_rois = chainReader.ReadBranch("trig_L1_jet_n")
        if self.verbose: print "TE   : %i L1 jets:"%n_l1_rois
        for i_l1 in range(n_l1_rois):
            roi_word = chainReader.ReadBranch("trig_L1_jet_RoIWord")[i_l1]
            et = chainReader.ReadBranch("trig_L1_jet_et8x8")[i_l1]/1000.
            if cut_flow: cut_flow.Fill(18)
            thresholds = chainReader.ReadBranch("trig_L1_jet_thrNames")[i_l1]
            if self.verbose: print "TE   :    - l1 jet[%2i]: Et: %7.2f GeV, eta: %+5.2f, phi: %+5.2f, roi word: %s,"%\
                (i_l1,et,chainReader.ReadBranch("trig_L1_jet_eta")[i_l1],chainReader.ReadBranch("trig_L1_jet_phi")[i_l1],roi_word),
            if self.verbose: print "thresholds: ",[t for t in thresholds]
        
        ### L2 objects
        n_t2calo_rois = chainReader.ReadBranch("trig_L2_jet_n")
        if self.verbose: print "TE   : %i T2Calo jets:"%n_t2calo_rois
        for i_l2 in range(n_t2calo_rois):
            roi_word = str(chainReader.ReadBranch("trig_L2_jet_RoIWord")[i_l2])
            et = float(chainReader.ReadBranch("trig_L2_jet_E")[i_l2])/float(cosh(chainReader.ReadBranch("trig_L2_jet_eta")[i_l2]))
            input_roi_type = chainReader.ReadBranch("trig_L2_jet_InputType")[i_l2]
            output_roi_type = chainReader.ReadBranch("trig_L2_jet_OutputType")[i_l2]
            counter = chainReader.ReadBranch("trig_L2_jet_counter")[i_l2]
            is_had = chainReader.ReadBranch("trig_L2_jet_c4cchad")[i_l2]
                
            if cut_flow: cut_flow.Fill(19)
            if self.verbose: print "TE   :    - t2calo jet[%2i]: Et: %7.2f GeV, eta: %+5.2f, phi: %+5.2f, roi word: %s, input type: %12s, output type: %12s, counter: %i, l2 c4cc had: %i"%\
                (i_l2,float(et)/1000.,chainReader.ReadBranch("trig_L2_jet_eta")[i_l2],chainReader.ReadBranch("trig_L2_jet_phi")[i_l2],roi_word,input_roi_type,output_roi_type,counter,is_had),
        
            if (is_had and (input_roi_type == "NON_L15")): 
                if self.verbose: print "- good"
                if cut_flow: cut_flow.Fill(20)
                good_l2_jets.append(i_l2)
                continue
            if self.verbose: print ""
        ## EF objects
        n_EF_rois = chainReader.ReadBranch("trig_EF_jet_n")
        if self.verbose: print "TE   : %i EF jets:"%n_EF_rois
        for i_ef in range(n_EF_rois):
            et = float(chainReader.ReadBranch("trig_EF_jet_E")[i_ef])/float(cosh(chainReader.ReadBranch("trig_EF_jet_eta")[i_ef]))
            calibration = chainReader.ReadBranch("trig_EF_jet_calibtags")[i_ef]
            if cut_flow: cut_flow.Fill(22)
            if self.verbose: print "TE   :    - EF jet[%2i]: Et: %7.2f GeV, eta: %+5.2f, phi: %+5.2f, calibration: %s"%\
            (i_ef,float(et)/1000.,chainReader.ReadBranch("trig_EF_jet_eta")[i_ef],chainReader.ReadBranch("trig_EF_jet_phi")[i_ef],calibration),
            if not (calibration == "AntiKt10_topo"): 
                if self.verbose: print ""
                continue
            if self.verbose: print "- good"
            good_ef_jets.append(i_ef)
        
        if self.verbose:
            print "TE   : Found %i good L2 jets:"%len(good_l2_jets),good_l2_jets
            print "TE   : Found %i good EF jets:"%len(good_ef_jets),good_ef_jets
        passed_L1_rois = {}
        ### L1 is easy just check if the name is in the RAW passed triggers
        for t in self.triggers: 
            if t[:2] != "L1": continue
            if self.verbose: print "TE   : === Checking trigger %s"%t
            for i_l1 in range(n_l1_rois):
                roi_word   = chainReader.ReadBranch("trig_L1_jet_RoIWord")[i_l1]
                thresholds = chainReader.ReadBranch("trig_L1_jet_thrNames")[i_l1]
                if t[3:] in thresholds:
                    if t not in passed_triggers: passed_triggers.append(t)
                    if t not in passed_L1_rois.keys(): passed_L1_rois[t] = []
                    passed_L1_rois[t].append(roi_word)
                    if self.verbose: print "TE   :      - passed by L1 jet %i"%i_l1
                    
        ### L2 now have to check the L1 and the l2 objects:
        for t in self.triggers: 
            if t[:2] != "L2": continue
            if self.verbose: print "TE   : === Checking trigger %s"%t
            ### check if L1 has passed
            if trigger_configurations[t] not in passed_triggers: continue
            
            threshold, multiplicity = GetL2EFThreshold(t)
            this_multiplicity = 0
            for i_l2 in good_l2_jets:
                et  = float(chainReader.ReadBranch("trig_L2_jet_E")[i_l2])/float(cosh(chainReader.ReadBranch("trig_L2_jet_eta")[i_l2]))
                eta = chainReader.ReadBranch("trig_L2_jet_eta")[i_l2]
                roi_word = chainReader.ReadBranch("trig_L2_jet_RoIWord")[i_l2]
                if fabs(eta) > 3.2: continue
                if et/1000. < threshold: continue
                if trigger_configurations[t] not in passed_L1_rois.keys(): continue
                if roi_word in passed_L1_rois[trigger_configurations[t]]:
                    this_multiplicity+=1
                if this_multiplicity >= multiplicity:
                    passed_triggers.append(t)
                    if self.verbose: print "TE   :      - passed by L2 jet %i"%i_l2
                    break
        
        ### EF now have to check the L2 pass and the EF objects:
        for t in self.triggers: 
            if t[:2] != "EF": continue
            if self.verbose: print "TE   : === Checking trigger %s"%t
            ### check if L2 has passed
            if trigger_configurations[t] not in passed_triggers: continue
            if "_ht" in t:
                if self.verbose: print "TE   :  HT trigger: %s"%t
                #print "testing HT trigger: %s"%t
                inclusive_threshold = GetEFHTInclusiveThreshold(t)
                HT_threshold        = GetEFHTHTThreshold(t)
                inclusive_threshold_passed = False
                both_passed = False
                trigger_HT = 0.
                for i_ef in good_ef_jets:
                    et = float(chainReader.ReadBranch("trig_EF_jet_E")[i_ef])/float(cosh(chainReader.ReadBranch("trig_EF_jet_eta")[i_ef]))
                    eta = chainReader.ReadBranch("trig_EF_jet_eta")[i_ef]
                    if fabs(eta) > 3.2: continue
                    if et/1000. > inclusive_threshold: inclusive_threshold_passed = True
                    if ((et/1000.) < 45.): continue   
                    trigger_HT+=(et/1000.)
                    if trigger_HT > HT_threshold:
                        if inclusive_threshold_passed: both_passed = True
                #print HT
                if both_passed:
                    passed_triggers.append(t)
                    #print "passed now"
                if self.verbose: print "TE   :  HT: %.2f GeV, passed: "%trigger_HT,both_passed
            else:
                threshold, multiplicity = GetL2EFThreshold(t)
                this_multiplicity = 0
                for i_ef in good_ef_jets:
                    et = float(chainReader.ReadBranch("trig_EF_jet_E")[i_ef])/float(cosh(chainReader.ReadBranch("trig_EF_jet_eta")[i_ef]))
                    eta = chainReader.ReadBranch("trig_EF_jet_eta")[i_ef]
                    if fabs(eta) > 3.2: continue
                    if et/1000. > threshold:
                        this_multiplicity+=1
                    if this_multiplicity >= multiplicity:
                        passed_triggers.append(t)
                        if self.verbose: print "TE   :      - passed by EF jet %i"%i_ef
                        break
        
        if self.verbose:
            print "TE   :  Triggers that could have passed: "
            l1 = [a for a in passed_triggers if a[:2]=="L1"]
            l2 = [a for a in passed_triggers if a[:2]=="L2"]
            ef = [a for a in passed_triggers if a[:2]=="EF"]
            l1.sort()
            l2.sort()
            ef.sort()
            print "TE   :  L1: ",l1
            print "TE   :  L2: ",l2
            print "TE   :  EF: ",ef
        
        # cross check against EF_j360
        if trigger_decisions:
            triggers_to_check = ["EF_j360_a4tchad","EF_3j170_a4tchad_L1J75"]
            triggers_to_check = []
            if self.verbose: print "TE   : Validating vs: ",triggers_to_check
            for t in triggers_to_check:
                if t in passed_triggers:      assert t in trigger_decisions, "TE   : trigger %s emulated but not passed"%t
                if t not in passed_triggers:  assert t not in trigger_decisions, "TE   : trigger %s passed but not emulated"%t
        
        
        return passed_triggers
