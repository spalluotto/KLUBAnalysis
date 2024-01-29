#!/usr/bin/env python
import os
import sys
import argparse


# ----- EDIT HERE ----
run = 'UL2016APV'
date = '26Jan24_isLeptTrigger_newBoosted'
whichChannels = [False, False, True, False]   # you may want to run one or more channels
# --------------------

klubdir = '/gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/'

# channel mapping of the considered channels
channelsMap = ['TauTau', 'MuTau', 'ETau', 'MuMu']

script = 'scripts/combineFillerOutputs.py'

print("Current Directory:   ", os.getcwd())
os.chdir(klubdir)

print 'after ', os.getcwd()

# Loop through channels and execute commands
for it,ch in enumerate(channelsMap):
    if whichChannels[it]:
        # You may want a tag similar to ---> analysis_MuMu_UL2016APV_18Oct2023
        tag = 'analysis_'+ch+'_'+run+'_'+date
        config = 'mainCfg_'+ch+'_'+run+'.cfg'

        # Construct and execute the command      
        command = 'python '+script+' --cfg '+config+' --tag '+tag+' --dir '+klubdir
        print command
        os.system(command)
