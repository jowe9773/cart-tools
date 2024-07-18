#file_managers.py
"""module containing methods for managing files"""

#import necessary packages
import os
import re
from collections import defaultdict
from pprint import pprint
from pathlib import Path
import tkinter as tk
from tkinter import filedialog



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

            if "_autohcthonous(MAS)_Scan00" in filename and "autoc_massa_scan1" in filenames:
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


        pprint(filenames)

        return filenames
