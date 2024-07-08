#single_massa.py
"""script to process the massa data for one experiment"""

#import neccesary packages and modules
from process_massa_data import ProcessMassaData
from file_managers import FileManagers

#initialize classes
pmd = ProcessMassaData()
fm = FileManagers()

#select files and directories, set epsg
massa_file = fm.load_fn("Choose a massa file")
fp_geotiff = fm.load_fn("Choose corresponding floodplain geotiff")
boundary_shp = fm.load_fn("Choose the shapefile with floodplain and channel polygons")
epsg = 32615
out = fm.load_dn("Choose location for output files")

#for experiments on days from 20240626 to 20240703, otherwise just comment it out
offset = 208.2

#now lets process one set of scans
pmd.process_massa_data(massa_file, fp_geotiff, boundary_shp, epsg, out, offset)
