#testing_parsing.py

from file_managers import FileManagers
fm = FileManagers()

# Define the root directory
root_dir = fm.load_dn("Select a data directory")

summary, grouped_files = fm.parse_directory(root_dir)

#lets set up our experiment metadata (what type of experiment was run?)
if summary is not None:
    experiment_deets = fm.read_exp_summary(summary)

for key in grouped_files:
    print(" ")
    print(key)
    #pprint(grouped_files[key])
    filenames = fm.sort_files(grouped_files[key])

    fm.check_exp_for_files(key, experiment_deets, filenames)
