#!/usr/bin/env python
import os
import sys
import argparse
import subprocess

# ------ EDIT --------
#ParticleNet_wp = 'medium'
ParticleNet_wp = 'low'
run = 'UL2016APV'
date = '01Feb24_isLeptTrigger_newBoosted_LP'
whichChannels = [True, True, True, False] 
# -------------------------

# settings
ymin_legend = '0.7'
lumi = '19.5'
#regions = ['SR', 'SStight', 'SSrlx', 'OSinviso', 'SSinviso']
regions = ['SR']
do_signal = True   # False means that I want to add the option no-sig through which I disable plotting signal
log = True #

blind = False
if blind:
    blind_range = [0.0,1.0]

parser = argparse.ArgumentParser(description='Command line parser of plotting options')
parser.add_argument('-n', '--dryrun', action='store_true', help='dry run mode')
args = parser.parse_args()


# dictionary selection : [variables]
#resolved_vars = [('DNNoutSM_kl_1', 'DNN_{out}^{SM} k_{#lambda}=1')]
#boosted_vars = resolved_vars
resolved_vars =     [  ("bjet1_pt",  "p_{T}(b_{1}) [GeV]")  , ("bjet2_pt", "p_{T}(b_{2}) [GeV]"), ("bjet1_eta","#eta(b_{1})"), ("bjet2_eta","#eta(b_{2})"), ("bH_mass","m_{bb} [GeV]"), ("bH_pt","p_{T,bb} [GeV]"), ("dau1_pt","p_{T}(lep_{1}) [GeV]"), ("dau2_pt","p_{T}(lep_{2}) [GeV]"), ("dau1_eta","#eta(lep_{1})"), ("dau2_eta","#eta(lep_{2})"), ("tauH_SVFIT_mass","m_{#tau#tau}(SVFit) [GeV]"), ("tauH_SVFIT_pt","p_{T,#tau#tau}(SVFit) [GeV]") ,("tauH_mass","m_{#tau#tau} (vis) [GeV]"), ("tauH_pt","p_{T,#tau#tau} (vis) [GeV]"), ('DNNoutSM_kl_1', 'DNN_{out}^{SM} k_{#lambda}=1'), ('bjet1_CvsL', 'CvsL(b_{1})'),  ('bjet1_CvsB', 'CvsB(b_{1})'), ('bjet1_HHbtag', 'HHbtag(b_{1})'), ('bjet2_CvsL', 'CvsL(b_{2})'),  ('bjet2_CvsB', 'CvsB(b_{2})'), ('bjet2_HHbtag', 'HHbtag(b_{2})')]

boosted_vars =  [('fatjet_softdropMass','m_{bb}^{SD} [GeV]'), ('fatjet_pt','p_{T, bb} [GeV]'), ('fatjet_eta','#eta(bb)'), ('fatjet_phi','#phi(bb)'), ('fatjet_particleNetMDJetTags_score','score_{pnet}(bb)'), ('fatjet_particleNetMDJetTags_mass','m_{bb}^{pnet}'), ('HHbregrsvfit_pt','p_{T,HH} (pnet regression) [GeV]'), ('HHbregrsvfit_eta','#eta_{HH}(pnet regression)'), ('HHbregrsvfit_phi','#phi_{HH}(pnet regression)'), ('HHbregrsvfit_m','m_{HH} (pnet regression) [GeV]'), ('DNNoutSM_kl_1', 'DNN_{out}^{SM} k_{#lambda}=1')]


if 'medium' in ParticleNet_wp:
    dict_sel_var = {
        "s1b1jresolvedMcut"   : resolved_vars,
        "s2b0jresolvedMcut"   : resolved_vars,
        "sboostedLLMcut_semi" : boosted_vars,
        "sboostedM_pnet"      : boosted_vars,
        "baseline"            : resolved_vars,
        "baseline_boosted"    : boosted_vars
    }
    selections = ['baseline', 'baseline_boosted']
    #    selections = ['s1b1jresolvedMcut','s2b0jresolvedMcut','sboostedLLMcut_semi', 'sboostedM_pnet', 'baseline', 'baseline_boosted']

elif 'low' in  ParticleNet_wp:
    dict_sel_var = {
        "s1b1jresolvedMcut"   : resolved_vars,
        "s2b0jresolvedMcut"   : resolved_vars,
        "sboostedLLMcut_semi" : boosted_vars,
        "sboostedL_pnet"      : boosted_vars,
        "baseline"            : resolved_vars,
        "baseline_boosted"    : boosted_vars
    }
    selections = ['baseline', 'baseline_boosted', 's1b1jresolvedMcut','s2b0jresolvedMcut',  'sboostedL_pnet']
    selections = ['s1b1jresolvedMcut','s2b0jresolvedMcut','sboostedLLMcut_semi', 'sboostedL_pnet', 'baseline', 'baseline_boosted']  
else:
    print("ParticleNet working point?")
    sys.exit()



# directories
klubdir = '/gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/'
script = 'scripts/makeFinalPlots_'+run+'.py'
outdir = klubdir+'/plots/'
indir = klubdir

print("Current Directory:   ", os.getcwd())
os.chdir(klubdir)
print 'after ', os.getcwd()

# channel mapping of the considered channels
channelsMap = ['MuTau', 'ETau', 'TauTau', 'MuMu']


# Loop through channels and execute commands
for it,ch in enumerate(channelsMap):
    print("\n CHANNEL ", ch)
    if whichChannels[it]:
        for region in regions:
            print("REGION : ", region)
            for selection,variables in dict_sel_var.items():
                print("SELECTION : ", selection)
                sel = selection

                tag = 'analysis_'+ch+'_'+run+'_'+date
                indir += tag+'/'

                log_option = " --log " if log else ""
                sig_option = ' --no-sig ' if not do_signal else ''
                blind_option = '--blind-range '+str(blind_range[0])+' '+str(blind_range[1]) if blind else ''

                for variab in variables:
                    print("VAR : ", variab)
                    var_name = variab[0]
                    var_label = variab[1]

                    command = 'python '+script+' --indir '+tag+' --outdir '+outdir+' --var '+var_name+' --reg '+region+' --sel '+selection+' --channel '+ch+' --lymin '+ymin_legend+' --lumi '+lumi+log_option+' --ratio --tag '+tag+' --label "'+var_label+'"'+sig_option+' '+blind_option+' --quit'
                    if not args.dryrun:
                        os.system(command)
                    else:
                        print command
