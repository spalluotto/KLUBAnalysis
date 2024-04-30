#!/usr/bin/env python
import os
import sys
import argparse


# ----- EDIT HERE ----
run = 'UL16APV'
date = ''
whichChannels = [True, True, True, True]   # you may want to run one or more channels
nJobs = '250'

checkGoodFiles = False
# --------------------

klubdir = '/gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/'

# channel mapping of the considered channels
channelsMap = ['MuTau', 'ETau', 'TauTau', 'MuMu']

if '16APV' in run:
    script = 'scripts/submitHistoFiller_UL2016APV.py'
elif 'UL16' == run:
    script = 'scripts/submitHistoFiller_UL2016.py'
else:
    sys.exit(0)
os.chdir(klubdir)


# Loop through channels and execute commands
for it,ch in enumerate(channelsMap):
    if whichChannels[it]:
        tag = 'analysis_'+ch+'_'+run+'_'+date
        config = 'config/mainCfg_'+ch+'_'+run+'.cfg'

        # Construct and execute the command      
        command = 'python '+script+' --cfg '+config+' --tag '+tag+' --n '+nJobs
        print command
        os.system(command)
