import os
from file_managers import FileManagers

def batch_rename_files(directory, old_date, new_date):
    # Get a list of all files in the directory
    files = os.listdir(directory)
    
    # Loop through each file and rename it
    for filename in files:
        # Check if the old_date is in the filename
        if old_date in filename:
            # Create the new filename
            new_name = filename.replace(old_date, new_date)
            
            # Create the full path to the old and new filenames
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_name)
            
            # Rename the file
            os.rename(old_file, new_file)
            print(f'Renamed: {old_file} to {new_file}')

# Usage

fm = FileManagers()

directory = fm.load_dn("Choose folder with fucked up filenames")  # Replace with the path to your directory
fuckup = 'nowood'
replacement = 'wood'

batch_rename_files(directory, fuckup, replacement)
