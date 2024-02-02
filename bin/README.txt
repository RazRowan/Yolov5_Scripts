### Open scripts up in a text editor for more information about the scripts, and how to use them.

# NOTE: Change config.ini values to match your path names!!!

## Normal Process - Folding, training, then cross-validation
1. fold.py
2. fold-train.py
3. cross-val.py *

* DEPRECATED, do not use as of 10/11/2023

## Single Train - Folding, then training
1. dataset_assigner.py **
2. FullBushDivider.py
3. Train.py

** Only needed if the data being trained has no validation/testing set

## Validation Testing Scripts
- easy_val.py - Makes using val.py a bit easier
- quick_val.py - Performs MANY validation tests en masse

## Other Scripts
- YOLO_Predictor.py - Used to make predictions with a weight file
- FullBushDivider.py - Created by Anthony Thompson to split datasets into 640x640 tiles
- yolo_quick_fix.py - Created via StackOverflow post
- save_hyps.py - Old script that was used to save training info in fold_train.sh and train.sh
