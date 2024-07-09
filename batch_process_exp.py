#batch_process_exp.py
"""this script repeats the process_exp.py method over multiple experiments"""

#import neccesary packages and modules
import os
from pathlib import Path
from file_managers import FileManagers
from process_exp import ProcessExperiment


#instantiate:
fm = FileManagers()
pe = ProcessExperiment()

#some neccesary inputs that will be consistent across experiments
flume_regions = fm.load_fn("Select the flume regions shapefile")
epsg = 32615
offset = 208.2

#parse directory for subdirectories
main_directory = fm.load_dn("Select a batch directory")

subdirs = []

for item in os.listdir(main_directory):
    item_path = Path(os.path.join(main_directory, item)).as_posix()
    if os.path.isdir(item_path):
        subdirs.append(item_path)

#iterate through subdirectories (each of which is for one experiment)
for i in range(len(subdirs)):
    out_dir = subdirs[i] + "/outputs"
    os.makedirs(out_dir, exist_ok=True)

    pe.process_exp(subdirs[i], out_dir,flume_regions, epsg, offset)

    
