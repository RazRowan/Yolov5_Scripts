### Fold.py creates folds for the directory passed in. This is the first step
### for Cross Validation.

# USAGE: python ./fold.py

# Imports
import sys
import os
import random
import string
import numpy as np
from sklearn.model_selection import KFold
import configparser
import print_dir
from random_seed import random_seed

# Read the current brightness from the config file
config = configparser.ConfigParser()
config.read('config.ini')
yolov5_path = config.get('paths', 'yolov5_path')
scripts_path = config.get('paths', 'scripts_path')
training_data_path = config.get('paths', 'training_data_path')
num_of_files = int(config.get('parameters', 'default_num_of_files'))

# Saves either images or labels from the original directory to the new fold directory    
def saveFiles(fold_set, original_path, new_path):
    for index in fold_set:
        os.system("cp " + original_path + "/train/images/" + image_array[index] + " " + new_path + "/images/")
        os.system("cp " + original_path + "/train/labels/" + label_array[index] + " " + new_path + "/labels/")

# Creates a data.yaml file (needed for train.py)
def saveYaml(path):
    f = open(path + "/data.yaml", 'w')
    sys.stdout = f
    if path[1] == ".":
        path = path[1:]
    print("train: " + path + "/train/images")
    print("val: " + path + "/valid/images")
    print("test: " + path + "/test/images")
    print()
    print("nc: 2")
    print("names: ['blue', 'green']")
    f.close()
    sys.stdout = sys.__stdout__

# Print most recent files in training_data directory
print_dir.print_files_path(path=training_data_path, num_of_files=num_of_files)

# Take input
directory_name=input("What is the name of the dataset to split? \n>")
dataset_path=f"{training_data_path}{directory_name}/"
num_folds=input("How many folds should be created? (ex: 5) \n>")

# Get seed for random assignment
seed = int(input("Please enter a seed for the random assignment (or -1 for new seed): "))
if seed == -1:
    seed = int(random_seed(directory_name, 8))
print("Using (" + str(seed) + ") as the random seed.")

# Creating variables to access the images/labels of original dir
image_dir = dataset_path + "train/images/"
label_dir = dataset_path + "train/labels/"

# Sort the files listen in these dirs
image_array = sorted(os.listdir(image_dir))
label_array = sorted(os.listdir(label_dir))

### Use KFold and kf.split to split the image_array into indices.
# The folding works by splitting the array into n lists of indices
# that are evenly split. See sklearn KFold documentation for more.
kf = KFold(n_splits=int(num_folds), shuffle=True, random_state=seed)
indices = kf.split(image_array)

# For loop to create the folds for each n of splits (see kf above)
for fold, (train, valid) in enumerate(indices):

    print("Creating Fold " + str(fold + 1) + "...")

    # Create directories for each Fold
    fold_path_name = dataset_path + "Fold" + str(fold + 1)
    os.system("mkdir -p " + fold_path_name)

    # Create directories for train and test
    train_path_name = fold_path_name + "/train/"
    os.system("mkdir -p " + train_path_name)
    os.system("mkdir -p " + train_path_name + "images/")
    os.system("mkdir -p " + train_path_name + "labels/")

    valid_path_name = fold_path_name + "/valid/"
    os.system("mkdir -p " + valid_path_name)
    os.system("mkdir -p " + valid_path_name + "images/")
    os.system("mkdir -p " + valid_path_name + "labels/")

    # Save Files in their respective dirs and create a data.yaml
    saveFiles(train, dataset_path, train_path_name)
    saveFiles(valid, dataset_path, valid_path_name)
    saveYaml(fold_path_name)

    print("Done!")

print(f"All folds created and stored at: {dataset_path}")
print("You should be ready to run the fold_train.py script!")

