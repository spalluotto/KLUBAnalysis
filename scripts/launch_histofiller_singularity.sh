TAG=2024_12_10_bkgCor
BASE_DIR=/gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/

cd $BASE_DIR

# python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL17 --channel ETau
# python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL17 --channel MuTau
# python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL17 --channel TauTau

# python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL16 --channel ETau
# python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL16 --channel MuTau
# python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL16 --channel TauTau

# python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL18 --channel ETau
# python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL18 --channel MuTau
# python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL18 --channel TauTau

python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL16APV --channel ETau
python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL16APV --channel MuTau
python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL16APV --channel TauTau
