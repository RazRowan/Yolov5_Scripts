### metrics_to_csv.py converts an outputted metric txt file to csv.
### This was made specifically to convert files generated from validation
### metrics. These files are created from the logging data produced in the
### val.py yolov5 script.

### VERSION: 7/5/2023, Brandon McHenry

# USAGE: python ./metrics_to_csv.py

# Imports
import sys
import os
import numpy as np
import pandas as pd

# Paths input
val_metric_path=input("Enter the path of the validation run name (ex: ../run/val/[RUN_NAME]/): ")

os.rename(val_metric_path + "c0.2_i0.0/Validation_Metrics.txt", val_metric_path + "c0.2_i0.0/Validation_Metrics.csv")

#df = pd.read_csv(val_metric_path + "c0.2_i0.0/Validation_Metrics.txt", sep="\t")

#df.to_excel("Validation_Metrics.xlsx", "Sheet1")
