#process_exp.py

"""script to process an entire experiments massa files"""

#load neccesary packages and modules
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

    def process_exp(self, exp_name, filenames, out_dir, flume_regions, epsg, offset):


        #BASED ON WHICH FILES ARE AVAILABLE, SELECT A PROCESSING PATH
        experiment_type = None

        #for high flood 
        required_present = ["nowood_sick .DAT",
                            "wood_sick .DAT",
                            "nowood_massa_scan1",
                            "wood_massa_scan1"
                            ]
        required_absent = ["remobilization_sick .DAT",
                            "remobilization_massa_scan1",
                            "pre_sick .DAT", "post_sick .DAT",
                            "autoc_massa_scan1"
                            ]

        if all(file in filenames for file in required_present) and not any(file in filenames for file in required_absent):
            experiment_type = "high"

        #for low flood 
        required_present = ["nowood_sick .DAT",
                            "wood_sick .DAT",
                            "nowood_massa_scan1",
                            "wood_massa_scan1",
                            "remobilization_sick .DAT",
                            "remobilization_massa_scan1"
                            ]
        required_absent = ["pre_sick .DAT",
                            "post_sick .DAT",
                            "autoc_massa_scan1"
                            ]

        if all(file in filenames for file in required_present) and not any(file in filenames for file in required_absent):
            experiment_type = "low"

        #for autochthonous flood 
        required_absent = ["nowood_sick .DAT",
                            "wood_sick .DAT",
                            "nowood_massa_scan1",
                            "wood_massa_scan1",
                            "remobilization_sick .DAT",
                            "remobilization_massa_scan1"
                            ]
        required_present = ["pre_sick .DAT",
                            "post_sick .DAT",
                            "autoc_massa_scan1"
                            ]

        if all(file not in filenames for file in required_absent) and all(file in filenames for file in required_present):
            experiment_type = "autochthonous"

        print(experiment_type)

        #Now that we have established the experiment type, we have the files we need and we know what steps need to be taken
        if experiment_type is None:
            print("There is an issue with your files. Make sure you have the correct files in the directory you chose.")

        if experiment_type is "high":
            #process sick data
            psd.process_sick_data(filenames["nowood_sick .DAT"], filenames["wood_sick .DAT"], epsg, out_dir)

            outputs = fm.parse_directory(out_dir)

            sick_outputs = outputs[1]

            sick_files = fm.sort_files(sick_outputs[f"{exp_name}"])

            #process massa data
            pmd.process_massa_data(filenames["nowood_massa_scan1"], sick_files["nowood_sick .tif"], flume_regions, epsg, out_dir, offset)
            pmd.process_massa_data(filenames["wood_massa_scan1"], sick_files["wood_sick .tif"], flume_regions, epsg, out_dir, offset)

        if experiment_type is "low":
            #process sick data
            psd.process_sick_data(filenames["nowood_sick .DAT"], filenames["wood_sick .DAT"], epsg, out = out_dir)
            psd.process_sick_data(filenames["wood_sick .DAT"], filenames["remobilization_sick .DAT"], epsg, out = out_dir, remobilization=True)

            outputs = fm.parse_directory(out_dir)

            sick_outputs = outputs[1]

            sick_files = fm.sort_files(sick_outputs[f"{exp_name}"])

            #process massa data
            pmd.process_massa_data(filenames["nowood_massa_scan1"], sick_files["nowood_sick .tif"], flume_regions, epsg, out_dir, offset)

            pmd.process_massa_data(filenames["remobilization_massa_scan1"], sick_files["remobilization_sick .tif"], flume_regions, epsg, out_dir, offset)

            pmd.process_massa_data(filenames["wood_massa_scan1"], sick_files["wood_sick .tif"], flume_regions, epsg, out_dir, offset)

        if experiment_type is "autochthonous":
            #process sick data
            psd.process_sick_data(filenames["pre_sick .DAT"], filenames["post_sick .DAT"], epsg, out = out_dir)

            outputs = fm.parse_directory(out_dir)

            sick_outputs = outputs[1]

            sick_files = fm.sort_files(sick_outputs[f"{exp_name}"])

            #process massa data
            pmd.process_massa_data(filenames["autoc_massa_scan1"], sick_files["post_sick .tif"], flume_regions, epsg, out_dir, offset)

        
