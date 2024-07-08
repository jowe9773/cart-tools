#process_massa_data.py
"""script that puts the massa tools together to create a function that actually processes the massa data"""

#import neccesary packages and modules
import os
import pandas as pd
import geopandas as gpd
from massa_tools import MassaTools


#instantiate classes
mt = MassaTools()

class ProcessMassaData:
    """class containing the function that will process 1 set of sick scans"""
    def __init__(self):
        print("Initialized!")

    def process_massa_data(self, massa_file, fp_geotiff, boundary_shp, epsg, out, offset):
        """script to process 1 massa dataset"""

        #find path to the massa filename
        path_to = os.path.dirname(massa_file)
        basename = os.path.basename(massa_file).split("(")[:-1][0]

        #load massa files with the same basename as the input massa file
        massa = gpd.GeoDataFrame()
        print(massa)
        for subdir, _, files in os.walk(path_to):
            for file in files:
                if basename in file:
                    data = mt.load_massa_file(subdir + "/" + file, epsg)
                    massa = pd.concat([massa, data])

        #find water depths
        water_depth = mt.get_water_depth(massa, fp_geotiff, offset)

        #extract points on the floodplain
        fp_data = mt.extract_aoi(water_depth, boundary_shp, polygon = 0)

        #extract points in the channel
        ch_data = mt.extract_aoi(water_depth, boundary_shp, polygon = 1)

        #make filenames for the channel and fp datasets
        out_name = massa_file.split("/")[-1].split("(")[0]

        fp_out = out + "/" + out_name + "_floodplain_points.shp"
        ch_out = out + "/" + out_name + "_channel_points.shp"

        #save data to shp files
        fp_data.to_file(fp_out)
        ch_data.to_file(ch_out)
