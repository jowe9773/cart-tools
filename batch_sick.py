#batch_sick.py
"""script to process sick data from multiple experiments"""

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

# Iterate through the first level directories
for first_level_dir in os.listdir(directory):
    first_level_path = os.path.join(directory, first_level_dir)
    if os.path.isdir(first_level_path):
        # Iterate through the second level directories
        for second_level_dir in os.listdir(first_level_path):
            second_level_path = os.path.join(first_level_path, second_level_dir)
            if os.path.isdir(second_level_path):
                print(second_level_path)
                # Iterate through the files in the second level directories
                for subdir, _, files in os.walk(second_level_path):
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

                        if "remobilization" in filepath and ".DAT" in filepath:
                            REMOBILIZATION = Path(filepath).as_posix()
                            print("Remobilization was created!")

                    if BEFORE is None or AFTER is None:
                        print("missing before or after data, check files for " + second_level_dir)
                        continue

                    outdir = out + "/" + first_level_dir
                    os.makedirs(outdir, exist_ok=True)

                    #check to see if these files have already been processed
                    out_names = BEFORE.split("/")[-1].split("_")[:3]
                    before_fn_out = outdir + "/" + out_names[0] + "_" + out_names[1] + "_" + out_names[2] + '.tif'
                    out_names = BEFORE.split("/")[-1].split("_")[:3]
                    after_fn_out = outdir + "/" + out_names[0] + "_" + out_names[1] + "_" + out_names[2] + '.tif'
                    out_names = BEFORE.split("/")[-1].split("_")[:3]

                    wood_fn_out = outdir + "/" + out_names[0] + "_" + out_names[1] + "_woodmap.tif"
                    remobilization_fn_out = outdir + "/" + out_names[0] + "_" + out_names[1] + "remobilization.tif"

                    if os.path.exists(before_fn_out) and os.path.exists(after_fn_out) and os.path.exists(wood_fn_out) and os.path.exists(remobilization_fn_out):
                        print(second_level_dir + " has already been processed. Skipping ahead to the next experiment.")
                        continue

                    #Now that we have the before and after files, we can create pre, post, and wood map DEMs
                    psd.process_sick_data(BEFORE, AFTER, ESPG, outdir)

                    if REMOBILIZATION is not None:
                        psd.process_sick_data(AFTER, REMOBILIZATION, ESPG, outdir, remobilization = True)
