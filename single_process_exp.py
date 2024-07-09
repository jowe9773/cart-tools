#single_process_exp.py

"""This script calls the process_exp method to process a single experiment"""

#import neccesary packages and modules
from file_managers import FileManagers
from process_exp import ProcessExperiment

#instantiate:
fm = FileManagers()
pe = ProcessExperiment()

#load a directory containing all files of importance (this means SICK raw, sick processed, Massa raw)
directory = fm.load_dn("Select Directory containing Massa and SICK data")
out_dir = fm.load_dn("Select a directory to store outputs in.")
flume_regions = fm.load_fn("Select the flume regions shapefile")

#a couple of other things
epsg = 32615
offset = 208.2

pe.process_exp(directory, out_dir, flume_regions, epsg, offset)
