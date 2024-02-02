### Train.py makes the other train.py a bit easier to use.

### USAGE: python ./Train.py

import configparser
import os

# Read the current brightness from the config file
config = configparser.ConfigParser()
config.read('config.ini')
yolov5_path = config.get('paths', 'yolov5_path')

# Variable for the hyperparameters being used
hyp_path=f"{yolov5_path}data/hyps/hyp.scratch-low.yaml"

# Run the train.py script
yaml_path=input("Enter the path of the data.yaml (relative path (ex: ../path/to/dataset/folder/data.yaml) or full path): \n>")
batch_size=input("Enter the batch-size to train with (ex: 64): \n>")
run_name=input("Enter the name of this training run: \n>")
num_epochs=input("Enter the number of epochs to train with (ex: 300): \n")

# Run the train.py with inputs as parameters
os.system('nohup python {yolov5_path}train.py --data {yaml_path}  --batch-size={batch_size} --name {run_name} --epochs={num_epochs} --hyp {hyp_path} &')

# Go to the data.yaml and get the train/test path
#train_path=$(cat $yaml_path | head -n1 | sed -n 's/train: //p')
#train_path=$(echo '.'"$train_path")
#test_path=$(cat $yaml_path | head -n2 | sed -n 's/val: //p')
#test_path=$(echo '.'"$test_path")
