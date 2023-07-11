### Yolov5_Scripts
These are scripts I, or others have created for Yolov5, and more specifically for the Blueberry Drone Project at Rowan University.

# How to use these scripts
1. All, if not, most of these scripts were created in a /bin dir that sits in the yolov5 repo. To avoid path issues, just copy this /bin repo into your yolov5 dir.
2. The scripts for the process of cross-validation, and the scripts relating to getting the metrics from val.py require changes to two files. It's possible to replace your val.py and /utils/metrics.py with the ones in this repo, HOWEVER, there may be new versions of these scripts released in the official yolov5 repo by the time you clone their repo and this one. I have pulled down recent changes and merged the files (as of 7/11/2023).
3. Open the scripts to understand how to use them. For the most part, they are either "./script.sh" or "python ./script.py", but there may be scripts that require in-line parameters.
