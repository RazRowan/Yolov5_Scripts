### easy_val.py allows for conducting a single validation test easier, as it
### prompts the user for the inputs, rather than accept them as a in-line parameter.

# USAGE: python ./easy_val.py

# Imports
import sys
import os
import numpy as np

# Paths input
validation_path=input("Enter the path of the validation set being used (ex: ../data/validation_data/[DATASET]/data.yaml): \n>")
weight_path=input("Enter the path of the weight file being used (ex: ../runs/train/[DATASET]/[FOLD#]/weights/best.pt): \n>")

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
