### Fold.py creates folds for the directory passed in. This is the first step
### for Cross Validation.

# USAGE: python ./fold.py

# Imports
import sys
import os
import numpy as np
from sklearn.model_selection import KFold

# Saves either images or labels from the original directory to the new fold directory    
def saveFiles(fold_set, original_path, new_path):
    for index in fold_set:
        os.system("cp " + original_path + "/train/images/" + image_array[index] + " " + new_path + "/images/")
        os.system("cp " + original_path + "/train/labels/" + label_array[index] + " " + new_path + "/labels/")

# Creates a data.yaml file (needed for train.py)
def saveYaml(path):
    f = open(path + "/data.yaml", 'w')
    sys.stdout = f
    path = path[1:]
    print("train: " + path + "/train/images")
    print("val: " + path + "/valid/images")
    print("test: " + path + "/test/images")
    print()
    print("nc: 2")
    print("names: ['blue', 'green']")
    f.close()
    sys.stdout = sys.__stdout__

# Take input
directory_name=input("What is the path of the Parent directory to split? (ex: ../data/training_data/[DATASET]/ \n>")
num_folds=input("How many folds should be created? (ex: 5) \n>")

# Creating variables to access the images/labels of original dir
image_dir = directory_name + "train/images/"
label_dir = directory_name + "train/labels/"

# Sort the files listen in these dirs
image_array = sorted(os.listdir(image_dir))
label_array = sorted(os.listdir(label_dir))

### Use KFold and kf.split to split the image_array into indices.
# The folding works by splitting the array into n lists of indices
# that are evenly split. See sklearn KFold documentation for more.
kf = KFold(n_splits = int(num_folds))
indices = kf.split(image_array)

# For loop to create the folds for each n of splits (see kf above)
for fold, (train, valid) in enumerate(indices):

    print("Creating Fold " + str(fold + 1) + "...")

    # Create directories for each Fold
    fold_path_name = directory_name + "Fold" + str(fold + 1)
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
    saveFiles(train, directory_name, train_path_name)
    saveFiles(valid, directory_name, valid_path_name)
    saveYaml(fold_path_name)

    print("Done!")

print("All folds created and stored at: " + directory_name)


