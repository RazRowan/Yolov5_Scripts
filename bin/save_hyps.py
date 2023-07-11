### save_hyps.py is a utility python script that is called in the training
### shell script to save the hyperparameters being used in training.

## Not intended to be called on its own, it will be called by a different
## script.

# USAGE: python  ./save_hyps.py [DATASET NAME] [DATASET SIZE] [EPOCHS] [HYP]

# Imports
import sys
import os
import json
from datetime import datetime

#ID/Version - Input
version = input("What is the version?\n")
#Explanation - Input
description = input("What is the description?\n")
#Yolov5 - Static
model_used = "Yolov5"
#A link? - ??? 

#Dataset used - Auto
dataset_used = sys.argv[2]
#Description of size of dataset - Auto
dataset_size = sys.argv[3]
#Date of when it was created - Auto
now = datetime.now()
creation_date = now.strftime("%m-%d-%Y %H:%M:%S")
#Any augments - Auto

#Testing accuracy? -???

#Epochs - Auto/Input
epochs = sys.argv[4]
#Hyperparameters - Auto
hyps = sys.argv[5:-1]

# Save to file
def save_to_file():
	with open(sys.argv[1] + 'settings.json', 'w', encoding='utf-8') as f:
		data = {
			'version' : version,
			'description' : description,
			'model_used' : model_used,
			'dataset_used' : dataset_used,
			'dataset_size' : dataset_size,
			'creation_date' : creation_date,
			'epochs' : epochs,
			'hyps' : hyps
		}
		json.dump(data, f, ensure_ascii=False, indent=4)

save_to_file()
