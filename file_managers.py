#file_managers.py
"""module containing methods for managing files"""

#import necessary packages
import os
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

    def parse_directory(self, directory):
        filenames = {}

        for subdir, _, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(subdir, file)

                if "_nowood" in filepath and ".DAT" in filepath:
                    filenames["nowood_sick .DAT"] = Path(filepath).as_posix()

                if "_nowood" in filepath and ".XML" in filepath:
                    filenames["nowood_sick .XML"] = Path(filepath).as_posix()

                if "_wood" in filepath and ".DAT" in filepath:
                    filenames["wood_sick .DAT"] = Path(filepath).as_posix()

                if "_wood" in filepath and ".XML" in filepath:
                    filenames["wood_sick .XML"] = Path(filepath).as_posix()

                if "_remobilization" in filepath and ".DAT" in filepath:
                    filenames["remobilization_sick .DAT"] = Path(filepath).as_posix()

                if "_remobilization" in filepath and ".XML" in filepath:
                    filenames["remobilization_sick .XML"] = Path(filepath).as_posix()

                if "_pre" in filepath and ".DAT" in filepath:
                    filenames["pre_sick .DAT"] = Path(filepath).as_posix()

                if "_pre" in filepath and ".XML" in filepath:
                    filenames["pre_sick .XML"] = Path(filepath).as_posix()

                if "_post" in filepath and ".DAT" in filepath:
                    filenames["post_sick .DAT"] = Path(filepath).as_posix()

                if "_post" in filepath and ".XML" in filepath:
                    filenames["post_sick .XML"] = Path(filepath).as_posix()

                if "_nowood(MAS)_Scan0001" in filepath:
                    filenames["nowood_massa_scan1"] = Path(filepath).as_posix()

                if "_nowood(MAS)_Scan0002" in filepath:
                    filenames["nowood_massa_scan2"] = Path(filepath).as_posix()

                if "_wood(MAS)_Scan0001" in filepath:
                    filenames["wood_massa_scan1"] = Path(filepath).as_posix()

                if "_wood(MAS)_Scan0002" in filepath:
                    filenames["wood_massa_scan2"] = Path(filepath).as_posix()

                if "_remobilization(MAS)_Scan0001" in filepath:
                    filenames["remobilization_massa_scan1"] = Path(filepath).as_posix()

                if "_remobilization(MAS)_Scan0002" in filepath:
                    filenames["remobilization_massa_scan2"] = Path(filepath).as_posix()

                if "_autochthonous(MAS)_Scan001" in filepath:
                    filenames["autoc_massa_scan1"] = Path(filepath).as_posix()

                if "_autochthonous(MAS)_Scan002" in filepath:
                    filenames["autoc_massa_scan2"] = Path(filepath).as_posix()

                if "_nowood" in filepath and ".tif" in filepath:
                    filenames["nowood_sick .tif"] = Path(filepath).as_posix()

                if "_wood.tif" in filepath:
                    filenames["wood_sick .tif"] = Path(filepath).as_posix()

                if "_woodmap.tif" in filepath:
                    filenames["woodmap_sick .tif"] = Path(filepath).as_posix()

                if "_remobilization.tif" in filepath:
                    filenames["remobilization_sick .tif"] = Path(filepath).as_posix()
                
                if "_remobilizationmap.tif" in filepath:
                    filenames["remobilizationmap_sick .tif"] = Path(filepath).as_posix()

                if "_pre.tif" in filepath:
                    filenames["pre_sick .tif"] = Path(filepath).as_posix()

                if "_post.tif" in filepath:
                    filenames["post_sick .tif"] = Path(filepath).as_posix()


        pprint(filenames)

        return filenames