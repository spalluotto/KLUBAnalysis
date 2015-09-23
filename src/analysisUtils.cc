#include "analysisUtils.h"

using namespace std ;


vector<pair <TString, TCut> >
addSelection (vector<pair <TString, TCut> > m_cuts, string cut, string tag)
{
  vector<pair <TString, TCut> > output = m_cuts ;
  for (unsigned int i = 0 ; i < output.size () ; ++i)
    {
      output.at (i).first = TString (tag.c_str ()) + output.at (i).first ;
      output.at (i).second = output.at (i).second && TCut (cut.c_str ()) ;
    }
  return output ;
}


// --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---


std::pair<int, int> leptonsType (int pairType)
{
  if (pairType == 0) return pair<int,int> (0, 2) ;
  if (pairType == 1) return pair<int,int> (1, 2) ;
  if (pairType == 2) return pair<int,int> (2, 2) ;
  if (pairType == 3) return pair<int,int> (0, 0) ;
  if (pairType == 4) return pair<int,int> (1, 1) ;
  if (pairType == 5) return pair<int,int> (1, 0) ; // FIXME are they ordered per flavour?
  if (pairType == 6) return pair<int,int> (1, 1) ;
  if (pairType == 7) return pair<int,int> (0, 0) ;
  return pair<int,int> (-1, -1) ;
}


// --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---


bool isIsolated (int leptonType, float threshold, float isoDeposits, float pT)
{
  if (leptonType == 0 || leptonType == 1) return (isoDeposits/pT < threshold) ;
  if (leptonType == 2) return (isoDeposits < threshold) ;
  return false ;
}


// --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---


void
addHistos (vector<sample> & samples, 
           HistoManager * manager,
           vector<string> & variablesList,
           vector<pair <TString, TCut> > & selections,
           bool isSignal,
           bool isData)
{
  TString histoName ;
  int histoType = 0 ;
  if (isSignal) histoType = 1 ;
  if (isData) histoType = 2 ;

  // loop on sim samples
  for (unsigned int j = 0 ; j < samples.size () ; ++j)
    {
      for (unsigned int k = 0 ; k < selections.size () ; ++k)
        {
          for (unsigned int i = 0 ; i < variablesList.size () ; ++i)
            {
              histoName.Form ("%s_%s_%s",
                              variablesList.at (i).c_str (),
                              samples.at (j).sampleName.Data (),
                              selections.at (k).first.Data ()
                              ) ;
              // remove not alphanumeric symbols from the var name
              string varID = variablesList.at (i) ;
              varID.erase (std::remove_if (varID.begin (), varID.end (), isNOTalnum ()), varID.end ()) ;
              // get histo nbins and range
              vector <float> limits = 
                gConfigParser->readFloatListOption (TString ("histos::") 
                    + varID.c_str ()) ;
              manager->AddNewHisto (histoName.Data (),histoName.Data (),
                  int (limits.at (0)), limits.at (1), limits.at (2),
                  gConfigParser->readIntOption (TString ("colors::") 
                      + samples.at (j).sampleName.Data ()), 
                  histoType,
                  variablesList.at (i).c_str (), "events"
                ) ;
            }  
        }
    } // loop on sim samples

  return ;
}


// --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---


counters
fillHistos (vector<sample> & samples, 
            plotContainer & plots,
            vector<string> & variablesList,
            vector<pair <TString, TCut> > & selections,
            float lumi,
            const vector<float> & scale,
            bool isData,
            bool isSignal)
{
  TString histoName ;

  // for efficiency evaluation
  counters localCounter ;

  //Loop on the samples
  for (unsigned int iSample = 0 ; iSample < samples.size () ; ++iSample)
    {
      double eff = samples.at (iSample).eff ;
      localCounter.initEfficiencies.push_back (eff) ;

      localCounter.counters.push_back (vector<float> (selections.size () + 1, 0.)) ;
      
      TTree *tree = samples.at (iSample).sampleTree ;
      TTreeFormula * TTF[selections.size ()] ;
      for (unsigned int isel = 0 ; isel < selections.size () ; ++isel)
        {
          TString fname ; fname.Form ("ttf%d",isel) ;
          TTF[isel] = new TTreeFormula (fname.Data (), selections.at (isel).second, tree) ;
        }
  
      float weight ;
      tree->SetBranchAddress ("MC_weight", &weight) ;
      // signal scaling
      float scaling = 1. / samples.at (iSample).eff_den ;
      if (scale.size () > 0) scaling *= scale.at (iSample) ;

      cout << "Opening sample: "
           << samples.at (iSample).sampleName
           << "\t with initial weighted events\t" << samples.at (iSample).eff_den
           << endl ;

      vector<float> address (variablesList.size (), 0.) ;
      int tempnjets;
      int indexNjets = -1;

      for (unsigned int iv = 0 ; iv < variablesList.size () ; ++iv)
      {
      	if(variablesList.at(iv)=="njets")
        {
      	  tree->SetBranchAddress (variablesList.at (iv).c_str (), &tempnjets) ;
      	  indexNjets=iv;
      	}
        else tree->SetBranchAddress (variablesList.at (iv).c_str (), &(address.at (iv))) ;
      }

      for (int iEvent = 0 ; iEvent < tree->GetEntries () ; ++iEvent)
        {
          tree->GetEntry (iEvent) ;

          if (isData) localCounter.counters.at (iSample).at (0) += 1. ;
          else        localCounter.counters.at (iSample).at (0) 
                          += weight * lumi * scaling ;
          for (unsigned int isel = 0 ; isel < selections.size () ; ++isel)
            {
              if (! TTF[isel]->EvalInstance ()) continue ;

              if (isData) localCounter.counters.at (iSample).at (isel+1) += 1. ;
              else        localCounter.counters.at (iSample).at (isel+1) 
                              += weight * lumi * scaling ;

              for (unsigned int iv = 0 ; iv < variablesList.size () ; ++iv)
                {
                  TH1F * histo = 
                  plots.getHisto (variablesList.at (iv),
                      selections.at (isel).first.Data (),
                      samples.at (iSample).sampleName.Data ()
                    ) ;
                  
                  if (isData) 
		              {
                      if(iv!=indexNjets)histo->Fill (address[iv]) ;
		                  else histo->Fill (tempnjets) ;
                  }
                  else        
                  {
                      if(iv!=indexNjets)histo->Fill (address[iv], weight * lumi * scaling) ;
		                  else histo->Fill (tempnjets, weight * lumi * scaling) ;
                  }
                } //loop on variables
            } //loop on selections
        } //loop on tree entries

      for (unsigned int isel = 0 ; isel < selections.size () ; ++isel) delete TTF[isel] ;
    } // Loop on the MC samples

  return localCounter ;
}


// --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---


vector<THStack *> 
stackHistos (vector<sample> & samples, HistoManager * manager, 
             vector<string> & variablesList,
             vector<pair <TString, TCut> > & selections,
             const string & tag)
{
  int nVars = variablesList.size () ;
  int nSel = selections.size () ;
  TString outputName, histoName ;
  
  vector <THStack *> hstack (nVars*nSel) ; //one stack for variable

  for (int isel = 0 ; isel < nSel ; ++isel)
    {
      for (int iv = 0 ; iv < nVars ; ++iv)
        {
          // filling stacks for background
          outputName.Form ("stack_%s_%s_%s",
            tag.c_str (),
            variablesList.at (iv).c_str (), selections.at (isel).first.Data ()) ;
          hstack.at (iv+nVars*isel) = new THStack (outputName.Data (), outputName.Data ()) ;
          for (unsigned int i = 0 ; i < samples.size () ; ++i)
            {
              histoName.Form ("%s_%s_%s",
                  variablesList.at (iv).c_str (),
                  samples.at (i).sampleName.Data (),
                  selections.at (isel).first.Data ()
                ) ;
              addOverAndUnderFlow (manager->GetHisto (histoName.Data ())) ;
              hstack.at (iv+nVars*isel)->Add (manager->GetHisto (histoName.Data ())) ;
            } 
        }
    }
  return hstack ;
}

