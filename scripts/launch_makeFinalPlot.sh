TAG=test5
BASE_DIR=/gwpool/users/spalluotto/HH_bbtautau/Run2/CMSSW_11_1_9/src/KLUBAnalysis/

cd $BASE_DIR

python3 scripts/makeFinalPlots.py --tag ${TAG}_UL18 --year 2018 --channels ETau --categories boostedL_pnet --region SR --singlethreaded --rebin 2
#python3 scripts/makeFinalPlots.py --tag ${TAG}_UL18 --year 2018 --channels ETau --categories ttbarCR --region SR --singlethreaded
#python3 scripts/makeFinalPlots.py --tag ${TAG}_UL18 --year 2018 --channels ETau --categories dyCR --region SR --singlethreaded
python3 scripts/makeFinalPlots.py --tag ${TAG}_UL18 --year 2018 --channels ETau --categories res1b --region SR --singlethreaded
python3 scripts/makeFinalPlots.py --tag ${TAG}_UL18 --year 2018 --channels ETau --categories res2b --region SR --singlethreaded
