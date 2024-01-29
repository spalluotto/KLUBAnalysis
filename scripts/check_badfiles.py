import os
import argparse

# usage
#      e.g.
#             python check_badfiles.py -d SKIMS_UL2016APV_11Nov23_ParticleNet

def check_single_folder(folder_path):
    badfiles_path = os.path.join(folder_path, "badfiles.txt")
    print("sto controllando qui ", badfiles_path)

    if os.path.isfile(badfiles_path):
        with open(badfiles_path, 'r') as bad_file:
            content = bad_file.read()
            if content.strip():
                print("{}".format(folder_path))
                with open("list_skims_with_badfiles.txt", 'a') as non_empty_file:
                    non_empty_file.write("{}\n".format(folder_path))
    else:
        print("The badfiles.txt does not exist in {}.".format(folder_path))

def check_badfiles(folder):
    print("Checking badfiles.txt in {}".format(folder))

    # Check the provided folder
    check_single_folder(folder)

    # Check subfolders
    for subdir in os.listdir(folder):
        full_path = os.path.join(folder, subdir)
        if os.path.isdir(full_path):
            check_single_folder(full_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check badfiles.txt in a folder and its subfolders")
    parser.add_argument('-b', '--baseDir', help='Path of the base skim directory', default="/gwdata/users/spalluotto/ResonantHHbbtautauAnalysis/", required=False)
    parser.add_argument('-d', '--direc', help='Path of the specific skim directory', required=True)
    args = parser.parse_args()

    skimDir = os.path.join(args.baseDir, args.direc)

    check_badfiles(skimDir)
