import os
import shutil
import argparse
import glob
import uproot
from concurrent.futures import ThreadPoolExecutor

#  usage :    
#    e.g.    
#             python check_skims_MT.py -d SKIMS_UL2016APV_01Dec23_ParticleNet_isAPV

klub_dir = '/gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis'
failed_jobs = "{}/scripts/failed_jobs.sh".format(klub_dir)

open(failed_jobs, 'w').close()

# -- official names ---
names = {
    # Data
    "SingleElectron_Run2016A" : "EGammaA",
    "SingleElectron_Run2016B" : "EGammaB",
    "SingleElectron_Run2016C" : "EGammaC",
    "SingleElectron_Run2016D" : "EGammaD",
    "SingleElectron_Run2016E" : "EGammaE",
    "SingleElectron_Run2016F" : "EGammaF",
    "Tau_Run2016A" : "TauA",
    "Tau_Run2016B" : "TauB",
    "Tau_Run2016C" : "TauC",
    "Tau_Run2016D" : "TauD",
    "Tau_Run2016E" : "TauE",
    "Tau_Run2016F" : "TauF",
    "SingleMuon_Run2016A" : "MuonA",
    "SingleMuon_Run2016B" : "MuonB",
    "SingleMuon_Run2016C" : "MuonC",
    "SingleMuon_Run2016D" : "MuonD",
    "SingleMuon_Run2016E" : "MuonE",
    "SingleMuon_Run2016F" : "MuonF",
    "MET_Run2016A" : "META",
    "MET_Run2016B" : "METB",
    "MET_Run2016C" : "METC",
    "MET_Run2016D" : "METD",
    "MET_Run2016E" : "METE",
    "MET_Run2016F" : "METF",

    # Signal
    "GluGluToRadionToHHTo2B2Tau_M-250" : "Rad250",
    "GluGluToRadionToHHTo2B2Tau_M-260" : "Rad260",
    "GluGluToRadionToHHTo2B2Tau_M-270" : "Rad270",
    "GluGluToRadionToHHTo2B2Tau_M-280" : "Rad280",
    "GluGluToRadionToHHTo2B2Tau_M-300" : "Rad300",
    "GluGluToRadionToHHTo2B2Tau_M-320" : "Rad320",
    "GluGluToRadionToHHTo2B2Tau_M-350" : "Rad350",
    "GluGluToRadionToHHTo2B2Tau_M-400" : "Rad400",
    "GluGluToRadionToHHTo2B2Tau_M-450" : "Rad450",
    "GluGluToRadionToHHTo2B2Tau_M-500" : "Rad500",
    "GluGluToRadionToHHTo2B2Tau_M-550" : "Rad550",
    "GluGluToRadionToHHTo2B2Tau_M-600" : "Rad600",
    "GluGluToRadionToHHTo2B2Tau_M-650" : "Rad650",
    "GluGluToRadionToHHTo2B2Tau_M-700" : "Rad700",
    "GluGluToRadionToHHTo2B2Tau_M-750" : "Rad750",
    "GluGluToRadionToHHTo2B2Tau_M-800" : "Rad800",
    "GluGluToRadionToHHTo2B2Tau_M-850" : "Rad850",
    "GluGluToRadionToHHTo2B2Tau_M-900" : "Rad900",
    "GluGluToRadionToHHTo2B2Tau_M-1000" : "Rad1000",
    "GluGluToRadionToHHTo2B2Tau_M-1250" : "Rad1250",
    "GluGluToRadionToHHTo2B2Tau_M-1500" : "Rad1500",
    "GluGluToRadionToHHTo2B2Tau_M-1750" : "Rad1750",
    "GluGluToRadionToHHTo2B2Tau_M-2000" : "Rad2000",
    "GluGluToRadionToHHTo2B2Tau_M-2500" : "Rad2500",
    "GluGluToRadionToHHTo2B2Tau_M-3000" : "Rad3000",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-250" : "Grav250",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-260" : "Grav260",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-270" : "Grav270",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-280" : "Grav280",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-300" : "Grav300",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-320" : "Grav320",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-350" : "Grav350",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-400" : "Grav400",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-450" : "Grav450",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-500" : "Grav500",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-550" : "Grav550",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-600" : "Grav600",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-650" : "Grav650",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-700" : "Grav700",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-750" : "Grav750",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-800" : "Grav800",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-850" : "Grav850",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-900" : "Grav900",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-1000" : "Grav1000",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-1250" : "Grav1250",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-1500" : "Grav1500",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-1750" : "Grav1750",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-2000" : "Grav2000",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-2500" : "Grav2500",
    "GluGluToBulkGravitonToHHTo2B2Tau_M-3000" : "Grav3000",

    # Background
    "TTToHadronic"     : "TT_Hadronic",
    "TTTo2L2Nu"        : "TT_FullyLep",
    "TTToSemiLeptonic" : "TT_SemiLep",

    "DYJetsToLL_M-50"                               : "DY_Incl",
    "DYJetsToLL_LHEFilterPtZ-0To50_MatchEWPDG20"    : "DY_PtZ0To50",
    "DYJetsToLL_LHEFilterPtZ-50To100_MatchEWPDG20"  : "DY_PtZ50To100",
    "DYJetsToLL_LHEFilterPtZ-100To250_MatchEWPDG20" : "DY_PtZ100To250",
    "DYJetsToLL_LHEFilterPtZ-250To400_MatchEWPDG20" : "DY_PtZ250To400",
    "DYJetsToLL_LHEFilterPtZ-400To650_MatchEWPDG20" : "DY_PtZ400To650",
    "DYJetsToLL_LHEFilterPtZ-650ToInf_MatchEWPDG20" : "DY_PtZ650ToInf",
    "DYJetsToLL_0J" : "DY_0J",
    "DYJetsToLL_1J" : "DY_1J",
    "DYJetsToLL_2J" : "DY_2J",

    "WJetsToLNu"              : "WJets_HT0To70", # for 0 < HT < 70
    "WJetsToLNu_HT-70To100"   : "WJets_HT70To100",
    "WJetsToLNu_HT-100To200"  : "WJets_HT100To200",
    "WJetsToLNu_HT-200To400"  : "WJets_HT200To400",
    "WJetsToLNu_HT-400To600"  : "WJets_HT400To600",
    "WJetsToLNu_HT-600To800"  : "WJets_HT600To800",
    "WJetsToLNu_HT-800To1200" : "WJets_HT800To1200",
    "WJetsToLNu_HT-1200To2500": "WJets_HT1200To2500",
    "WJetsToLNu_HT-2500ToInf" : "WJets_HT2500ToInf",

    "EWKWPlus2Jets_WToLNu_M-50"   : "EWKWPlus2Jets_WToLNu",
    "EWKWMinus2Jets_WToLNu_M-50"  : "EWKWMinus2Jets_WToLNu",
    "EWKZ2Jets_ZToLL_M-50"        : "EWKZ2Jets_ZToLL",

    "ST_tW_antitop_5f_inclusiveDecays"         : "ST_tW_antitop",
    "ST_tW_top_5f_inclusiveDecays"             : "ST_tW_top",
    "ST_t-channel_antitop_5f_InclusiveDecays"  : "ST_t-channel_antitop",
    "ST_t-channel_top_5f_InclusiveDecays"      : "ST_t-channel_top",

    "GluGluHToTauTau_M125"  : "GluGluHToTauTau",
    "VBFHToTauTau_M125"     : "VBFHToTauTau",
    "WplusHToTauTau_M125"   : "WplusHToTauTau",
    "WminusHToTauTau_M125"  : "WminusHToTauTau",
    "ZHToTauTau_M125"       : "ZHToTauTau",

    "ZH_HToBB_ZToLL" : "ZH_HToBB_ZToLL",
    "ZH_HToBB_ZToQQ" : "ZH_HToBB_ZToQQ",

    "ttHToNonbb_M125"  : "ttHToNonbb",
    "ttHTobb_M125"     : "ttHTobb",
    "ttHToTauTau_M125" : "ttHToTauTau",
    
    "WW" : "WW",
    "WZ" : "WZ",
    "ZZ" : "ZZ",

    "WWW_4F" : "WWW",
    "WWZ_4F" : "WWZ",
    "WZZ"    : "WZZ",
    "ZZZ"    : "ZZZ",

    "TTWJetsToLNu"     : "TTWJetsToLNu",
    "TTWJetsToQQ"      : "TTWJetsToQQ",
    "TTZToLLNuNu_M-10"  : "TTZToLLNuNu",
    "TTZToQQ"          : "TTZToQQ",
    "TTWW" : "TTWW",
    "TTZZ" : "TTZZ", 
    "TTWZ" : "TTWZ",

    "TTWH" : "TTWH",
    "TTZH" : "TTZH",

    "GluGluToHHTo2B2Tau" : "GluGluToHHTo2B2Tau"
}

# Switch keys and values
skims = {value: key for key, value in names.items()}



def check_closed(root_file):
    try:
        with uproot.open(root_file) as file:
            tree = file["HTauTauTree"]
            return True
    except:
        return False

def process_files(directory,flag_root):
    print("Processing directory: {}".format(directory))
    os.chdir(directory) 

    # txt files
    open("goodfiles.txt", 'w').close()
    open("badfiles.txt", 'w').close()

    logfiles = glob.glob("output_*.log")
    rootfiles = glob.glob("output_*.root")

    with ThreadPoolExecutor(max_workers=10) as executor:
        log_futures = []
        for logfile in logfiles:
            log_futures.append(executor.submit(process_log_file, logfile, directory))

        root_futures = []
        if flag_root:
            for rootfile in rootfiles:
                root_futures.append(executor.submit(process_root_file, rootfile, directory))
        else:
            root_futures=[]

        for future in log_futures + root_futures:
            future.result()

    print("Processing complete.")
    os.chdir("..") 


# check if log files contain any error
def process_log_file(logfile, directory):
    tmp = logfile.split('_')
    idx = tmp[1].split('.')[0]
    
    with open(logfile, 'r') as log_file:
        log_content = log_file.read()
        
        if "R__unzip: error" in log_content:
            print("job num {}: file corrupted".format(idx))
            with open("badfiles.txt", 'a') as bad_file:
                bad_file.write("{}\n".format(os.path.join(directory, "output_" + idx + ".root")))                    
            with open(failed_jobs, 'a') as fail_jobs:
                fail_jobs.write("condor_submit {}/{}/SKIM_{}/condorLauncher_{}.sh\n".format(klub_dir,directory.split("/")[-2],skims[directory.split("/")[-1]], idx))

        elif "... SKIM finished, exiting." not in log_content:
            print("job num {}: file not correctly finished".format(idx))
            with open("badfiles.txt", 'a') as bad_file:
                bad_file.write("{}\n".format(os.path.join(directory, "output_" + idx + ".root")))
            with open(failed_jobs, 'a') as fail_jobs:
                fail_jobs.write("condor_submit {}/{}/SKIM_{}/condorLauncher_{}.sh\n".format(klub_dir,directory.split("/")[-2],skims[directory.split("/")[-1]], idx))

        else:
            with open("goodfiles.txt", 'a') as good_file:
                good_file.write("{}\n".format(os.path.join(directory, "output_" + idx + ".root")))

# check if root files have been properly closed
def process_root_file(rootfile, directory):
    tmp = rootfile.split('_')
    idx = tmp[1].split('.')[0]
    root_path = "{}".format(os.path.join(directory, rootfile))
    if not check_closed(root_path):
        print("job num {}: file not correctly closed".format(idx))
        with open("badfiles.txt", 'a') as unclosed_file:
            unclosed_file.write("{}\n".format(os.path.join(directory, rootfile)))
        with open(failed_jobs, 'a') as fail_jobs:
            fail_jobs.write("condor_submit {}/{}/SKIM_{}/condorLauncher_{}.sh\n".format(klub_dir,directory.split("/")[-2],skims[directory.split("/")[-1]], idx))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check good and bad files")
    parser.add_argument('-b', '--baseDir', help='Path of the base skim directory', default="/gwdata/users/spalluotto/ResonantHHbbtautauAnalysis/", required=False)
    parser.add_argument('-d', '--direc', help='Path of the specific skim directory', required=True)
    parser.add_argument('-r', '--rootFiles', help='Check if root files have been properly closed', required=False, action='store_true')
    
    args = parser.parse_args()

    skimDir = os.path.join(args.baseDir, args.direc)

    print("skim dir: ", skimDir)

    # check if the provided directory contains subdirectories
    subdirs = [subdir for subdir in os.listdir(skimDir) if os.path.isdir(os.path.join(skimDir, subdir))]

    if subdirs:
        for subdir in subdirs:
            full_path = os.path.join(skimDir, subdir)
            process_files(full_path,args.rootFiles)
    else:
        process_files(skimDir,args.rootFiles)
