### Quick_val.py allows for multiple validation tests with a specified weight file
### and specified validation tests. The conf threshold and IOU threshold is incremented
### by a step set by the user and looped from the min to the max (see below variables)

# USAGE: python ./quick_val.py

# Imports
import sys
import os
import numpy as np

# Paths input
validation_path=input("Enter the path of the validation set being used (ex: ../data/validation_data/[DATASET]/data.yaml): ")
weight_path=input("Enter the path of the weight file being used (ex: ../runs/train/[DATASET]/[FOLD#]/weights/best.pt): ")

# Parameters input
img_size=int(input("Enter the inference image size: (ex: 3200): "))
conf_step=float(input("Enter the confidence threshold step (ex: 0.05): "))
IOU_step=float(input("Enter the IOU threshold step (ex: 0.05): "))
batch_size=int(input("Enter the batch-size to validate with (ex: 16): "))
run_name=input("Enter the name of the run (ex: DRONE_MAIN_SET_20o30s_[Drone/Handheld]): ")

# Mins/Maxs used in the for loop
conf_min=0.20
IOU_min=0.0
conf_max=0.5 #exclusive
IOU_max=0.2 #exclusive

# Loop through the range of confidence values (min-max by step)
for conf_threshold in np.arange(conf_min, conf_max, conf_step):
   # Loop through the range of IOU values (min-max by step)
   for IOU_threshold in np.arange(IOU_min, IOU_max, IOU_step):
      # Create run name for unique folders
      new_run_name = run_name + "/c" + str(round(conf_threshold, 2)) + "_i" + str(round(IOU_threshold, 2))

      #path_for_txt='../runs/val/'+run_name+'/c'+str(conf_threshold)+"_i"+str(IOU_threshold)+'/Metrics.txt'
      #sys.stdout = open(path_for_txt, 'w')

      # Create the command for validation
      cmd = "python ../val.py   --data {0} \
                                        --weights {1} \
                                        --conf-thres {2} \
                                        --iou-thres {3} \
                                        --name {4} \
                                        --img {5} \
					--batch-size {6} \
                                        > test.txt".format(validation_path, weight_path, round(conf_threshold, 2), round(IOU_threshold, 2), new_run_name, img_size, batch_size)
      # Show the command
      print(cmd)
      # Run the command
      os.system(cmd)
