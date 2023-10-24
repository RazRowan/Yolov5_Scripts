### Quick_val.py allows for multiple validation tests with a specified weight file
### and specified validation tests. The conf threshold and IOU threshold is incremented
### by a step set by the user and looped from the min to the max (see below variables)

# USAGE: python ./quick_val.py

# Imports
import sys
import os
import numpy as np

# Paths input
validation_path=input("Enter the path of the validation set being used (ex: ../data/validation_data/[DATASET]/data.yaml): \n>")
weight_path=input("Enter the path of the weight file being used (ex: ../runs/train/[DATASET]/[FOLD#]/weights/best.pt): \n>")

# Parameters input
img_size=int(input("Enter the inference image size: (ex: 3200): \n>"))
conf_step=float(input("Enter the confidence threshold step (ex: 0.05): \n>"))
IOU_step=float(input("Enter the IOU threshold step (ex: 0.05): \n>"))
conf_min=float(input("Enter the starting confidence threshold value: (ex: 0.0; this will really be 0.001, but the rest of the values will step from 0) \n>"))
IOU_min=float(input("Enter the starting IOU threshold value: (ex: 0.0) |n>"))
conf_max=float(input("Enter the ending confidence threshold value: (ex: 0.5) \n>")) #inclusive
IOU_max=float(input("Enter the ending IOU threshold value: (ex: 0.9) \n>")) #inclusive
batch_size=int(input("Enter the batch-size to validate with (ex: 16): \n>"))
run_name=input("Enter the name of the run (ex: DRONE_MAIN_SET_20o30s_[Drone/Handheld]): \n>")

# Create an array with the value 0.001
conf_array_1 = np.array([0.001])

# Create an array of values from conf_min to conf_max (inclusive) with a step of conf_step
conf_array_2 = np.arange(conf_min, conf_max + conf_step, conf_step)

# Remove the value 0 from the array
conf_array_2 = conf_array_2[conf_array_2 != 0]

# Concatenate the two arrays
conf_array_3 = np.concatenate((conf_array_1, conf_array_2))

# Create an array of values from IOU_min to IOU_max (inclusive) with a step of IOU_Step
IOU_array = np.arange(IOU_min, IOU_max + IOU_step, IOU_step)

# Loop through the range of confidence values (min-max by step)
for conf_threshold in conf_array_3:
   # Loop through the range of IOU values (min-max by step)
   for IOU_threshold in IOU_array:

      if conf_threshold != 0.001:
          conf_threshold =  round(conf_threshold, 2)
      IOU_threshold = round(IOU_threshold, 2)

      # Create run name for unique folders
      new_run_name = run_name + "/c" + str(conf_threshold) + "_i" + str(IOU_threshold)

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
                                        > test.txt".format(validation_path, weight_path, conf_threshold, IOU_threshold, new_run_name, img_size, batch_size)
      # Show the command
      print(cmd)
      # Run the command
      os.system(cmd)
