### fold_train.py allows you to train all folds for a MAIN dataset that was folded.
### This is the final step for cross-validation. BE CAREFUL with trainings not
### finishing, as training many models at the same time is extremely performance
### intensive. Monitor your training runs closely.

### USAGE: python ./fold_train.py

import configparser
import os

# Read the current brightness from the config file
config = configparser.ConfigParser()
config.read('config.ini')
yolov5_path = config.get('paths', 'yolov5_path')
training_data_path = config.get('paths', 'training_data_path')

# Variable for the hyperparameters being used
hyp_path=f"{yolov5_path}data/hyps/hyp.scratch-low.yaml"

# Vars needed to train the folds
num_folds=input("How many folds are there to train? (usually between 5-10): \n>")
main_set_name=input("Enter the name of the Main Set (ex: [Blueberry_berry_merged_80]): \n>")
batch_size=input("Enter the batch-size to train with (ex: 16): \n>")
num_epochs=input("Enter the number of epochs to train with (ex: 300): \n>")

# Additional var for naming Fold dirs
main_set_path=f"{training_data_path}{main_set_name}/"

for i in range(int(num_folds)):
    run_name=f"{main_set_name}/Fold{i}"
    fold_path=f"{main_set_path}/Fold{i}/"
    yaml_path=f"{fold_path}data.yaml"

    os.system(f"nohup python {yolov5_path}train.py --data {yaml_path} --batch-size={batch_size} --name {run_name} --epochs={num_epochs} --hyp {hyp_path} --save-period 50  &")

    # Go to the data.yaml and get the train/test path
    #train_path=$(cat $yaml_path | head -n1 | sed -n 's/train: //p')
    #train_path=$(echo '.'"$train_path")
    #test_path=$(cat $yaml_path | head -n2 | sed -n 's/val: //p')
    #test_path=$(echo '.'"$test_path")

    print(f"\nFold{i} training started...\n")
