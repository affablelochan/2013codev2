// Dear emacs, this is -*- c++ -*-
// $Id: LinkDef.h 581262 2014-02-03 17:23:31Z tamartin $
#ifndef TRIGROOTANALYSIS_LINKDEF_H
#define TRIGROOTANALYSIS_LINKDEF_H

// Local include(s):
#include "../TrigRootAnalysis/IDataAccess.h"
#include "../TrigRootAnalysis/IConfigAccess.h"
#include "../TrigRootAnalysis/IITrigConfigSvcD3PD.h"
#include "../TrigRootAnalysis/IITrigDecisionToolD3PD.h"
#include "../TrigRootAnalysis/TrigConfigSvcD3PD.h"
#include "../TrigRootAnalysis/DataAccess.h"
#include "../TrigRootAnalysis/ConfigAccess.h"
#include "../TrigRootAnalysis/ChainGroupHandling.h"
#include "../TrigRootAnalysis/TrigDecisionFunctions.h"
#include "../TrigRootAnalysis/TrigDecisionToolD3PD.h"
#include "../TrigRootAnalysis/PyTrigDecisionToolD3PD.h"
#include "../TrigRootAnalysis/ChainGroup.h"

#ifdef __CINT__

#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;

#pragma link C++ nestedclass;

// Dictionaries for the interface classes:
#pragma link C++ class D3PD::IITrigConfigSvcD3PD+;
#pragma link C++ class D3PD::IITrigDecisionToolD3PD+;
#pragma link C++ class D3PD::Trig::IDataAccess+;
#pragma link C++ class D3PD::Trig::IConfigAccess+;

// Dictionaries for the classes implemented in this library:
#pragma link C++ class D3PD::TrigConfigSvcD3PD+;
#pragma link C++ class D3PD::Trig::DataAccess+;
#pragma link C++ class D3PD::Trig::ConfigAccess+;
#pragma link C++ class D3PD::Trig::ChainGroupHandling+;
#pragma link C++ class D3PD::Trig::TrigDecisionFunctions+;
#pragma link C++ class D3PD::TrigDecisionToolD3PD+;
#pragma link C++ class D3PD::PyTrigDecisionToolD3PD+;
#pragma link C++ class D3PD::ChainGroup+;

// Other constructs:
#pragma link C++ enum D3PD::TrigDefs::DecisionTypes+;

// Additional dictionaries for reading the D3PDs. ROOT says that it doesn't
// need some of these, but I beg to differ. I've seen some weird crashes without
// these in some test jobs...
#pragma link C++ class map<string,string>+;
#pragma link C++ class pair<string,string>+;
#pragma link C++ class map<string,int>+;
#pragma link C++ class map<string,float>+;
#pragma link C++ class vector<short>+;
// [TrigMonConfig] addind some more dictionaries for additional structures used saving the full trig conf.
// Will not run without these.
#pragma link C++ class vector<vector<float> >+;
#pragma link C++ class vector<vector<string> >+;

#endif // __CINT__
#endif // TRIGROOTANALYSIS_LINKDEF_H
