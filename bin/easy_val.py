### easy_val.py allows for conducting a single validation test easier, as it
### prompts the user for the inputs, rather than accept them as a in-line parameter.

# USAGE: python ./easy_val.py

# Imports
import sys
import os
import numpy as np
import configparser
import print_dir

# Read the current brightness from the config file
config = configparser.ConfigParser()
config.read('config.ini')
validation_data_path = config.get('paths', 'validation_data_path')
train_run_path = config.get('paths', 'train_run_path')
num_of_files = int(config.get('parameters', 'default_num_of_files'))

# Print most recent files in validation_data directory
print_dir.print_files_path(path=validation_data_path, num_of_files=num_of_files)

# Paths input
validation_path= validation_data_path + input("What is the name of the validation dataset you want to use? \n>") + "/data.yaml"
weight_path= train_run_path + input("Enter the path of the weight file being used (from /runs/train/, ex: [DATASET]/[FOLD#]/): \n>") + "weights/best.pt"

# Parameters input
img_size=int(input("Enter the inference image size: (ex: 3200): \n>"))
batch_size=int(input("Enter the batch-size to validate with (ex: 16): \n>"))
run_name=input("Enter the name of the run (ex: DRONE_MAIN_SET_20o30s_[Drone/Handheld]): \n>")

# Create the command for validation
cmd = "python ../val.py   --data {0} \
                          --weights {1} \
                          --name {2} \
                          --img {3} \
                          --batch-size {4} \
                          --save-txt \
                          --save-hybrid \
                          --save-conf \
                          ".format(validation_path, weight_path, run_name, img_size, batch_size)
# Show the command
print(cmd)
# Run the command
os.system(cmd)
