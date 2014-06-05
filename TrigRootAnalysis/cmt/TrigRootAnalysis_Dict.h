/********************************************************************
* TrigRootAnalysis_Dict.h
* CAUTION: DON'T CHANGE THIS FILE. THIS FILE IS AUTOMATICALLY GENERATED
*          FROM HEADER FILES LISTED IN G__setup_cpp_environmentXXX().
*          CHANGE THOSE HEADER FILES AND REGENERATE THIS FILE.
********************************************************************/
#ifdef __CINT__
#error TrigRootAnalysis_Dict.h/C is only for compilation. Abort cint.
#endif
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#define G__ANSIHEADER
#define G__DICTIONARY
#define G__PRIVATE_GVALUE
#include "G__ci.h"
#include "FastAllocString.h"
extern "C" {
extern void G__cpp_setup_tagtableTrigRootAnalysis_Dict();
extern void G__cpp_setup_inheritanceTrigRootAnalysis_Dict();
extern void G__cpp_setup_typetableTrigRootAnalysis_Dict();
extern void G__cpp_setup_memvarTrigRootAnalysis_Dict();
extern void G__cpp_setup_globalTrigRootAnalysis_Dict();
extern void G__cpp_setup_memfuncTrigRootAnalysis_Dict();
extern void G__cpp_setup_funcTrigRootAnalysis_Dict();
extern void G__set_cpp_environmentTrigRootAnalysis_Dict();
}


#include "TObject.h"
#include "TMemberInspector.h"
#include "../TrigRootAnalysis/ChainGroup.h"
#include "../TrigRootAnalysis/ChainGroupHandling.h"
#include "../TrigRootAnalysis/Conditions.h"
#include "../TrigRootAnalysis/ConfigAccess.h"
#include "../TrigRootAnalysis/DataAccess.h"
#include "../TrigRootAnalysis/IConfigAccess.h"
#include "../TrigRootAnalysis/IDataAccess.h"
#include "../TrigRootAnalysis/IITrigConfigSvcD3PD.h"
#include "../TrigRootAnalysis/TrigDecisionFunctions.h"
#include "../TrigRootAnalysis/PyTrigDecisionToolD3PD.h"
#include "../TrigRootAnalysis/TrigConfigSvcD3PD.h"
#include "../TrigRootAnalysis/TrigDecisionToolD3PD.h"
#include "../TrigRootAnalysis/VarHandle.h"
#include <algorithm>
namespace std { }
using namespace std;

#ifndef G__MEMFUNCBODY
#endif

extern G__linked_taginfo G__TrigRootAnalysis_DictLN_TClass;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_TBuffer;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_TMemberInspector;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_TObject;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_TNamed;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_TString;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_vectorlEshortcOallocatorlEshortgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_vectorlEshortcOallocatorlEshortgRsPgRcLcLiterator;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_reverse_iteratorlEvectorlEshortcOallocatorlEshortgRsPgRcLcLiteratorgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_vectorlElongsPlongcOallocatorlElongsPlonggRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_vectorlEunsignedsPcharcOallocatorlEunsignedsPchargRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_vectorlEunsignedsPshortcOallocatorlEunsignedsPshortgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_vectorlEunsignedsPintcOallocatorlEunsignedsPintgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_vectorlEfloatcOallocatorlEfloatgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_string;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_vectorlEROOTcLcLTSchemaHelpercOallocatorlEROOTcLcLTSchemaHelpergRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_reverse_iteratorlEvectorlEROOTcLcLTSchemaHelpercOallocatorlEROOTcLcLTSchemaHelpergRsPgRcLcLiteratorgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_vectorlETVirtualArraymUcOallocatorlETVirtualArraymUgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_reverse_iteratorlEvectorlETVirtualArraymUcOallocatorlETVirtualArraymUgRsPgRcLcLiteratorgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_D3PD;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_D3PDcLcLTrigDefs;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_D3PDcLcLTrigDefscLcLDecisionTypes;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_D3PDcLcLTrig;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_D3PDcLcLTrigcLcLIDataAccess;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_D3PDcLcLTrigcLcLIConfigAccess;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_D3PDcLcLTrigcLcLChainGroupHandling;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_D3PDcLcLChainGroup;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_vectorlEstringcOallocatorlEstringgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_reverse_iteratorlEvectorlEstringcOallocatorlEstringgRsPgRcLcLiteratorgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_vectorlEintcOallocatorlEintgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_reverse_iteratorlEvectorlEintcOallocatorlEintgRsPgRcLcLiteratorgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_D3PDcLcLTrigcLcLIDataAccesscLcLL1ResultType;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_D3PDcLcLTrigcLcLIDataAccesscLcLHLTResultType;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_D3PDcLcLIITrigConfigSvcD3PD;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_D3PDcLcLIITrigDecisionToolD3PD;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_lesslEstringgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_allocatorlEpairlEconstsPstringcOintgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEstringcOintcOlesslEstringgRcOallocatorlEpairlEconstsPstringcOintgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_pairlEstringcOintgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEstringcOintcOlesslEstringgRcOallocatorlEpairlEconstsPstringcOintgRsPgRsPgRcLcLiterator;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEstringcOintcOlesslEstringgRcOallocatorlEpairlEconstsPstringcOintgRsPgRsPgRcLcLreverse_iterator;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_allocatorlEpairlEconstsPstringcOfloatgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEstringcOfloatcOlesslEstringgRcOallocatorlEpairlEconstsPstringcOfloatgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_pairlEstringcOfloatgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEstringcOfloatcOlesslEstringgRcOallocatorlEpairlEconstsPstringcOfloatgRsPgRsPgRcLcLiterator;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEstringcOfloatcOlesslEstringgRcOallocatorlEpairlEconstsPstringcOfloatgRsPgRsPgRcLcLreverse_iterator;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_pairlEintcOintgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_TTree;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_D3PDcLcLTrigConfigSvcD3PD;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_pairlEintcOpairlEintcOintgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOpairlEintcOintgRsPgRcOmaplEstringcOintcOlesslEstringgRcOallocatorlEpairlEconstsPstringcOintgRsPgRsPgRcOlesslEpairlEintcOpairlEintcOintgRsPgRsPgRcOallocatorlEpairlEconstsPpairlEintcOpairlEintcOintgRsPgRcOmaplEstringcOintcOlesslEstringgRcOallocatorlEpairlEconstsPstringcOintgRsPgRsPgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOpairlEintcOintgRsPgRcOmaplEstringcOfloatcOlesslEstringgRcOallocatorlEpairlEconstsPstringcOfloatgRsPgRsPgRcOlesslEpairlEintcOpairlEintcOintgRsPgRsPgRcOallocatorlEpairlEconstsPpairlEintcOpairlEintcOintgRsPgRcOmaplEstringcOfloatcOlesslEstringgRcOallocatorlEpairlEconstsPstringcOfloatgRsPgRsPgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_allocatorlEpairlEconstsPstringcOstringgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEstringcOstringcOlesslEstringgRcOallocatorlEpairlEconstsPstringcOstringgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_pairlEstringcOstringgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEstringcOstringcOlesslEstringgRcOallocatorlEpairlEconstsPstringcOstringgRsPgRsPgRcLcLiterator;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEstringcOstringcOlesslEstringgRcOallocatorlEpairlEconstsPstringcOstringgRsPgRsPgRcLcLreverse_iterator;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_pairlEmaplEstringcOstringcOlesslEstringgRcOallocatorlEpairlEconstsPstringcOstringgRsPgRsPgRcLcLiteratorcOboolgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOpairlEintcOintgRsPgRcOmaplEstringcOstringcOlesslEstringgRcOallocatorlEpairlEconstsPstringcOstringgRsPgRsPgRcOlesslEpairlEintcOpairlEintcOintgRsPgRsPgRcOallocatorlEpairlEconstsPpairlEintcOpairlEintcOintgRsPgRcOmaplEstringcOstringcOlesslEstringgRcOallocatorlEpairlEconstsPstringcOstringgRsPgRsPgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEunsignedsPintcOunsignedsPintcOlesslEunsignedsPintgRcOallocatorlEpairlEconstsPunsignedsPintcOunsignedsPintgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOpairlEintcOintgRsPgRcOmaplEunsignedsPintcOunsignedsPintcOlesslEunsignedsPintgRcOallocatorlEpairlEconstsPunsignedsPintcOunsignedsPintgRsPgRsPgRcOlesslEpairlEintcOpairlEintcOintgRsPgRsPgRcOallocatorlEpairlEconstsPpairlEintcOpairlEintcOintgRsPgRcOmaplEunsignedsPintcOunsignedsPintcOlesslEunsignedsPintgRcOallocatorlEpairlEconstsPunsignedsPintcOunsignedsPintgRsPgRsPgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEunsignedsPintcOstringcOlesslEunsignedsPintgRcOallocatorlEpairlEconstsPunsignedsPintcOstringgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOpairlEintcOintgRsPgRcOmaplEunsignedsPintcOstringcOlesslEunsignedsPintgRcOallocatorlEpairlEconstsPunsignedsPintcOstringgRsPgRsPgRcOlesslEpairlEintcOpairlEintcOintgRsPgRsPgRcOallocatorlEpairlEconstsPpairlEintcOpairlEintcOintgRsPgRcOmaplEunsignedsPintcOstringcOlesslEunsignedsPintgRcOallocatorlEpairlEconstsPunsignedsPintcOstringgRsPgRsPgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOintgRcOstringcOlesslEpairlEintcOintgRsPgRcOallocatorlEpairlEconstsPpairlEintcOintgRcOstringgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOpairlEintcOintgRsPgRcOmaplEpairlEintcOintgRcOstringcOlesslEpairlEintcOintgRsPgRcOallocatorlEpairlEconstsPpairlEintcOintgRcOstringgRsPgRsPgRcOlesslEpairlEintcOpairlEintcOintgRsPgRsPgRcOallocatorlEpairlEconstsPpairlEintcOpairlEintcOintgRsPgRcOmaplEpairlEintcOintgRcOstringcOlesslEpairlEintcOintgRsPgRcOallocatorlEpairlEconstsPpairlEintcOintgRcOstringgRsPgRsPgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOintgRcOunsignedsPintcOlesslEpairlEintcOintgRsPgRcOallocatorlEpairlEconstsPpairlEintcOintgRcOunsignedsPintgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOpairlEintcOintgRsPgRcOmaplEpairlEintcOintgRcOunsignedsPintcOlesslEpairlEintcOintgRsPgRcOallocatorlEpairlEconstsPpairlEintcOintgRcOunsignedsPintgRsPgRsPgRcOlesslEpairlEintcOpairlEintcOintgRsPgRsPgRcOallocatorlEpairlEconstsPpairlEintcOpairlEintcOintgRsPgRcOmaplEpairlEintcOintgRcOunsignedsPintcOlesslEpairlEintcOintgRsPgRcOallocatorlEpairlEconstsPpairlEintcOintgRcOunsignedsPintgRsPgRsPgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEintcOstringcOlesslEintgRcOallocatorlEpairlEconstsPintcOstringgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOpairlEintcOintgRsPgRcOmaplEintcOstringcOlesslEintgRcOallocatorlEpairlEconstsPintcOstringgRsPgRsPgRcOlesslEpairlEintcOpairlEintcOintgRsPgRsPgRcOallocatorlEpairlEconstsPpairlEintcOpairlEintcOintgRsPgRcOmaplEintcOstringcOlesslEintgRcOallocatorlEpairlEconstsPintcOstringgRsPgRsPgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOpairlEintcOintgRsPgRcOvectorlEstringcOallocatorlEstringgRsPgRcOlesslEpairlEintcOpairlEintcOintgRsPgRsPgRcOallocatorlEpairlEconstsPpairlEintcOpairlEintcOintgRsPgRcOvectorlEstringcOallocatorlEstringgRsPgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOpairlEintcOintgRsPgRcOunsignedsPshortcOlesslEpairlEintcOpairlEintcOintgRsPgRsPgRcOallocatorlEpairlEconstsPpairlEintcOpairlEintcOintgRsPgRcOunsignedsPshortgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOpairlEintcOintgRsPgRcOvectorlEunsignedsPintcOallocatorlEunsignedsPintgRsPgRcOlesslEpairlEintcOpairlEintcOintgRsPgRsPgRcOallocatorlEpairlEconstsPpairlEintcOpairlEintcOintgRsPgRcOvectorlEunsignedsPintcOallocatorlEunsignedsPintgRsPgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOpairlEintcOintgRsPgRcOvectorlEunsignedsPshortcOallocatorlEunsignedsPshortgRsPgRcOlesslEpairlEintcOpairlEintcOintgRsPgRsPgRcOallocatorlEpairlEconstsPpairlEintcOpairlEintcOintgRsPgRcOvectorlEunsignedsPshortcOallocatorlEunsignedsPshortgRsPgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_vectorlEvectorlEunsignedsPintcOallocatorlEunsignedsPintgRsPgRcOallocatorlEvectorlEunsignedsPintcOallocatorlEunsignedsPintgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_reverse_iteratorlEvectorlEvectorlEunsignedsPintcOallocatorlEunsignedsPintgRsPgRcOallocatorlEvectorlEunsignedsPintcOallocatorlEunsignedsPintgRsPgRsPgRsPgRcLcLiteratorgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOpairlEintcOintgRsPgRcOvectorlEvectorlEunsignedsPintcOallocatorlEunsignedsPintgRsPgRcOallocatorlEvectorlEunsignedsPintcOallocatorlEunsignedsPintgRsPgRsPgRsPgRcOlesslEpairlEintcOpairlEintcOintgRsPgRsPgRcOallocatorlEpairlEconstsPpairlEintcOpairlEintcOintgRsPgRcOvectorlEvectorlEunsignedsPintcOallocatorlEunsignedsPintgRsPgRcOallocatorlEvectorlEunsignedsPintcOallocatorlEunsignedsPintgRsPgRsPgRsPgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOpairlEintcOintgRsPgRcOvectorlEunsignedsPcharcOallocatorlEunsignedsPchargRsPgRcOlesslEpairlEintcOpairlEintcOintgRsPgRsPgRcOallocatorlEpairlEconstsPpairlEintcOpairlEintcOintgRsPgRcOvectorlEunsignedsPcharcOallocatorlEunsignedsPchargRsPgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOpairlEintcOintgRsPgRcOvectorlEfloatcOallocatorlEfloatgRsPgRcOlesslEpairlEintcOpairlEintcOintgRsPgRsPgRcOallocatorlEpairlEconstsPpairlEintcOpairlEintcOintgRsPgRcOvectorlEfloatcOallocatorlEfloatgRsPgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_vectorlEvectorlEstringcOallocatorlEstringgRsPgRcOallocatorlEvectorlEstringcOallocatorlEstringgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_vectorlEvectorlEstringcOallocatorlEstringgRsPgRcOallocatorlEvectorlEstringcOallocatorlEstringgRsPgRsPgRsPgRcLcLiterator;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_reverse_iteratorlEvectorlEvectorlEstringcOallocatorlEstringgRsPgRcOallocatorlEvectorlEstringcOallocatorlEstringgRsPgRsPgRsPgRcLcLiteratorgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOpairlEintcOintgRsPgRcOvectorlEvectorlEstringcOallocatorlEstringgRsPgRcOallocatorlEvectorlEstringcOallocatorlEstringgRsPgRsPgRsPgRcOlesslEpairlEintcOpairlEintcOintgRsPgRsPgRcOallocatorlEpairlEconstsPpairlEintcOpairlEintcOintgRsPgRcOvectorlEvectorlEstringcOallocatorlEstringgRsPgRcOallocatorlEvectorlEstringcOallocatorlEstringgRsPgRsPgRsPgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_vectorlEvectorlEfloatcOallocatorlEfloatgRsPgRcOallocatorlEvectorlEfloatcOallocatorlEfloatgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_vectorlEvectorlEfloatcOallocatorlEfloatgRsPgRcOallocatorlEvectorlEfloatcOallocatorlEfloatgRsPgRsPgRsPgRcLcLiterator;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_reverse_iteratorlEvectorlEvectorlEfloatcOallocatorlEfloatgRsPgRcOallocatorlEvectorlEfloatcOallocatorlEfloatgRsPgRsPgRsPgRcLcLiteratorgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOpairlEintcOintgRsPgRcOvectorlEvectorlEfloatcOallocatorlEfloatgRsPgRcOallocatorlEvectorlEfloatcOallocatorlEfloatgRsPgRsPgRsPgRcOlesslEpairlEintcOpairlEintcOintgRsPgRsPgRcOallocatorlEpairlEconstsPpairlEintcOpairlEintcOintgRsPgRcOvectorlEvectorlEfloatcOallocatorlEfloatgRsPgRcOallocatorlEvectorlEfloatcOallocatorlEfloatgRsPgRsPgRsPgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_vectorlEvectorlEunsignedsPshortcOallocatorlEunsignedsPshortgRsPgRcOallocatorlEvectorlEunsignedsPshortcOallocatorlEunsignedsPshortgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_reverse_iteratorlEvectorlEvectorlEunsignedsPshortcOallocatorlEunsignedsPshortgRsPgRcOallocatorlEvectorlEunsignedsPshortcOallocatorlEunsignedsPshortgRsPgRsPgRsPgRcLcLiteratorgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOpairlEintcOintgRsPgRcOvectorlEvectorlEunsignedsPshortcOallocatorlEunsignedsPshortgRsPgRcOallocatorlEvectorlEunsignedsPshortcOallocatorlEunsignedsPshortgRsPgRsPgRsPgRcOlesslEpairlEintcOpairlEintcOintgRsPgRsPgRcOallocatorlEpairlEconstsPpairlEintcOpairlEintcOintgRsPgRcOvectorlEvectorlEunsignedsPshortcOallocatorlEunsignedsPshortgRsPgRcOallocatorlEvectorlEunsignedsPshortcOallocatorlEunsignedsPshortgRsPgRsPgRsPgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_vectorlEvectorlEunsignedsPcharcOallocatorlEunsignedsPchargRsPgRcOallocatorlEvectorlEunsignedsPcharcOallocatorlEunsignedsPchargRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_reverse_iteratorlEvectorlEvectorlEunsignedsPcharcOallocatorlEunsignedsPchargRsPgRcOallocatorlEvectorlEunsignedsPcharcOallocatorlEunsignedsPchargRsPgRsPgRsPgRcLcLiteratorgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_maplEpairlEintcOpairlEintcOintgRsPgRcOvectorlEvectorlEunsignedsPcharcOallocatorlEunsignedsPchargRsPgRcOallocatorlEvectorlEunsignedsPcharcOallocatorlEunsignedsPchargRsPgRsPgRsPgRcOlesslEpairlEintcOpairlEintcOintgRsPgRsPgRcOallocatorlEpairlEconstsPpairlEintcOpairlEintcOintgRsPgRcOvectorlEvectorlEunsignedsPcharcOallocatorlEunsignedsPchargRsPgRcOallocatorlEvectorlEunsignedsPcharcOallocatorlEunsignedsPchargRsPgRsPgRsPgRsPgRsPgRsPgR;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_D3PDcLcLTrigcLcLConfigAccess;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_D3PDcLcLTrigcLcLDataAccess;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_D3PDcLcLTrigcLcLTrigDecisionFunctions;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_D3PDcLcLTrigDecisionToolD3PD;
extern G__linked_taginfo G__TrigRootAnalysis_DictLN_D3PDcLcLPyTrigDecisionToolD3PD;

/* STUB derived class for protected member access */
typedef vector<short,allocator<short> > G__vectorlEshortcOallocatorlEshortgRsPgR;
typedef map<string,int,less<string>,allocator<pair<const string,int> > > G__maplEstringcOintcOlesslEstringgRcOallocatorlEpairlEconstsPstringcOintgRsPgRsPgR;
typedef map<string,float,less<string>,allocator<pair<const string,float> > > G__maplEstringcOfloatcOlesslEstringgRcOallocatorlEpairlEconstsPstringcOfloatgRsPgRsPgR;
typedef map<string,string,less<string>,allocator<pair<const string,string> > > G__maplEstringcOstringcOlesslEstringgRcOallocatorlEpairlEconstsPstringcOstringgRsPgRsPgR;
typedef pair<string,string> G__pairlEstringcOstringgR;
typedef vector<vector<string,allocator<string> >,allocator<vector<string,allocator<string> > > > G__vectorlEvectorlEstringcOallocatorlEstringgRsPgRcOallocatorlEvectorlEstringcOallocatorlEstringgRsPgRsPgRsPgR;
typedef vector<vector<float,allocator<float> >,allocator<vector<float,allocator<float> > > > G__vectorlEvectorlEfloatcOallocatorlEfloatgRsPgRcOallocatorlEvectorlEfloatcOallocatorlEfloatgRsPgRsPgRsPgR;
