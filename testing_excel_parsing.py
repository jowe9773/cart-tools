#testing_excel_parsing.py

from file_managers import FileManagers
from pprint import pprint

fm = FileManagers()

excel_fn = fm.load_fn("Select an excel file to parse")

flood_type = "H"

counts = fm.extract_count_data(excel_fn, flood_type)

pprint(counts)

