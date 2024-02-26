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
scripts_path = config.get('paths', 'scripts_path')
num_of_files = int(config.get('parameters', 'default_num_of_files'))
update_repo_automatically = config.getboolean('parameters', 'update_repo_automatically')

# Pull down changes to repo
if update_repo_automatically:
    check_for_updates(scripts_path)

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
    num_epochs=input("Enter the number of epochs to train with (ex: 300): \n>")
    device_number=input("What GPU do you want to assign this task to? (0-7): \n>")
    weight_file=input("What size model are you training? (yolov5s.pt, yolov5m.pt, etc.): \n>")

    if os.path.exists("nohup.out"):
        os.remove("nohup.out")

    # Run the train.py with inputs as parameters
    #os.system('nohup python {yolov5_path}train.py --data {yaml_path}  --batch-size={batch_size} --name {run_name} --epochs={num_epochs} --hyp {hyp_path} &')
    os.system(f'python {yolov5_path}train.py --data {yaml_path}  --batch-size={batch_size} --name {run_name} --epochs={num_epochs} --device {device_number} --weights {yolov5_path}{weight_file} --hyp {hyp_path}')
