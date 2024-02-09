### Train.py makes the other train.py a bit easier to use.

### USAGE: python ./Train.py

import configparser
import os
from util.print_dir import print_files_path
from util.evaluate_datasets import evaluate_dataset

# Read from the config file
config = configparser.ConfigParser()
config.read('./util/config.ini')
yolov5_path = config.get('paths', 'yolov5_path')
training_data_path = config.get('paths', 'training_data_path')
num_of_files = int(config.get('parameters', 'default_num_of_files'))

# Variable for the hyperparameters being used
hyp_path=f"{yolov5_path}data/hyps/hyp.scratch-low.yaml"

# Print most recent files in training_data directory
print_files_path(path=training_data_path, num_of_files=num_of_files)

# Run the train.py script
dataset_name = input("What's the name of the dataset you're using? \n>")

if evaluate_dataset(path_to_dataset=f"{training_data_path}{dataset_name}/", type_of_dataset="training"):
    yaml_path=f"{training_data_path}{dataset_name}/data.yaml"
    batch_size=input("Enter the batch-size to train with (ex: 64): \n>")
    run_name=input("Enter the name of this training run: \n>")
    num_epochs=input("Enter the number of epochs to train with (ex: 300): \n")

    # Run the train.py with inputs as parameters
    os.system('nohup python {yolov5_path}train.py --data {yaml_path}  --batch-size={batch_size} --name {run_name} --epochs={num_epochs} --hyp {hyp_path} &')
    #os.system(f'python {yolov5_path}train.py --data {yaml_path}  --batch-size={batch_size} --name {run_name} --epochs={num_epochs} --hyp {hyp_path}')
