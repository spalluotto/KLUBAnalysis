TAG=2024_11_26_bkgSF
BASE_DIR=/gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/

cd $BASE_DIR
# python scripts/combineFillerOutputs.py --dir $BASE_DIR --tag $TAG --channel ETau --year UL16APV --cfg mainCfg_ETau_UL16APV.cfg
# python scripts/combineFillerOutputs.py --dir $BASE_DIR --tag $TAG --channel MuTau --year UL16APV --cfg mainCfg_MuTau_UL16APV.cfg
# python scripts/combineFillerOutputs.py --dir $BASE_DIR --tag $TAG --channel TauTau --year UL16APV --cfg mainCfg_TauTau_UL16APV.cfg
python scripts/combineFillerOutputs.py --dir $BASE_DIR --tag $TAG --channel MuMu --year UL16APV --cfg mainCfg_MuMu_UL16APV.cfg

# python scripts/combineFillerOutputs.py --dir $BASE_DIR --tag $TAG --channel ETau --year UL16 --cfg mainCfg_ETau_UL16.cfg
# python scripts/combineFillerOutputs.py --dir $BASE_DIR --tag $TAG --channel MuTau --year UL16 --cfg mainCfg_MuTau_UL16.cfg
# python scripts/combineFillerOutputs.py --dir $BASE_DIR --tag $TAG --channel TauTau --year UL16 --cfg mainCfg_TauTau_UL16.cfg
# python scripts/combineFillerOutputs.py --dir $BASE_DIR --tag $TAG --channel MuMu --year UL16 --cfg mainCfg_MuMu_UL16.cfg

python scripts/combineFillerOutputs.py --dir $BASE_DIR --tag $TAG --channel ETau --year UL17 --cfg mainCfg_ETau_UL17.cfg
# python scripts/combineFillerOutputs.py --dir $BASE_DIR --tag $TAG --channel MuTau --year UL17 --cfg mainCfg_MuTau_UL17.cfg
# python scripts/combineFillerOutputs.py --dir $BASE_DIR --tag $TAG --channel TauTau --year UL17 --cfg mainCfg_TauTau_UL17.cfg
python scripts/combineFillerOutputs.py --dir $BASE_DIR --tag $TAG --channel MuMu --year UL17 --cfg mainCfg_MuMu_UL17.cfg

# python scripts/combineFillerOutputs.py --dir $BASE_DIR --tag $TAG --channel ETau --year UL18 --cfg mainCfg_ETau_UL18.cfg
# python scripts/combineFillerOutputs.py --dir $BASE_DIR --tag $TAG --channel MuTau --year UL18 --cfg mainCfg_MuTau_UL18.cfg
# python scripts/combineFillerOutputs.py --dir $BASE_DIR --tag $TAG --channel TauTau --year UL18 --cfg mainCfg_TauTau_UL18.cfg
# python scripts/combineFillerOutputs.py --dir $BASE_DIR --tag $TAG --channel MuMu --year UL18 --cfg mainCfg_MuMu_UL18.cfg
