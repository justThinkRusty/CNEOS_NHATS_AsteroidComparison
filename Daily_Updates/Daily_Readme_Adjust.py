# Charlie Hanner - 11/10/2022
# This file can be run to automatically adjust the readme file to include the most recent chart generation, and delete any older chart generations

import os

# Get current requied paths
high_path_spec = os.path.dirname(os.path.realpath(__file__)) # path to: CNEOS_NHATS_AsteroidComparison/Daily_Updates
high_path_spec = high_path_spec[:len(high_path_spec)-13] # path to: CNEOS_NHATS_AsteroidComparison/
fullpath_spec = high_path_spec + "CNEOS_Pictures/" # path to: CNEOS_NHATS_AsteroidComparison/CNEOS_Pictures/

# Find all files that begin with "CNEOS_AstCompare_" and end with ".png"
file_list = [f for f in os.listdir(fullpath_spec) if f.startswith("CNEOS_AstCompare_") and f.endswith(".png")]

# Sort the list of files by the date of creation
file_list.sort(key=lambda x: os.path.getmtime(os.path.join(fullpath_spec, x)))

# Get the most recent file
most_recent_file = file_list[-1]

# Get the date of the most recent file
most_recent_date = most_recent_file[17:len(most_recent_file)-4]
# print(most_recent_date)

# Now open the readme file and adjust the most recent date
with open(high_path_spec + "README.md", "r") as f:
    lines = f.readlines()

# Find the line that contains the most recent date
for i in range(len(lines)):
    if lines[i].startswith("![Generated Image](CNEOS_Pictures/CNEOS_AstCompare_"):
        lines[i] = "![Generated Image](CNEOS_Pictures/CNEOS_AstCompare_" + most_recent_date + ".png) \n " 
        
# Now write the new lines to the README file
with open(high_path_spec + "README.md", "w") as f:
    f.writelines(lines)

# Now move all other "CNEOS_AstCompare_" files to the "Old_Charts" folder
for i in range(len(file_list)-1):
    # if filename contains "CNEOS_AstCompare_" and ends with ".png"
    if file_list[i].startswith("CNEOS_AstCompare_") and file_list[i].endswith(".png"):
        # move file to "Old_Charts" folder
        os.rename(fullpath_spec + file_list[i], fullpath_spec + "Old_Charts/" + file_list[i])

