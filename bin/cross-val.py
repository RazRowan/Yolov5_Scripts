### Cross-val.py runs the val.py script for all of a given set of 
### fold weights.

# USAGE: python ./cross-val.py

# Imports
import sys
import os

# Parameters
NUM_FOLD = 5

set_name=input("What is the name of the MASTER_SET being cross-validated?\n")

MODEL_WEIGHTS = [
	"../runs/train/" + set_name + "/Fold1/weights/best.pt",
	"../runs/train/" + set_name + "/Fold2/weights/best.pt",
	"../runs/train/" + set_name + "/Fold3/weights/best.pt",
	"../runs/train/" + set_name + "/Fold4/weights/best.pt",
	"../runs/train/" + set_name + "/Fold5/weights/best.pt",
]

DATA = [
	"../data/training_data/" + set_name + "/Fold1/data.yaml",
	"../data/training_data/" + set_name + "/Fold2/data.yaml",
	"../data/training_data/" + set_name + "/Fold3/data.yaml",
	"../data/training_data/" + set_name + "/Fold4/data.yaml",
	"../data/training_data/" + set_name + "/Fold5/data.yaml"
]

# Fix to automatically take these parameters
CONFIDENCE =[
	open("../runs/train/" + set_name + "/Fold1/F1_value.txt").read(),
	open("../runs/train/" + set_name + "/Fold2/F1_value.txt").read(),
	open("../runs/train/" + set_name + "/Fold3/F1_value.txt").read(),
	open("../runs/train/" + set_name + "/Fold4/F1_value.txt").read(),
	open("../runs/train/" + set_name + "/Fold5/F1_value.txt").read()
]

for fold in range(NUM_FOLD):
	print('FOLD NUMBER: ', fold + 1)
	save_dir = set_name + "/Fold" + str(fold + 1)
	cmd = "nohup python ../val.py 	--data {0} \
					--weights {1} \
					--conf-thres {2} \
					--iou-thres 0.5 \
					--name {3} \
					--save-txt \
					--save-hybrid \
					--save-conf \
					&".format(DATA[fold], MODEL_WEIGHTS[fold], CONFIDENCE[fold], save_dir)
	print(cmd)
	os.system(cmd)
	print('################################################################\n')
