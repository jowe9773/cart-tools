#process_exp.py

"""script to process an entire experiments massa files"""

#load neccesary packages and modules
from file_managers import FileManagers
from process_massa_data import ProcessMassaData

#instantiate
fm = FileManagers()
pmd = ProcessMassaData()

#load a directory containing all files of importance (this means SICK raw, sick processed, Massa raw )
directory = fm.load_dn("Select Directory containing Massa and SICK data")

#parse through these files and make a dictionary of filenames for the relevant files
filenames = fm.parse_directory(directory)

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
                    "autochthonous_massa_scan1"
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
                    "autochthonous_massa_scan1"
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
                    "autochthonous_massa_scan1"
                    ]

if all(file not in filenames for file in required_absent) and all(file in filenames for file in required_present):
    experiment_type = "autochthonous"

print(experiment_type)

#Now that we have established the experiment type, we have the files we need and we know what steps need to be taken
if experiment_type is None:
    print("There is an issue with your files. Make sure you have the correct files in the directory you chose.")

if experiment_type is "high":
    #call method to process high experiment
    continue

if experiment_type is "low":
    #call method to process low experiment
    break

if experiment_type is "autochthonous":
    #call method do process autochthonous experiment
    break
