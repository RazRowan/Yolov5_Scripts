import os
import glob

def print_files_path(path, num_of_files):
    # Get the list of files in the directory
    files = glob.glob(os.path.join(path, '*'))

    # Sort the files by modification time
    files.sort(key=os.path.getmtime, reverse=True)

    # Print the # most recent files
    print(f"You likely want to train with some recent data, here's the {num_of_files} most recent in your training_data area!")
    if num_of_files > len(files):
        num_of_files = len(files)
    for i in range(num_of_files):
        print(f" - {os.path.basename(files[i])}")
