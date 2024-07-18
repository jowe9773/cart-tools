#testing_parsing.py

import os
import re
from collections import defaultdict
from file_managers import FileManagers
fm = FileManagers()

# Define the root directory
root_dir = fm.load_dn("Select a data directory")

# Regex pattern to match filenames starting with "experimentdate_experiment#_"
pattern = re.compile(r'(\d{8})_exp(\d+)_')

# Dictionary to store grouped files
grouped_files = defaultdict(list)

# Walk through the directory and its subdirectories
for subdir, _, files in os.walk(root_dir):
    for file in files:
        match = pattern.match(file)
        if match:
            date = match.group(1)
            experiment_number = match.group(2)
            key = f"{date}_exp{experiment_number}"
            full_path = os.path.join(subdir, file)
            grouped_files[key].append(full_path)

for key in grouped_files:
    print(key)
    fm.parse_directory(grouped_files[key])
