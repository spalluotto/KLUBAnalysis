import os
import re

tag_in = 'data_2016APV_17Jan2025'
tag_out = 'UL16APV_Data'

root_dir = f"/gwteras/cms/store/user/dzuolo/ResonantHHbbtautauNtuples/{tag_in}/"
output_dir = f"/gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/inputFiles/{tag_out}"
os.makedirs(output_dir, exist_ok=True)


# Function to clean the sample name
def clean_sample_name(sample_name):
    sample_name = re.sub(r"^\d+_", "", sample_name)
    sample_name = re.split(r"_TuneCP5", sample_name)[0]
    return sample_name

# Iterate through the directory structure
for sample in os.listdir(root_dir):
    sample_path = os.path.join(root_dir, sample)
    if os.path.isdir(sample_path):
        cleaned_sample_name = clean_sample_name(sample)
        txt_file = os.path.join(output_dir, f"{cleaned_sample_name}.txt")
        with open(txt_file, "w") as f:
            for root, _, files in os.walk(sample_path):
                for file in files:
                    if file.endswith(".root"):
                        full_path = os.path.join(root, file)
                        f.write(full_path + "\n")

print(f"Text files (.txt) generated in: {output_dir}")
