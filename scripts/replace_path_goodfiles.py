import os

def update_goodfiles_paths(root_dir):
    # Iterate through all subdirectories
    for subdir, _, files in os.walk(root_dir):
        # Check if 'goodfiles.txt' exists in the current directory
        if "goodfiles.txt" in files:
            goodfiles_path = os.path.join(subdir, "goodfiles.txt")
            new_lines = []
            
            # Read the content of 'goodfiles.txt'
            with open(goodfiles_path, 'r') as file:
                lines = file.readlines()
            
            # Replace paths
            for line in lines:
                line = line.strip()  # Remove leading/trailing whitespace
                if line:  # Skip empty lines
                    filename = os.path.basename(line)  # Extract the file name (e.g., output_X.root)
                    new_path = os.path.join(subdir, filename)  # Create the new path
                    new_lines.append(new_path)


            # testing
            print("\n".join(new_lines))
            return

            # writing 
            # # Overwrite 'goodfiles.txt' with the updated paths
            # with open(goodfiles_path, 'w') as file:
            #     file.write("\n".join(new_lines))
            
            # # Print confirmation for the updated file
            # print(f"Updated: {goodfiles_path}")




# Specify the root directory containing the subdirectories
direc = '/eos/cms/store/group/phys_b2g/HHbbtautau/skims_2018/'
update_goodfiles_paths(direc)
