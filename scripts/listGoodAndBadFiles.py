import os
import shutil
import argparse
import glob

#  usage :    
#    e.g.    
#             python listGoodAndBadFiles.py -d SKIMS_UL2016APV_01Dec23_ParticleNet_isAPV

def process_files(directory):
    print("Processing directory: {}".format(directory))

    os.chdir(directory)  # Change to the directory

    open("goodfiles.txt", 'w').close()
    open("badfiles.txt", 'w').close()
    
    logfiles = glob.glob("output_*.log")
    
    if logfiles:
        for logfile in logfiles:
            tmp = logfile.split('_')
            idx = tmp[1].split('.')[0]

            with open(logfile, 'r') as log_file:
                log_content = log_file.read()

                if "R__unzip: error" in log_content:
                    print("job num {}: file corrupted".format(idx))
                    with open("badfiles.txt", 'a') as bad_file:
                            bad_file.write("{}\n".format(os.path.join(directory, "output_" + idx + ".root")))
                elif "... SKIM finished, exiting." not in log_content:
                    print("job num {}: file not correctly finished".format(idx))
                    with open("badfiles.txt", 'a') as bad_file:
                            bad_file.write("{}\n".format(os.path.join(directory, "output_" + idx + ".root")))
                else:
                    with open("goodfiles.txt", 'a') as good_file:
                        good_file.write("{}\n".format(os.path.join(directory, "output_" + idx + ".root")))

    print("Processing complete.")
    os.chdir("..")  # Change back to the original directory


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check good and bad files")
    parser.add_argument('-b', '--baseDir', help='Path of the base skim directory', default="/gwdata/users/spalluotto/ResonantHHbbtautauAnalysis/", required=False)
    parser.add_argument('-d', '--direc', help='Path of the specific skim directory', required=True)
    args = parser.parse_args()

    skimDir = os.path.join(args.baseDir, args.direc)

    print("skim dir: ", skimDir)

    # Check if the provided directory contains subdirectories
    subdirs = [subdir for subdir in os.listdir(skimDir) if os.path.isdir(os.path.join(skimDir, subdir))]

    if subdirs:
        # Iterate through subdirectories
        for subdir in subdirs:
            full_path = os.path.join(skimDir, subdir)
            process_files(full_path)
    else:
        # Check the root files directly in the provided directory
        process_files(skimDir)
