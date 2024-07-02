#single_sick.py

#import neccesary modules and packages
import os
from pathlib import Path
from sick_tools import SickTools
from file_managers import FileManagers
from process_sick_data import ProcessSICKData

#instantiate classes
fm = FileManagers()
st = SickTools()
psd = ProcessSICKData()

#load directory containing data for each experiment organized into individual directories
directory = fm.load_dn("Choose folder containing data organized by experiment")

#select directory to store outputs in
out = fm.load_dn("select directory to store outputs in")

#choose a coordinate system to store data in
ESPG = 32615

for subdir, _, files in os.walk(directory):
    BEFORE = None
    AFTER = None
    REMOBILIZATION = None
    for file in files:
        filepath = os.path.join(subdir, file)

        # if a particular filepath is the one we are looking for, then we will make it the before or after file
        if ("_nowood" in filepath or "_pre" in filepath) and ".DAT" in filepath:
            BEFORE = Path(filepath).as_posix()
            print("Before was created!")

        if ("_wood" in filepath or "_post" in filepath) and ".DAT" in filepath:
            AFTER = Path(filepath).as_posix()
            print("After was created!")

        if "_remobilization" in filepath and ".DAT" in filepath:
            REMOBILIZATION =  Path(filepath).as_posix()
            print("Remobilization was created!")

    if BEFORE is None or AFTER is None:
        print("missing before or after data, check files for " + directory)
        continue

    os.makedirs(out, exist_ok=True)


    #Now that we have the before and after files, we can create pre, post, and wood map DEMs
    psd.process_sick_data(BEFORE, AFTER, ESPG, out)

    if REMOBILIZATION is not None:
        psd.process_sick_data(AFTER, REMOBILIZATION, ESPG, out, remobilization = True)    