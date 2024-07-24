#process_exp.py

"""script to process an entire experiments massa files"""

#load neccesary packages and modules
import numpy as np
from file_managers import FileManagers
from process_massa_data import ProcessMassaData
from process_sick_data import ProcessSICKData

#instantiate
fm = FileManagers()
pmd = ProcessMassaData()
psd = ProcessSICKData()

class ProcessExperiment:
    """method for processing experiment"""
    def __init__(self):
        print("initialized")

    def process_exp(self, exp_name, experiment_type, filenames, out_dir, flume_regions, epsg, offset, forest_den):


        #Now that we have established the experiment type, we have the files we need and we know what steps need to be taken
        if experiment_type is None:
            print("There is an issue with your files. Make sure you have the correct files in the directory you chose.")

        if experiment_type is "H":
            #process sick data
            psd.process_sick_data(filenames["nowood_sick .DAT"], filenames["wood_sick .DAT"], epsg, out_dir)

            outputs = fm.parse_directory(out_dir)

            sick_outputs = outputs[1]

            sick_files = fm.sort_files(sick_outputs[f"{exp_name}"])

            if forest_den == 0.5 or forest_den == 1 or forest_den == 2 or forest_den == 4:
                sick_files = fm.manage_missing_files(sick_files, forest_den, sick_outputs, "processed")

            #process massa data
            nowood_avg_fp_elev, nowood_median_fp_elev, nowood_avg_ch_elev, nowood_median_ch_elev = pmd.process_massa_data(filenames["nowood_massa_scan1"], sick_files["nowood_sick .tif"], flume_regions, epsg, out_dir, offset)
            wood_avg_fp_elev, wood_median_fp_elev, wood_avg_ch_elev, wood_median_ch_elev = pmd.process_massa_data(filenames["wood_massa_scan1"], sick_files["wood_sick .tif"], flume_regions, epsg, out_dir, offset)

            remobilization_avg_ch_elev = np.nan
            remobilization_avg_fp_elev = np.nan
            remobilization_median_ch_elev = np.nan
            remobilization_median_fp_elev = np.nan


        if experiment_type is "L":
            #process sick data
            psd.process_sick_data(filenames["nowood_sick .DAT"], filenames["wood_sick .DAT"], epsg, out = out_dir)
            psd.process_sick_data(filenames["wood_sick .DAT"], filenames["remobilization_sick .DAT"], epsg, out = out_dir, remobilization=True)

            outputs = fm.parse_directory(out_dir)

            sick_outputs = outputs[1]

            sick_files = fm.sort_files(sick_outputs[f"{exp_name}"])

            sick_files = fm.manage_missing_files(sick_files, forest_den, sick_outputs, "processed")

            #process massa data
            nowood_avg_fp_elev, nowood_median_fp_elev, nowood_avg_ch_elev, nowood_median_ch_elev = pmd.process_massa_data(filenames["nowood_massa_scan1"], sick_files["nowood_sick .tif"], flume_regions, epsg, out_dir, offset)

            remobilization_avg_fp_elev, remobilization_median_fp_elev, remobilization_avg_ch_elev, remobilization_median_ch_elev = pmd.process_massa_data(filenames["remobilization_massa_scan1"], sick_files["remobilization_sick .tif"], flume_regions, epsg, out_dir, offset)

            wood_avg_fp_elev, wood_median_fp_elev, wood_avg_ch_elev, wood_median_ch_elev = pmd.process_massa_data(filenames["wood_massa_scan1"], sick_files["wood_sick .tif"], flume_regions, epsg, out_dir, offset)

        if experiment_type is "A":
            #process sick data
            psd.process_sick_data(filenames["pre_sick .DAT"], filenames["post_sick .DAT"], epsg, out = out_dir)

            outputs = fm.parse_directory(out_dir)

            sick_outputs = outputs[1]

            sick_files = fm.sort_files(sick_outputs[f"{exp_name}"])

            sick_files = fm.manage_missing_files(sick_files, forest_den, sick_outputs, "processed")

            #process massa data
            autoc_avg_fp_elev, autoc_median_fp_elev, autoc_avg_ch_elev, autoch_median_ch_elev = pmd.process_massa_data(filenames["autoc_massa_scan1"], sick_files["post_sick .tif"], flume_regions, epsg, out_dir, offset)

        outs = [nowood_avg_fp_elev, nowood_median_fp_elev, nowood_avg_ch_elev, nowood_median_ch_elev, wood_avg_fp_elev, wood_median_fp_elev, wood_avg_ch_elev, wood_median_ch_elev, remobilization_avg_fp_elev, remobilization_median_fp_elev, remobilization_avg_ch_elev, remobilization_median_ch_elev]
    
        return outs