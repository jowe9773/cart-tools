#testing_parsing.py

import os
import re
import pandas as pd
from pprint import pprint
from pathlib import Path
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

        if "_summary" in file:
            summary = Path(os.path.join(subdir, file)).as_posix()


#lets set up our experiment metadata (what type of experiment was run?)
if summary is not None:
    #read summary csv into pandas df
    summary_df = pd.read_excel(summary)
    #print(summary_df)

    #make a dictionary that contains keys(experiment names) and values (list of floodtype, congestion, forest stand)
    experiment_deets = {}

    for index, row in summary_df.iterrows():
        if index >=2:
            #grad experiment name
            experiment = row["Experiment Name"]

            #grab flood type
            flood_type = row["Flood type"]

            #grab transport regime
            congestion = row["Congestion"]

            #grab flood magnitude
            tree_spacing = row["Forest Stand Density"]

            #create a list of these attributes and append it to the dictionary
            experiment_deets[f"{experiment}"] = [flood_type, congestion, tree_spacing]

for key in grouped_files:
    print(" ")
    print(key)
    #pprint(grouped_files[key])
    filenames = fm.sort_files(grouped_files[key])
    #pprint(filenames)

    #lets check to see if the neccesary files are present
    if key in experiment_deets:
        experimental_setup = experiment_deets[f"{key}"]
        #print(experimental_setup)

        #check files that all experiments should have
        if "ocs" not in filenames:
            print("Missing ocean control file")

        if "counts" not in filenames:
            print("Missing field notes file")

        if "density" not in filenames:
            print("Missing density data file")

        if "flowlog" not in filenames:
            print("Missing flow log data")

        if "notes" not in filenames:
            print("Missing experiment notes file")

        #now based on the flood type lets check if the neccesary files are there
        if experimental_setup[0] is 'H':
            if "nowood_sick .DAT" not in filenames:
                print("Missing nowood_sick.dat")
            
            if "nowood_sick .XML" not in filenames:
                print("Missing nowood_sick.xml")

            if "wood_sick .DAT" not in filenames:
                print("Missing wood_sick.dat")
            
            if "wood_sick .XML" not in filenames:
                print("Missing wood_sick.xml")
            
            
            if "nowood_massa_scan1" not in filenames:
                print("Missing both nowood massa scans")

            if "nowood_massa_scan2" not in filenames:
                print("Missing second nowood massa scan")

            if "wood_massa_scan1" not in filenames:
                print("Missing both wood massa scans")

            if "wood_massa_scan2" not in filenames:
                print("Missing second wood massa scan")

        if experimental_setup[0] is 'L':
            if "nowood_sick .DAT" not in filenames:
                print("Missing nowood_sick.dat")
            
            if "nowood_sick .XML" not in filenames:
                print("Missing nowood_sick.xml")

            if "wood_sick .DAT" not in filenames:
                print("Missing wood_sick.dat")
            
            if "wood_sick .XML" not in filenames:
                print("Missing wood_sick.xml")

            if "remobilization_sick .DAT" not in filenames:
                print("Missing remobilization_sick.DAT")

            if "remobilization_sick .XML" not in filenames:
                print("Missing remobilization_sick.XML")

            
            if "nowood_massa_scan1" not in filenames:
                print("Missing both nowood massa scans")

            if "nowood_massa_scan2" not in filenames:
                print("Missing second nowood massa scan")

            if "wood_massa_scan1" not in filenames:
                print("Missing both wood massa scans")

            if "wood_massa_scan2" not in filenames:
                print("Missing second wood massa scan")

            if "remobilization_massa_scan1" not in filenames:
                print("Missing both remobilization massa scans")

            if "remobilization_massa_scan2" not in filenames:
                print("Missing second remobilization massa scan")

        if experimental_setup[0] is 'A':
            if "pre_sick .DAT" not in filenames:
                print("Missing pre_sick.dat")
            
            if "pre_sick .XML" not in filenames:
                print("Missing pre_sick.xml")

            if "post_sick .DAT" not in filenames:
                print("Missing post_sick.dat")
            
            if "post_sick .XML" not in filenames:
                print("Missing post_sick.xml")

            
            if "autoc_massa_scan1" not in filenames:
                print("Missing both autoc massa scans")

            if "autoc_massa_scan2" not in filenames:
                print("Missing second autoc massa scan")
                
    else: 
        print("No experiment details in summary")
