#group_data.py

"""This file contains code that will batch process massa and sick data, then pull 
data from each experiment and make an excel file that holds all of the data """

#import neccesary packages and modules
from file_managers import FileManagers
from process_exp import ProcessExperiment
import numpy as np
import pandas as pd
from pprint import pprint

#instantiate:
fm = FileManagers()
pe = ProcessExperiment()
summary = None

#lets instantiate the dataframe that will be exported at the very end
output_df = pd.DataFrame(columns = ["experiment_name", "s_dropped", "i_dropped", "l_dropped", "all_dropped",
                "s_fp_injam", "i_fp_injam", "l_fp_injam", "all_fp_injam",
                "s_cm_injam", "i_cm_injam", "l_cm_injam", "all_cm_injam",
                "s_ic_injam", "i_ic_injam", "l_ic_injam", "all_ic_injam",
                "s_tot_injam", "i_tot_injam", "l_tot_injam", "all_injam",
                "s_fp_ind", "i_fp_ind", "l_fp_ind", "all_fp_ind",
                "s_cm_ind", "i_cm_ind", "l_cm_ind", "all_cm_ind",
                "s_ic_ind", "i_ic_ind", "l_ic_ind", "all_ic_ind",
                "s_tot_ind", "i_tot_ind", "l_tot_ind", "all_ind",
                "all_s", "all_i", "all_l", "all_pieces",
                "all_fp", "all_cm", "all_ic",
                "remobilized_s", "remobilized_i", "remobilized_l", "remobilized_total",
                "nowood_avg_fp_elev", "nowood_median_fp_elev", "nowood_avg_ch_elev", "nowood_median_ch_elev", 
                "wood_avg_fp_elev", "wood_median_fp_elev", "wood_avg_ch_elev", "wood_median_ch_elev", 
                "remobilization_avg_fp_elev", "remobilization_median_fp_elev", "remobilization_avg_ch_elev", "remobilization_median_ch_elev"
            ])



#some user inputs
root_dir = fm.load_dn("Select a data directory")
out_dir = fm.load_dn("Select a directory to keep outputs in")
flume_regions = fm.load_fn("Choose the flume regions shapefile")
epsg = 32615
offset = 0 #the default massa offset is 0mm

# load files into groups 
summary, grouped_files = fm.parse_directory(root_dir)

#lets set up our experiment metadata (what type of experiment was run?)
if summary is not None:
    experiment_deets = fm.read_exp_summary(summary)

#now lets go through each experiment (each key represents one experiment)
for key in grouped_files:
    print(" ")
    print(key)

    #if experiment is within a certain range of dates change the offset accordingly
    if "20240626" in key or "20240627" in key or "20240628" in key or "20240629" in key or "20240630" in key or "20240701" in key or "20240702" in key or "20240703" in key:
        offset =  208.2


    #pprint(grouped_files[key])
    filenames = fm.sort_files(grouped_files[key])

    #list the flood type for the experiment
    flood_type = experiment_deets[key][0]

    print(flood_type)

    if flood_type == "H" or flood_type == "L":

        #process sick and massa data
        outs = pe.process_exp(key, filenames, out_dir, flume_regions, epsg, offset)
        
        #get the count data 
        counts = fm.extract_count_data(filenames["counts"], flood_type)

        #add water depth data
        data = outs + counts

        data.insert(0, key)
        
        #append the count data to the output_df
        new_row = pd.DataFrame([data], columns= ["experiment_name", "s_dropped", "i_dropped", "l_dropped", "all_dropped",
                "s_fp_injam", "i_fp_injam", "l_fp_injam", "all_fp_injam",
                "s_cm_injam", "i_cm_injam", "l_cm_injam", "all_cm_injam",
                "s_ic_injam", "i_ic_injam", "l_ic_injam", "all_ic_injam",
                "s_tot_injam", "i_tot_injam", "l_tot_injam", "all_injam",
                "s_fp_ind", "i_fp_ind", "l_fp_ind", "all_fp_ind",
                "s_cm_ind", "i_cm_ind", "l_cm_ind", "all_cm_ind",
                "s_ic_ind", "i_ic_ind", "l_ic_ind", "all_ic_ind",
                "s_tot_ind", "i_tot_ind", "l_tot_ind", "all_ind",
                "all_s", "all_i", "all_l", "all_pieces",
                "all_fp", "all_cm", "all_ic",
                "remobilized_s", "remobilized_i", "remobilized_l", "remobilized_total",
                "nowood_avg_fp_elev", "nowood_median_fp_elev", "nowood_avg_ch_elev", "nowood_median_ch_elev", 
                "wood_avg_fp_elev", "wood_median_fp_elev", "wood_avg_ch_elev", "wood_median_ch_elev", 
                "remobilization_avg_fp_elev", "remobilization_median_fp_elev", "remobilization_avg_ch_elev", "remobilization_median_ch_elev"
                ])
        output_df = pd.concat([output_df, new_row], ignore_index=True)


pprint(output_df)

output_df.to_csv(out_dir + "/output_dataframe.csv")
