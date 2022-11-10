# Charlie Hanner - 11/10/2022
# This file can be run to automatically adjust the readme file to include the most recent chart generation, and delete any older chart generations

# First scan the CNEOS_Pictures directory to find the most recent chart generation

import os

# Get current library path
high_path_spec = os.path.dirname(os.path.realpath(__file__)) + "/"
fullpath_spec = high_path_spec + "CNEOS_Pictures/"

# Find all files that begin with "CNEOS_AstCompare_" and end with ".png"
file_list = [f for f in os.listdir(fullpath_spec) if f.startswith("CNEOS_AstCompare_") and f.endswith(".png")]

# Sort the list of files by the date of creation
file_list.sort(key=lambda x: os.path.getmtime(os.path.join(fullpath_spec, x)))

# Get the most recent file
most_recent_file = file_list[-1]

# Get the date of the most recent file
most_recent_date = most_recent_file[17:25]

# Now open the readme file and adjust the most recent date
with open(high_path_spec + "Readme.md", "r") as f:
    lines = f.readlines()

# Find the line that contains the most recent date
for i in range(len(lines)):
    if lines[i].startswith("![Generated Image](CNEOS_Pictures/CNEOS_AstCompare_"):
        lines[i] = "![Generated Image](CNEOS_Pictures/CNEOS_AstCompare_" + most_recent_date + ".png"

# Now write the new lines to the readme file
with open(high_path_spec + "Readme.md", "w") as f:
    f.writelines(lines)

# Now delete all files that are older than the most recent file
for i in range(len(file_list) - 1):
    os.remove(fullpath_spec + file_list[i])




