#file_managers.py
"""module containing methods for managing files"""

#import necessary packages
import os
import re
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import pandas as pd


class FileManagers:
    """Class contains methods for managing files"""

    def __init__(self):
        print("initialized")

    def load_dn(self, purpose):
        """this function opens a tkinter GUI for selecting a 
        directory and returns the full path to the directory 
        once selected
        
        'purpose' -- provides expanatory text in the GUI
        that tells the user what directory to select"""

        root = tk.Tk()
        root.withdraw()
        directory_name = filedialog.askdirectory(title = purpose)

        return directory_name

    def load_fn(self, purpose):
        """this function opens a tkinter GUI for selecting a 
        file and returns the full path to the file 
        once selected
        
        'purpose' -- provides expanatory text in the GUI
        that tells the user what file to select"""

        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(title = purpose)

        return filename


    def parse_directory(self, root_dir):
        """Goes through all files in a directory and all subdirectories and groups them by experiment name. 
        Outputs a dictionary of lists where the keys in the dictionary are the experiment names and the 
        lists are lists of all related files"""


        # Regex pattern to match filenames starting with "experimentdate_experiment#_"
        pattern = re.compile(r'(\d{8})_exp(\d+)_')

        # Dictionary to store grouped files
        grouped_files = defaultdict(list)

        #variable to store summary file
        summary = None

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

                if "summary" in file:
                    summary = os.path.join(subdir, file)
                    print("Summary file present")
                    print(summary)

        return summary, grouped_files

    def sort_files(self, file_list):
        filenames = {}

        for i, file in enumerate(file_list):

            output_file = Path(file).as_posix()

            #split into filepath and filename
            filepath = output_file.rsplit("/", 1)[0]
            filename = output_file.rsplit("/", 1)[1]

            #SICK FILES
            if "_nowood" in filename and ".DAT" in filename and "Processed" in filepath:
                filenames["nowood_sick .DAT"] = output_file

            if "_nowood" in filename and ".XML" in filename and "Processed" in filepath:
                filenames["nowood_sick .XML"] = output_file

            if "_wood" in filename and ".DAT" in filename and "Processed" in filepath:
                filenames["wood_sick .DAT"] = output_file

            if "_wood" in filename and ".XML" in filename and "Processed" in filepath:
                filenames["wood_sick .XML"] = output_file

            if "_remobilization" in filename and ".DAT" in filename and "Processed" in filepath:
                filenames["remobilization_sick .DAT"] = output_file

            if "_remobilization" in filename and ".XML" in filename and "Processed" in filepath:
                filenames["remobilization_sick .XML"] = output_file

            if "_pre" in filename and ".DAT" in filename and "Processed" in filepath:
                filenames["pre_sick .DAT"] = output_file

            if "_pre" in filename and ".XML" in filename and "Processed" in filepath:
                filenames["pre_sick .XML"] = output_file

            if "_post" in filename and ".DAT" in filename and "Processed" in filepath:
                filenames["post_sick .DAT"] = output_file

            if "_post" in filename and ".XML" in filename and "Processed" in filepath:
                filenames["post_sick .XML"] = output_file


            #MASSA SCANS
            if "_nowood(MAS)_Scan00" in filename and "nowood_massa_scan1" not in filenames:
                filenames["nowood_massa_scan1"] = output_file

            if "_nowood(MAS)_Scan00" in filename and "nowood_massa_scan1" in filenames:
                filenames["nowood_massa_scan2"] = output_file

            if "_wood(MAS)_Scan00" in filename and "wood_massa_scan1" not in filenames:
                filenames["wood_massa_scan1"] = output_file

            if "_wood(MAS)_Scan00" in filename and "wood_massa_scan1" in filenames:
                filenames["wood_massa_scan2"] = output_file

            if "_remobilization(MAS)_Scan00" in filename and "remobilization_massa_scan1" not in filenames:
                filenames["remobilization_massa_scan1"] = output_file

            if "_remobilization(MAS)_Scan00" in filename and "remobilization_massa_scan1" in filenames:
                filenames["remobilization_massa_scan2"] = output_file

            if "_autochthonous(MAS)_Scan00" in filename and "autoc_massa_scan1" not in filenames:
                filenames["autoc_massa_scan1"] = output_file

            if "_autochthonous(MAS)_Scan00" in filename and "autoc_massa_scan1" in filenames:
                filenames["autoc_massa_scan2"] = output_file


            #OUTPUTS
            if "_nowood" in filename and ".tif" in filename:
                filenames["nowood_sick .tif"] = output_file

            if "_wood.tif" in filename:
                filenames["wood_sick .tif"] = output_file

            if "_woodmap.tif" in filename:
                filenames["woodmap_sick .tif"] = output_file

            if "_remobilization.tif" in filename:
                filenames["remobilization_sick .tif"] = output_file
            
            if "_remobilizationmap.tif" in filename:
                filenames["remobilizationmap_sick .tif"] = output_file

            if "_pre.tif" in filename:
                filenames["pre_sick .tif"] = output_file

            if "_post.tif" in filename:
                filenames["post_sick .tif"] = output_file

            #OTHER FILES
            if "summary" in filename:
                filenames["summary"] = output_file

            if "_ocs" in filename:
                filenames["ocs"] = output_file

            if "_flowlog" in filename:
                filenames["flowlog"] = output_file

            if "_fieldnotes" in filename:
                filenames["counts"] = output_file

            if "_experiment_notes" in filename: 
                filenames["notes"] = output_file
            
            if "_densitydata" in filename:
                filenames["density"] = output_file

        return filenames

    def read_exp_summary(self, summary_fn):
         #read summary csv into pandas df
        summary_df = pd.read_excel(summary_fn)
        print(summary_df)

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

        return experiment_deets
    
    def check_exp_for_files(self, key, experiment_deets, filenames):
        if key in experiment_deets:
            experimental_setup = experiment_deets[f"{key}"]
            print(experimental_setup)

            #check files that all experiments should have
            if experimental_setup[0] != "x":
                if "ocs" not in filenames:
                    print("Missing ocean control file")

                if "density" not in filenames:
                    print("Missing density data file")

                if "flowlog" not in filenames:
                    print("Missing flow log data")

                if "notes" not in filenames:
                    print("Missing experiment notes file")

            #now based on the flood type lets check if the neccesary files are there
            if experimental_setup[0] == 'H':
                if "counts" not in filenames:
                    print("Missing field notes file")


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

            if experimental_setup[0] == 'L':
                if "counts" not in filenames:
                    print("Missing field notes file")

                    
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

            if experimental_setup[0] == 'A':
                if "pre_sick .DAT" not in filenames:
                    print("Missing pre_sick.dat")
                
                if "pre_sick .XML" not in filenames:
                    print("Missing pre_sick.xml")

                if "post_sick .DAT" not in filenames:
                    print("Missing post_sick.dat")
                
                if "post_sick .XML" not in filenames:
                    print("Missing post_sick.xml")

                
                if "autoc_massa_scan1" not in filenames:
                    print("Missing first autoc massa scan")

                if "autoc_massa_scan2" not in filenames:
                    print("Missing second autoc massa scan")

        else: 
            print("No experiment details in summary")