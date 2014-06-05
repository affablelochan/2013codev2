from math import sqrt,fabs

class DQ(object):
    def __init__(self,grlfile,verbose=False):
        self.grlfile = grlfile
        self.verbose = verbose
        print "utils: === Initialising DQ"
        print "utils:    grl:       ",self.grlfile
        print "utils:    verbose:   ",self.verbose
    
    
        from xml.dom.minidom import parse, parseString
        xmlfile=open(grlfile)
        xmldata=xmlfile.read()
        xmlfile.close()
        dom1 = parseString(xmldata)
        self.DQ="( (run_number<140000) "  # for MC
        for i in dom1.getElementsByTagName("LumiBlockCollection"):
          for j in i.childNodes:
            try:
              if j.tagName=="Run":
                RUN=j.childNodes[0].data
              elif j.tagName=='LBRange':
                self.DQ+=" or (run_number==%s and (lumi_block>=%s and lumi_block<=%s))" % (RUN,j.getAttribute("Start"),j.getAttribute("End"))
            except AttributeError: pass
        dom1.unlink()
        self.DQ+=" )"
        print "utils: DQ setup"
        
    def test_event(self,run_number,lumi_block,event_number):
        if self.verbose:
            print "utils: Evaluating DQ"
            print "utils:    run number:    ",run_number
            print "utils:    lumi block:    ",lumi_block
            print "utils:    event number:  ",event_number
        passDQ = eval(self.DQ)
        
        if self.verbose: print "utils: DQ: ",passDQ
        return passDQ

def JetID(criteria,
          larq,     # LAr quality
          negE,     #in MeV
          emf, 
          hecf, 
          time,     #in ns
          fmax, 
          eta,      #emscale Eta 
          chf, 
          hecq, 
          LArQmean
          ):

    if(criteria=="LooserBad" or criteria=="LooseBad" or criteria=="MediumBad" or criteria=="TightBad"):
        #HEC spikes
        if(hecf>0.5 and fabs(hecq)>0.5 and LArQmean>0.8):  return True,"HEC spikes: hecf[%.2f]>0.5 and fabs(hecq[%.2f])>0.5 and LArQmean[%.2f]>0.8"%(hecf,hecq,LArQmean)
        if(fabs(negE)>60000.):                             return True,"HEC spikes: fabs(negE[%.2f])>60000."%(negE)
        #EM coherent noise
        if(emf>0.95 and fabs(larq)>0.8 and 
           LArQmean>0.8 and fabs(eta)<2.8 ):               return True,"EM coherent noise: emf[%.2f]>0.95 and fabs(larq[%.2f])>0.8 and LArQmean[%.2f]>0.8 and fabs(eta[%.2f])<2.8 "%(emf,larq,LArQmean,eta)
        #Non-collision background & cosmics
        if(emf<0.05 and chf<0.05 and fabs(eta)<2):         return True,"Non-collision background & cosmics: emf[%.2f]<0.05 and chf[%.2f]<0.05 and fabs(eta[%.2f])<2"%(emf,chf,eta)
        if(emf<0.05 and fabs(eta)>=2):                      return True,"Non-collision background & cosmics: emf[%.2f]<0.05 and fabs(eta[%.2f])>=2"%(emf,eta)
        if(fmax>0.99 and fabs(eta)<2):                     return True,"Non-collision background & cosmics: fmax[%.2f]>0.99 and fabs(eta[%.2f])<2"%(fmax,eta)
    
    if(criteria=="LooseBad" or criteria=="MediumBad" or criteria=="TightBad"):
        #HEC spikes
        if(hecf>0.5 and fabs(hecq)>0.5):                   return True,"HEC spikes: hecf[%.2f]>0.5 and fabs(hecq[%.2f])>0.5"%(hecf,hecq)
        #EM coherent noise
        if(emf>0.95 and fabs(larq)>0.8 and fabs(eta)<2.8): return True,"EM coherent noise: emf[%.2f]>0.95 and fabs(larq[%.2f])>0.8 and fabs(eta[%.2f])<2.8"%(emf,larq,eta)
        #Non-collision background & cosmics
        if(fabs(time)>25):                                 return True,"Non-collision background & cosmics: fabs(time[%.2f])>25"%time
    
    if(criteria=="MediumBad" or criteria=="TightBad"):
        #HEC spikes
        if(hecf>1-fabs(hecq)):                           return True,"HEC spikes: hecf[%.2f]>1-fabs(hecq[%.2f])"%(hecf,hecq)
        #EM coherent noise
        if(emf>0.9 and fabs(larq)>0.8 and fabs(eta)<2.8):return True,"EM coherent noise: emf[%.2f]>0.9 and fabs(larq[%.2f])>0.8 and fabs(eta[%.2f])<2.8"%(emf,larq,eta)
        #Non-collision background & cosmics
        if(fabs(time)>10):                               return True,"Non-collision background & cosmics: fabs(time[%.2f])>10"%(time)
        if(emf<0.05 and chf<0.1 and fabs(eta)<2):        return True,"Non-collision background & cosmics: emf[%.2f]<0.05 and chf[%.2f]<0.1 and fabs(eta[%.2f])<2"%(emf,chf,eta)
        if(emf>0.95 and chf<0.05 and fabs(eta)<2):       return True,"Non-collision background & cosmics: emf[%.2f]>0.95 and chf[%.2f]<0.05 and fabs(eta[%.2f])<2"%(emf,chf,eta)
    
    if(criteria=="TightBad"):
        #EM coherent noise
        if(fabs(larq)>0.95):                             return True,"EM coherent noise: fabs(larq[%.2f])>0.95"%(larq)
        if(emf>0.98 and fabs(larq)>0.05):                return True,"EM coherent noise: emf[%.2f]>0.98 and fabs(larq[%.2f])>0.05"%(emf,larq)
        #Non-collision background & cosmics
        if(emf<0.1 and chf<0.2 and fabs(eta)<2.5):       return True,"Non-collision background & cosmics: emf[%.2f]<0.1 and chf[%.2f]<0.2 and fabs(eta[%.2f])<2.5"%(emf,chf,eta)
        if(emf>0.9 and chf<0.1 and fabs(eta)<2.5):       return True,"Non-collision background & cosmics: emf[%.2f]>0.9 and chf[%.2f]<0.1 and fabs(eta[%.2f])<2.5"%(emf,chf,eta)
        if(chf<0.01 and fabs(eta)<2.5):                  return True,"Non-collision background & cosmics: chf[%.2f]<0.01 and fabs(eta[%.2f])<2.5"%(chf,eta)
        if(emf<0.1 and fabs(eta)>2.5 ):                  return True,"Non-collision background & cosmics: emf[%.2f]<0.1 and fabs(eta[%.2f])>2.5" %(emf,eta)
    

    return False,"clean"
    

def N_or_more_good_jets(jets,JET_MIN_PT,JET_MAX_Y,MULTIPLICITY):
    good_jets = 0
    for jet in jets:
        if ( (fabs(jet.Rapidity()) < JET_MAX_Y) and (jet.Pt() > JET_MIN_PT) ):
            good_jets+=1
    return good_jets>(MULTIPLICITY-1)

def good_pileup(reco_jets,truth_pts,mcevt_pdf_scale,verbose=False):
    # - based on instructions from: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/ExoticDijetsFull2011#Veto_events_with_too_high_pile_u
        # Some dijet events, especially those in the lower JX samples, have been generated with pile-up that is too high 
        # compared to the primary event itself. A way to veto these events is to compare the reco jets with truth jets properties. 
        # More specifically you can only accept the event if:
        # pTavg < 2*maxTruthJetPt AND
        # pTavg < 2.5*pThat 
        # pTavg is the average dijet pT of the reco jets, maxTruthJetPt is the maximum truth pT running over the AntiKt6(4)TruthNew container and pThat is the pT of the LO hard scattering diagram which is found by:
        # mcevt_pdf_scale->at(0)*1000.; 
        # The factor 1000 comes from the fact that this variable is in GeV while all other jet pTs are in MeV.
        reco_pts = []
        for jet in reco_jets: reco_pts.append(jet.Pt())
        reco_pts.sort(reverse=True)
        if verbose: print "utils:  sorted reco pts: ", ["%.2f"%r for r in reco_pts]
        if len(reco_pts) < 2:
            if verbose: print "utils:  there aren't two reco jets so can't comment on this event"
            return True
            
        average_dijet_pt = (reco_pts[0]+reco_pts[1]) / 2.
        if verbose: print "utils:  average reco dijet pT: ",average_dijet_pt
        
        truth_pts.sort(reverse=True)
        if verbose: print "utils:  sorted truth pts: ", ["%.2f"%r for r in truth_pts]
        
        if len(truth_pts) < 1:
            if verbose: print "utils:  there aren't any truth jets so assuming this event is bad"
            return False
            
        if verbose: print "utils:  is average dijet pt: %.2f GeV >= 2*maximum truth pt: %.2f GeV"%(average_dijet_pt/1000.,2*truth_pts[0]/1000.)
        if (average_dijet_pt >= (2*truth_pts[0])):
            if verbose: print "utils:    - yes, therefore a bad event"
            return False
        if verbose: print "utils:    - no"
        
        pt_hat = mcevt_pdf_scale*1000.
        if verbose: print "utils:  pT hat: ",pt_hat
        
        if verbose: print "utils:  is average dijet pt: %.2f GeV >= 2.5*pT hat: %.2f GeV"%(average_dijet_pt/1000.,2.5*pt_hat/1000.)
        if (average_dijet_pt >= (2.5*pt_hat)):
            if verbose: print "utils:    - yes, therefore a bad event"
            return False
        if verbose: print "utils:    - no"
        #assert False
        return True
        
    
def ChfAndTileHotSpotCleaning(RunNumber, eta, phi, fmax, smax, pt, chf, emf, verbose=False):
    ### code from: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/ExoticDijets2012Cutflows#Cleaning_Cuts
    
    if verbose: 
        print "utils:  ChfAndTileHotSpotCleaning"
        print "utils:    - RunNumber: %i, eta: %+.2f, phi: %+.2f, fmax: %.2f, smax: %i"%(RunNumber,eta,phi,fmax,smax)
        print "utils:    - pt: %.2f GeV, chf: %.2f, emf: %.2f"%(pt,chf,emf)
    
    #### Tile Hot spot
    if (RunNumber in [202660,202668,202712,202740,202965,202987,202991,203027]):
        if verbose: print "utils:    - in hot-spot affected period"
        if (eta>-0.2 and eta<-0.1 and phi>2.65 and phi< 2.75 ):
            if verbose: print "utils:    - in hot-spot affected region"
            # pick up the fraction of sampling max and the relevant variables for each jet 
            # note that it doesn't really matter if jet variables are those calibrated or not, as the BCH_CORR_JET does not change the direction of the jet
            if (fmax>0.6 and smax==13):
                if verbose: print "utils:    - hot-spot jet, therefore ugly"
                return 1
    
    #### CHF jets
    if (((emf > 0.9 and chf <0.05) or chf<0.02) and (fabs(eta) < 2.0) and pt>100000):
        if verbose: print "utils:    - bad CHF jet, therefore ugly"
        #assert False
        return 1
    return 0
    
def TileHotSpotCleaning(RunNumber, eta, phi, fmax, smax, verbose=False):
    ### code from: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/ExoticDijets2012Cutflows#Cleaning_Cuts
    
    if verbose: 
        print "utils:  TileHotSpotCleaning"
        print "utils:    - RunNumber: %i, eta: %+.2f, phi: %+.2f, fmax: %.2f, smax: %i"%(RunNumber,eta,phi,fmax,smax)
        
    #### Tile Hot spot
    if (RunNumber in [202660,202668,202712,202740,202965,202987,202991,203027]):
        if verbose: print "utils:    - in hot-spot affected period"
        if (eta>-0.2 and eta<-0.1 and phi>2.65 and phi< 2.75 ):
            if verbose: print "utils:    - in hot-spot affected region"
            # pick up the fraction of sampling max and the relevant variables for each jet 
            # note that it doesn't really matter if jet variables are those calibrated or not, as the BCH_CORR_JET does not change the direction of the jet
            if (fmax>0.6 and smax==13):
                if verbose: print "utils:    - hot-spot jet, therefore ugly"
                return 10
    return 0
    
def ChfCleaning(pt, eta, chf, emf, verbose=False):
    ### code from: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/ExoticDijets2012Cutflows#Cleaning_Cuts
    
    if verbose: 
        print "utils:  ChfCleaning"
        print "utils:    - pt: %.2f GeV, eta: %+.2f, chf: %.2f, emf: %.2f"%(pt/1000.,eta,chf,emf)
    
    #### CHF jets
    if (((emf > 0.9 and chf <0.05) or chf<0.02) and (fabs(eta) < 2.0) and pt>100000):
        if verbose: print "utils:    - bad CHF jet, therefore ugly"
        #assert False
        return 100
    return 0
