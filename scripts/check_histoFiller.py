import os

tag='2024_11_26_bkgSF_UL17'

path = f'/gwpool/users/spalluotto/HH_bbtautau/CMSSW_11_1_9/src/KLUBAnalysis/{tag}/'


# ------ functions -----
def read_last_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return lines[-1].strip() if lines else None

def read_second_last_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return lines[-2].strip() if len(lines) > 1 else None

def check_logs(super_folder):
    channels_status = {}
    
    for subfolder in os.listdir(super_folder):
        subfolder_path = os.path.join(super_folder, subfolder)
        
        if os.path.isdir(subfolder_path):
            logs_dir = os.path.join(subfolder_path, 'logs')
            if os.path.isdir(logs_dir):
                issues_found = False
                for file_name in os.listdir(logs_dir):
                    if file_name.endswith('.out'):
                        file_path = os.path.join(logs_dir, file_name)
                        last_line = read_last_line(file_path)
                        second_last_line = read_second_last_line(file_path)

                        if last_line != "[INFO::testAnalysisHelper] Exiting.":
                            print(f"Error in {file_path}: Last line is not '[INFO::testAnalysisHelper] Exiting.'")
                            issues_found = True
                        elif second_last_line != "@@ ... saving completed, closing output file":
                            print(f"Error in {file_path}: Second last line is not '@@ ... saving completed, closing output file'")
                            issues_found = True
                
                channels_status[subfolder] = "All files are correct." if not issues_found else "Some files have issues."

    # Print summary at the end
    for channel, status in channels_status.items():
        print(f"Channel {channel}: {status}")



# ---- main

check_logs(path)
