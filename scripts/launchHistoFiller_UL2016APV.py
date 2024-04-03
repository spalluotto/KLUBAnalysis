#!/usr/bin/env python
import os
import sys
import argparse


# ----- EDIT HERE ----
skim_name = 'SKIMS_UL2016APV_14Feb2024'   # --- this only serves for checking bad files, but samples should be put in the sampleCfg
run = 'UL16APV'
date = '17Mar2024_categories'
whichChannels = [True, True, True, True]   # you may want to run one or more channels
nJobs = '250'

checkGoodFiles = False
# --------------------

klubdir = '/gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/'

# channel mapping of the considered channels
channelsMap = ['MuTau', 'ETau', 'TauTau', 'MuMu']

if '16APV' in run:
    script = 'scripts/submitHistoFiller_UL2016APV.py'
else:
    sys.exit(0)
os.chdir(klubdir)

# creating goodfiles
if checkGoodFiles:
    list_goodfiles = 'python scripts/listGoodAndBadFiles.py -d '+skim_name
    os.system(list_goodfiles)

# Loop through channels and execute commands
for it,ch in enumerate(channelsMap):
    if whichChannels[it]:
        # You may want a tag similar to ---> analysis_MuMu_UL2016APV_18Oct2023
        tag = 'analysis_'+ch+'_'+run+'_'+date
        config = 'config/mainCfg_'+ch+'_'+run+'.cfg'

        # Construct and execute the command      
        command = 'python '+script+' --cfg '+config+' --tag '+tag+' --n '+nJobs
        print command
        os.system(command)
