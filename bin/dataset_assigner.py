### The dataset_assigner creates takes a dataset folder (train/valid/test) and
### using a random seed randomly assigns a percentage of photos to train/valid/test.

# USAGE: python ./dataset_assigner.py

import os
import shutil
import random
import string
import configparser
import print_dir
from random_seed import random_seed

# Read the current brightness from the config file
config = configparser.ConfigParser()
config.read('config.ini')
yolov5_path = config.get('paths', 'yolov5_path')
training_data_path = config.get('paths', 'training_data_path')
num_of_files = int(config.get('parameters', 'default_num_of_files'))

# Assign is the main method that will assign files to specific train/valid/test folders
def assign(path_to_project, dataset_folder, per_train, per_valid, per_test):
    # Helper method to move a specific number of files from a path to a new path
    def move_files(path, path_to_new_folder, num_to_move):
        # List the files at the path
        img_files = os.listdir(path + "/images/")

        # For as many as we're moving based on the percent of files we want to move
        #for i in range(num_to_move):
        for file in random.sample(list(img_files), num_to_move):
            # Grab random image file
            #file = random.choice(img_files)

            # Define paths for image files in order to move them
            src_img_file = os.path.join(path+ "/images/", file)
            dst_img_file = os.path.join(path_to_new_folder + "/images/", file)

            # Display
            print("This file: " + src_img_file + " is going to: " + dst_img_file)

            # Move the file
            shutil.move(src_img_file, dst_img_file)

            # Define paths for the corresponding text files in order to move them
            src_txt_file = os.path.join(path + "/labels/", file[:-3] + "txt")
            dst_txt_file = os.path.join(path_to_new_folder + "/labels/", file[:-3] + "txt")

            # Display
            print("This file: " + src_txt_file + " is going to: " + dst_txt_file)

            # Move the file
            shutil.move(src_txt_file, dst_txt_file)

    # Convert inputs to percentage as decimal
    per_train = int(per_train) / 100
    per_valid = int(per_valid) / 100
    per_test = int(per_test) / 100

    # Get total number of files before moving anything
    num_of_files = len(os.listdir(path_to_project + "/" + dataset_folder + "/images/"))

    # Get number of files wanted for each folder
    num_train = int(num_of_files * per_train)
    num_valid = int(num_of_files * per_valid)
    num_test = int(num_of_files * per_test)

    # If we want train files and we don't have a train folder
    if num_train > 0 and not os.path.exists(path_to_project + "/train/"):
        os.makedirs(os.path.dirname(path_to_project + "/train/images/"), exist_ok=False)
        os.makedirs(os.path.dirname(path_to_project + "/train/labels/"), exist_ok=False)

    # If we want valid files and we don't have a valid folder
    if num_valid > 0 and not os.path.exists(path_to_project + "/valid/"):
        os.makedirs(os.path.dirname(path_to_project + "/valid/images/"), exist_ok=False)
        os.makedirs(os.path.dirname(path_to_project + "/valid/labels/"), exist_ok=False)

    # If we want test files and we don't have a test folder
    if num_test > 0 and not os.path.exists(path_to_project + "/test/"):
        os.makedirs(os.path.dirname(path_to_project + "/test/images/"), exist_ok=False)
        os.makedirs(os.path.dirname(path_to_project + "/test/labels/"), exist_ok=False)

    # Get seed for random assignment
    seed = input("Please enter a seed for the random assignment (or -1 for new seed): ")
    if seed == "-1":
        if path_to_project[-1] == "/":
           dataset_name = os.path.basename(path_to_project[:-1])
        else:
           dataset_name = os.path.basename(path_to_project)
        seed = random_seed(dataset_name, 8)
    print("Using (" + str(seed) + ") as the random seed.")

    # Seed our random
    random.seed(seed)

    # Get the path to the dataset (./path/to/folder/[train/valid/test]/
    path_to_dataset = path_to_project + "/" + dataset_folder + "/"

    # If our dataset isn't already in train
    if dataset_folder != "train":
        path_to_new_folder = path_to_project + "/train/"
        move_files(path_to_dataset, path_to_new_folder, num_train)

    # If our dataset isn't already in valid
    if dataset_folder != "valid":
        path_to_new_folder = path_to_project + "/valid/"
        move_files(path_to_dataset, path_to_new_folder, num_valid)

    # If our dataset isn't already in test
    if dataset_folder != "test":
        path_to_new_folder = path_to_project + "/test/"
        move_files(path_to_dataset, path_to_new_folder, num_test)

    print("If you assigned some data to the train & valid folder, you COULD start training.")
    print("NOTE: If you have not used the FullBushDivider.py script, please do that before training!")

# Print most recent files in training_data directory
print_dir.print_files_path(path=training_data_path, num_of_files=num_of_files)

# Run the main program with these parameters
project_folder = training_data_path + input("What is the name of the dataset? \n>")
dataset_folder = input("What folder holds all the data? (Ex: train, valid, or test) \n>")
percent_train = int(input("What percentage of the data should the train folder have? \n>"))
percent_valid = int(input("What percentage of the data should the valid folder have? \n>"))
percent_test = int(input("What percentage of the data should the test folder have? \n>"))

assign(project_folder, dataset_folder, percent_train, percent_valid, percent_test)
