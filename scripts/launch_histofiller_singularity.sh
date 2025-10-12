TAG=test5
BASE_DIR=/gwpool/users/spalluotto/HH_bbtautau/Run2/CMSSW_11_1_9/src/KLUBAnalysis/

cd $BASE_DIR

# python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/Run2/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL17 --channel ETau
# python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/Run2/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL17 --channel MuTau
# python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/Run2/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL17 --channel TauTau

# python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/Run2/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL16 --channel ETau
# python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/Run2/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL16 --channel MuTau
# python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/Run2/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL16 --channel TauTau

python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/Run2/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL18 --channel ETau --njobs 400
#python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/Run2/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL18 --channel MuTau --njobs 300
#python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/Run2/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL18 --channel TauTau

# python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/Run2/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL16APV --channel ETau
# python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/Run2/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL16APV --channel MuTau
# python3 scripts/submitHistoFiller_singularity.py -o /gwpool/users/spalluotto/HH_bbtautau/Run2/CMSSW_11_1_9/src/KLUBAnalysis/ -t $TAG --year UL16APV --channel TauTau
