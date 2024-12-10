import os
from sample_name_mapping import *


tag = 'SKIMS_UL2016APV_06Dec2024_corBkg'



def check_badfiles_and_generate_script(root_dir, condor_dir, sample_name=None):
    """
    Checks 'badfiles.txt' files for errors in ROOT samples and generates a shell script
    to resubmit failed jobs using condor_submit.

    :param root_dir: Path to the main directory containing the ROOT file samples.
    :param condor_dir: Path to the main directory containing the condorLauncher scripts.
    :param sample_name: Name of a specific ROOT sample to check. If None, checks all samples.
    """
    if not os.path.isdir(root_dir):
        print(f"Error: The directory '{root_dir}' does not exist.")
        return

    if not os.path.isdir(condor_dir):
        print(f"Error: The directory '{condor_dir}' does not exist.")
        return

    # Reverse the mapping: from value to key
    reverse_mapping = {v: k for k, v in names.items()}

    # Output script file
    output_script_path = os.path.join(os.getcwd(), "resubmit_badfiles.sh")
    with open(output_script_path, "w") as script_file:
        script_file.write("#!/bin/bash\n\n")  # Add shebang for bash script
        
        # Determine which samples to check
        samples_to_check = [sample_name] if sample_name else os.listdir(root_dir)
        
        for root_sample in samples_to_check:
            root_sample_path = os.path.join(root_dir, root_sample)
            print(root_sample)
            
            # Check if the ROOT sample path exists and is a directory
            if not os.path.isdir(root_sample_path):
                continue

            badfiles_path = os.path.join(root_sample_path, "badfiles.txt")
            
            if os.path.exists(badfiles_path):
                with open(badfiles_path, "r") as badfiles:
                    # Read the list of bad files
                    badfiles_list = [line.strip() for line in badfiles if line.strip()]
                    
                    if badfiles_list:  # Process only if there are bad files
                        for badfile in badfiles_list:
                            # Extract the partition number from the filename (e.g., "output_1.root")
                            filename = os.path.basename(badfile)
                            if "output_" in filename and filename.endswith(".root"):
                                partition_number = filename.split("_")[1].replace(".root", "")
                                print("\n\n",partition_number)
                                if partition_number.isdigit():
                                    print("oppla")
                                    # Map the ROOT sample name to the condorLauncher key
                                    condor_sample_name = reverse_mapping.get(root_sample, root_sample)
                                    print(condor_sample_name)
                                    condor_sample_path = os.path.join(condor_dir, "SKIM_{}".format(condor_sample_name))
                                    print(condor_sample_path)
                                    if os.path.isdir(condor_sample_path):
                                        condor_script = os.path.join(
                                            condor_sample_path, f"condorLauncher_{partition_number}.sh"
                                        )
                                        # Write the condor_submit command
                                        script_file.write(f"condor_submit {condor_script}\n")

    print(f"Resubmission script created: {output_script_path}")
    # Make the script executable
    os.chmod(output_script_path, 0o755)

# Example usage:
# Specify the directories and optionally the name of a specific sample.
root_directory = "/gwdata/users/spalluotto/ResonantHHbbtautauAnalysis/{}".format(tag)
condor_directory = "/gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/{}".format(tag)

check_badfiles_and_generate_script(root_directory, condor_directory)  # Check all samples
# check_badfiles_and_generate_script(root_directory, condor_directory, "specific_sample_name")  # Check a specific sample
