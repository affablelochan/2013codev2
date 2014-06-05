roi_type_dictionary = {
    "NONE":       0x01,  
    "L1SW8x8":    0x02, 
    "L2CONE":     0x03, 
    "A4TT":       0x04,
    "A4TT_JES":   0x05,
    "A4TT_TC":    0x06,
    "A4TT_TC_JES":0x07,
    "A4TT_PU_SUB":0x08,
    "A10TT":      0x09,
    "A4JE":       0x10,
    "A4JE_JES":   0x11,
    "A4JE_TC":    0x12,
    "A4JE_TC_JES":0x13,
    "A4JE_PU_SUB":0x14,
    "A10JE":      0x20,
    "UNCALIBRATED":0x30, 
    "CALIBRATED": 0x31, 
    "UNKNOWN":    0x40,
    "A4CC":       0x15,
    #"NONE":      0x01,
    #"L1SW8x8":   0x02,  
    #"L2CONE":    0x03,  
    #"A4TT":      0x04,
    #"A4TT_JES":  0x05,
    #"A10TT":     0x08,
    #"A4JE":      0x10,
    #"A4JE_JES":  0x11,
    #"A10JE":     0x20,
    #"UNKNOWN":   0x40,
    #"UNCALIBRATED": 0x30, 
    #"CALIBRATED":   0x31, 
    
}

SET_INPUT     = 0x10000
GET_INPUT     = 0x10000*255
SET_OUTPUT    = 0x100
GET_OUTPUT    = 0x100*255
BLANKWORD = 0x70000000

def ParseRoIWord(RoIword,verbose=True):
    if verbose:
        print "rp   : === ParseRoIWord"
        print "rp   :  given RoI word: ",RoIword
        
    input_type   = False
    output_type  = False
    for roi_type in roi_type_dictionary.items():
        #if verbose: print "rp   :  comparing RoI word to ",roi_type
        if ((RoIword&(BLANKWORD+GET_INPUT))==(BLANKWORD+SET_INPUT*roi_type[1])):
            if verbose: print "rp   :  Input type is  ",roi_type[0]
            input_type  = roi_type[0]
        if ((RoIword&(BLANKWORD+GET_OUTPUT))==(BLANKWORD+SET_OUTPUT*roi_type[1])):
            if verbose: print "rp   :  Output type is ",roi_type[0]
            output_type  = roi_type[0]
    
    if not input_type:
        if verbose: print "rp   :  No input type found from RoIword %i,  setting to NON_L15"%RoIword
        input_type = "NON_L15"
    if not output_type:
        if verbose: print "rp   :  No output type found from RoIword %i, setting to NON_L15"%RoIword
        output_type = "NON_L15"
    
    counter = ExtractCounter(RoIword,verbose=verbose)
    
    return input_type,output_type,counter
    

def ExtractCounter(RoIword,verbose=False):
    if verbose:
        print "rp   : === ExtractCounter"
        print "rp   :  given RoI word: ",RoIword
        
    counter = RoIword & 255
    if verbose: print "rp   :  counter is ",counter
        
    return counter
