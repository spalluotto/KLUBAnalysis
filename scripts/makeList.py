import os
import re

tag_in = 'signals_2016APV_27Nov2024_Others'
tag_out = 'UL16APV_Signals'

root_dir = f"/gwteras/cms/store/user/dzuolo/ResonantHHbbtautauNtuples/{tag_in}/"
output_dir = f"/gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/inputFiles/{tag_out}"
os.makedirs(output_dir, exist_ok=True)


# Function to clean the sample name
def clean_sample_name(sample_name):
    # Remove the leading number and underscore
    sample_name = re.sub(r"^\d+_", "", sample_name)
    # Truncate everything after "_TuneCP5"
    sample_name = re.split(r"_TuneCP5", sample_name)[0]
    return sample_name

# Iterate through the directory structure
for sample in os.listdir(root_dir):
    sample_path = os.path.join(root_dir, sample)
    if os.path.isdir(sample_path):  # Check if it is a directory
        # Clean the sample name
        cleaned_sample_name = clean_sample_name(sample)
        
        # Path for the .txt file
        txt_file = os.path.join(output_dir, f"{cleaned_sample_name}.txt")
        
        with open(txt_file, "w") as f:
            for root, _, files in os.walk(sample_path):
                for file in files:
                    if file.endswith(".root"):  # Filter for .root files
                        full_path = os.path.join(root, file)
                        f.write(full_path + "\n")  # Write the full path to the .txt file

print(f"Text files (.txt) generated in: {output_dir}")
