import os
import ROOT

# questo puo girare su singularity e vuole root quindi devi fare cmsenv

verbose = False
overwrite_flag = True # if you want to overwrite already existing goodfiles



# Base path of the directory containing the samples
dir_path = "/gwdata/users/spalluotto/ResonantHHbbtautauAnalysis/"
tag = 'SKIMS_UL2016APV_04Feb2025_Backgrounds/'
base_path = "{}/{}".format(dir_path, tag)

# Function to check the last line of a log file
def check_log(log_file):
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
            if lines and lines[-1].strip() == "... SKIM finished, exiting.":
                return True
            else:
                return False
    except Exception as e:
        print "Error reading the file {}: {}".format(log_file, e)
        return False

# Function to check if a ROOT file is valid
def is_good_file(fname, verb):
    try:
        f = ROOT.TFile(fname)
        if f.IsZombie():
            if verb:
                print "ROOT file {} is a zombie.".format(fname)
            return False
        if f.TestBit(ROOT.TFile.kRecovered):
            if verb:
                print "ROOT file {} is recovered.".format(fname)
            return False

        tree = f.Get("HTauTauTree")
        try:
            tree.GetEntries()
        except AttributeError:
            if verb:
                print 'The HTauTauTree does not exist in {}.'.format(fname)
            return False
        return True
    except Exception as e:
        if verb:
            print "Error in ROOT file {}: {}".format(fname, e)
        return False

# Function to check if a file exists
def file_exists(afile, verb):
    if not os.path.exists(afile):
        if verb:
            print 'File {} is missing.'.format(afile)
        return False
    return True

# Function to find error messages in the log file
def find_error_messages(afile, verb):
    with open(afile, 'r') as f:
        problems = [w for w in f.readlines()
                if ((('Error' in w or 'ERROR' in w) and
                'WARNING' not in w and 'Warning' not in w and 'TCling' not in w) or
                 ('bus error' in w) or
                 ('R__unzip: error' in w) or
                 ('SysError in <TFile::WriteBuffer>: error writing to file' in w) or
                 ('The system macro SYSTEM_PERIODIC_REMOVE expression' in w)) and
                'Error in <TROOT::TVector2::Phi_mpi_pi>: function called with NaN' not in w]
        if len(problems) != 0:
            if verb:
                mes = 'Found errors in file {}:\n'.format(afile)
                for problem in problems:
                    mes += '  {}'.format(problem)
                print mes
            return True
    return False

# Function to debug and print out information
def debug_print(message, verb):
    if verb:
        print message

# Main function to traverse the sample directories
def check_samples(base_path, verb=False, overwrite=False):
    # Iterate through the main sample directories
    debug_print("Starting to process the sample directories...", verb)
    
    for sample_dir in os.listdir(base_path):
        sample_path = os.path.join(base_path, sample_dir)
        if os.path.isdir(sample_path):
            print("Processing directory: {}".format(sample_path))
            good_files = []
            bad_files = []
            
            # Check if goodfiles.txt or badfiles.txt already exist
            goodfiles_exists = os.path.exists(os.path.join(sample_path, 'goodfiles.txt'))
            badfiles_exists = os.path.exists(os.path.join(sample_path, 'badfiles.txt'))
            
            # Skip processing if files exist and overwrite is False
            if (goodfiles_exists or badfiles_exists) and not overwrite:
                debug_print("Skipping directory {}: goodfiles.txt or badfiles.txt already exists.".format(sample_path), verb)
                continue
            
            # Iterate through the files inside each sample directory
            for root_file in os.listdir(sample_path):
                if root_file.endswith('.root'):
                    root_path = os.path.join(sample_path, root_file)
                    log_file = root_file.replace('.root', '.log')
                    log_path = os.path.join(sample_path, log_file)
                    
                    debug_print("Checking file: {}".format(root_file), verb)
                    
                    # Check if the ROOT file is good and if the log file contains the desired last line
                    if (file_exists(root_path, verb) and
                        check_log(log_path) and
                        is_good_file(root_path, verb) and
                        not find_error_messages(log_path, verb)):
                        debug_print("File {} is good.".format(root_file), verb)
                        good_files.append(root_path)
                    else:
                        debug_print("File {} is bad.".format(root_file), verb)
                        bad_files.append(root_path)
            
            # Save the results in goodfiles.txt and badfiles.txt if they don't already exist or overwrite is enabled
            if good_files or bad_files:
                debug_print("Writing good files to goodfiles.txt and bad files to badfiles.txt...", verb)
                
                if not goodfiles_exists or overwrite:
                    with open(os.path.join(sample_path, 'goodfiles.txt'), 'w') as gf:
                        for file in good_files:
                            gf.write(file + '\n')
                
                if not badfiles_exists or overwrite:
                    with open(os.path.join(sample_path, 'badfiles.txt'), 'w') as bf:
                        for file in bad_files:
                            bf.write(file + '\n')
            else:
                debug_print("No good or bad files found in directory: {}".format(sample_path), verb)

# Run the main function with the verbosity flag for error messages
debug_print("Starting the script...", verb=verbose)
check_samples(base_path, verb=verbose, overwrite=overwrite_flag)
debug_print("Script finished.", verb=verbose)
