#file_managers.py
"""module containing methods for managing files"""

#import necessary packages
import os
import re
import numpy as np
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import pandas as pd


class FileManagers:
    """Class contains methods for managing files"""

    def __init__(self):
        print("Initialized file managers")

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

    def extract_count_data(self, count_fn, flood_type):

        summary_df = pd.read_excel(count_fn, sheet_name = "Summary")

        #dropped counts
        s_dropped = summary_df.iat[1,2]
        i_dropped = summary_df.iat[1,3]
        l_dropped = summary_df.iat[1,4]
        all_dropped = summary_df.iat[1,5]

        #floodplain in jam counts
        s_fp_injam = summary_df.iat[3,2]
        i_fp_injam = summary_df.iat[3,3]
        l_fp_injam = summary_df.iat[3,4]
        all_fp_injam = summary_df.iat[3,5]

        #channel margin in jam counts
        s_cm_injam = summary_df.iat[4,2]
        i_cm_injam = summary_df.iat[4,3]
        l_cm_injam = summary_df.iat[4,4]
        all_cm_injam = summary_df.iat[4,5]

        #in channel in jam counts
        s_ic_injam = summary_df.iat[5,2]
        i_ic_injam = summary_df.iat[5,3]
        l_ic_injam = summary_df.iat[5,4]
        all_ic_injam = summary_df.iat[5,5]

        # total counts in jams by piece size
        s_tot_injam = summary_df.iat[6,2]
        i_tot_injam = summary_df.iat[6,3]
        l_tot_injam = summary_df.iat[6,4]
        all_injam = summary_df.iat[6,5]

        #floodplain individual piece counts
        s_fp_ind = summary_df.iat[8,2]
        i_fp_ind = summary_df.iat[8,3]
        l_fp_ind = summary_df.iat[8,4]
        all_fp_ind = summary_df.iat[8,5]

        #channel marginal individual piece counts
        s_cm_ind = summary_df.iat[9,2]
        i_cm_ind = summary_df.iat[9,3]
        l_cm_ind = summary_df.iat[9,4]
        all_cm_ind = summary_df.iat[9,5]

        #in channel individual piece counts
        s_ic_ind = summary_df.iat[10,2]
        i_ic_ind = summary_df.iat[10,3]
        l_ic_ind = summary_df.iat[10,4]
        all_ic_ind = summary_df.iat[10,5]

        #total counts of individual pieces by size
        s_tot_ind = summary_df.iat[11,2]
        i_tot_ind = summary_df.iat[11,3]
        l_tot_ind = summary_df.iat[11,4]
        all_ind = summary_df.iat[11,5]

        #total number of pieces by location
        all_fp = all_fp_ind + all_fp_injam
        all_cm = all_cm_ind + all_cm_injam
        all_ic = all_ic_ind + all_ic_injam

        #total number of pieces in the flume at the end of the flood
        if flood_type == "H":
            #total number of pieces by size
            all_s = s_tot_ind + s_tot_injam
            all_i = i_tot_ind + i_tot_injam
            all_l = l_tot_ind + l_tot_injam

            all_pieces = all_s + all_i + all_l

            remobilized_s = np.nan
            remobilized_i = np.nan
            remobilized_l = np.nan
            remobilized_total = np.nan

        if flood_type == "L":
            remobilized_s = summary_df.iat[16,2]
            remobilized_i = summary_df.iat[16,3]
            remobilized_l = summary_df.iat[16,4]
            remobilized_total = summary_df.iat[16,5]

            #total number of pieces by size
            all_s = s_tot_ind + s_tot_injam + remobilized_s
            all_i = i_tot_ind + i_tot_injam + remobilized_i
            all_l = l_tot_ind + l_tot_injam + remobilized_l

            all_pieces = all_s + all_i + all_l

        count_list = [
            s_dropped, i_dropped, l_dropped, all_dropped,
            s_fp_injam, i_fp_injam, l_fp_injam, all_fp_injam,
            s_cm_injam, i_cm_injam, l_cm_injam, all_cm_injam,
            s_ic_injam, i_ic_injam, l_ic_injam, all_ic_injam,
            s_tot_injam, i_tot_injam, l_tot_injam, all_injam,
            s_fp_ind, i_fp_ind, l_fp_ind, all_fp_ind,
            s_cm_ind, i_cm_ind, l_cm_ind, all_cm_ind,
            s_ic_ind, i_ic_ind, l_ic_ind, all_ic_ind,
            s_tot_ind, i_tot_ind, l_tot_ind, all_ind,
            all_s, all_i, all_l, all_pieces,
            all_fp, all_cm, all_ic,
            remobilized_s, remobilized_i, remobilized_l, remobilized_total
            ]

        return count_list
    
    def manage_missing_files(self, filenames, forest_den, grouped_files, time):
        
        if forest_den == 0.5:
            exp_to_parse = grouped_files["20240603_exp1"]

        if forest_den == 1:
            exp_to_parse = grouped_files["20240529_exp2"]

        if forest_den == 2:
            exp_to_parse = grouped_files["20240605_exp1"]

        if forest_den == 4:
            exp_to_parse = grouped_files["20240606_exp1"]

        fm = FileManagers()

        replacement_files = fm.sort_files(exp_to_parse)

        if time == "raw":
            if "nowood_sick .DAT" not in filenames:
                filenames["nowood_sick .DAT"] = replacement_files["nowood_sick .DAT"]

            if "nowood_sick .XML" not in filenames:
                filenames["nowood_sick .XML"] = replacement_files["nowood_sick .XML"]

            if "nowood_massa_scan1" not in filenames:
                filenames["nowood_massa_scan1"] = replacement_files["nowood_massa_scan1"]

            if "nowood_massa_scan2" not in filenames:
                filenames["nowood_massa_scan2"] = replacement_files["nowood_massa_scan2"]

        if time == "processed":
            if "nowood_sick .tif" not in filenames:
                filenames["nowood_sick .tif"] = replacement_files["nowood_sick .tif"]

        return filenames