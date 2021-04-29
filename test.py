import configparser
import subprocess
import os

# Read Configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Gather info on the object
args = str(config['locations']['sub_auto_tool'])
args += str("sbsbaker.exe info --hide-location --hide-bounding-box ") # File
args += '"' + str("D:/3D/Test/cs1483/cs1483.fbx") + '"' # Mesh files to process. This option is implicit, so you can just provide a list of files at the end of your arguments, they will be interpreted as inputs.

temp = subprocess.Popen(args, stdout = subprocess.PIPE)

# we use the communicate function
# to fetch the output
output = str(temp.communicate())

# splitting the output so that
# we can parse them line by line
output = output.split("\\r\\n")

# a variable to store the output
res = []

# iterate through the output
# line by line
for line in output:
    if line.find('Entity') != -1:
        clean_line = line.replace('  Entity "', '').replace('":', '')
        res.append(clean_line)

print(res)
