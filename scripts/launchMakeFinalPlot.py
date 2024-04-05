#!/usr/bin/env python
import os
import sys
import argparse
import subprocess

# ------ EDIT --------
#ParticleNet_wp = 'medium'
ParticleNet_wp = 'low'
run = 'UL16APV'
date = '17Mar2024_categories'

out_tag = '_noScaleBinWidth'
whichChannels = [False, False, True, True] 

selections = ['res1b','res2b','boosted_semi', 'boostedL_pnet', 'baseline', 'baseline_boosted']
# -------------------------

# settings
ymin_legend = '0.7'
lumi = '19.5'
#regions = ['SR', 'SStight', 'SSrlx', 'OSinviso', 'SSinviso']
regions = ['SR']
do_signal = True   # False means that I want to add the option no-sig through which I disable plotting signal
log = True #

no_bin_width = True # True Means that I do not want to scale graphs by the bin width
blind = False
if blind:
    blind_range = [0.0,1.0]

parser = argparse.ArgumentParser(description='Command line parser of plotting options')
parser.add_argument('-n', '--dryrun', action='store_true', help='dry run mode')
args = parser.parse_args()


# dictionary selection : [variables]
resolved_vars =     [  ("bjet1_pt",  "p_{T}(b_{1}) [GeV]")  , ("bjet2_pt", "p_{T}(b_{2}) [GeV]"), ("bjet1_eta","#eta(b_{1})"), ("bjet2_eta","#eta(b_{2})"), ("bH_mass","m_{bb} [GeV]"), ("bH_pt","p_{T,bb} [GeV]"), ("dau1_pt","p_{T}(lep_{1}) [GeV]"), ("dau2_pt","p_{T}(lep_{2}) [GeV]"), ("dau1_eta","#eta(lep_{1})"), ("dau2_eta","#eta(lep_{2})"), ("tauH_SVFIT_mass","m_{#tau#tau}(SVFit) [GeV]"), ("tauH_SVFIT_pt","p_{T,#tau#tau}(SVFit) [GeV]") ,("tauH_mass","m_{#tau#tau} (vis) [GeV]"), ("tauH_pt","p_{T,#tau#tau} (vis) [GeV]"), ('DNNoutSM_kl_1', 'DNN_{out}^{SM} k_{#lambda}=1')]

boosted_vars =  [('fatjet_softdropMass','m_{bb}^{SD} [GeV]'), ('fatjet_pt','p_{T, bb} [GeV]'), ('fatjet_eta','#eta(bb)'), ('fatjet_phi','#phi(bb)'), ('fatjet_particleNetMDJetTags_score','score_{pnet}(bb)'), ('fatjet_particleNetMDJetTags_mass','m_{bb}^{pnet}'), ('HHbregrsvfit_pt','p_{T,HH} (pnet regression) [GeV]'), ('HHbregrsvfit_eta','#eta_{HH}(pnet regression)'), ('HHbregrsvfit_phi','#phi_{HH}(pnet regression)'), ('HHbregrsvfit_m','m_{HH} (pnet regression) [GeV]'), ('DNNoutSM_kl_1', 'DNN_{out}^{SM} k_{#lambda}=1')]


if 'medium' in ParticleNet_wp:
    dict_sel_var = {
        "res1b"   : resolved_vars,
        "res2b"   : resolved_vars,
        "boosted_semi" : boosted_vars,
        "boostedM_pnet"      : boosted_vars,
        "baseline"            : resolved_vars,
        "baseline_boosted"    : boosted_vars
    }
elif 'low' in  ParticleNet_wp:
    dict_sel_var = {
        "res1b"   : resolved_vars,
        "res2b"   : resolved_vars,
        "boosted_semi" : boosted_vars,
        "boostedL_pnet"      : boosted_vars,
        "baseline"            : resolved_vars,
        "baseline_boosted"    : boosted_vars
    }
else:
    print("ParticleNet working point?")
    sys.exit()



# directories
klubdir = '/gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/'
if 'UL16APV' in run:
    script = 'scripts/makeFinalPlots_UL2016APV.py'
else:
    print("RUN ?")
    sys.exit(0)
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
                if selection not in selections:
                    continue
                print("SELECTION : ", selection)
                sel = selection

                tag = 'analysis_'+ch+'_'+run+'_'+date
                indir += tag+'/'

                log_option = " --log " if log else ""
                sig_option = ' --no-sig ' if not do_signal else ''
                blind_option = '--blind-range '+str(blind_range[0])+' '+str(blind_range[1]) if blind else ''
                binwidth_option = '--no-binwidth' if no_bin_width else ''
                for variab in variables:
                    print("VAR : ", variab)
                    var_name = variab[0]
                    var_label = variab[1]
                    outTag = tag + out_tag

                    command = 'python '+script+' --indir '+tag+' --outdir '+outdir+' --var '+var_name+' --reg '+region+' --sel '+selection+' --channel '+ch+' --lymin '+ymin_legend+' --lumi '+lumi+log_option+' --ratio --tag '+outTag+' --label "'+var_label+'"'+sig_option+' '+blind_option+' '+binwidth_option+' --quit'
                    if not args.dryrun:
                        os.system(command)
                    else:
                        print command
