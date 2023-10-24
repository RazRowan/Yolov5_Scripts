### Open scripts up in a text editor for more information about the scripts, and how to use them.

## Normal Process - Folding, training, then cross-validation
1. fold.py
2. fold-train.sh
3. cross-val.py *

* DEPRECATED, do not use as of 10/11/2023

## Single Train - Folding, then training
1. fold.py *
2. train.sh

* Only needed if the data being trained has no validation/testing set

## Validation Testing Scripts
- easy_val.py
- quick_val.py

## Other Scripts
- FullBushDivider.py - Created by Anthony Thompson
- yolo_quick_fix.py - Created via StackOverflow post
- save_hyps.py - Old script that was used to save training info in fold_train.sh and train.sh
