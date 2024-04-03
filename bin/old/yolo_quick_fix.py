### Cocosplit exports yolo files with three classes [berries, green, blue].
### This is due to some datasets having the superclass berries show up as its own class.
### Val.py doesn't work without the classes being the same, so this is a quick fix to
### move all the yolo labels' class # (the first digit in the yolo txt files) over by 1.

### USAGE: python yolo_quick_fix.py

### Found @ https://stackoverflow.com/questions/61990495/need-to-replace-the-first-words-of-each-line-in-several-text-files

# Imports
import os

# Get input
dirname = input("What is the directory name that will be modified? (ex: ../data/validation_data/[DATASET]/[train/valid/test]/labels): \n>")


for txt_in in os.listdir(dirname):
    with open(os.path.join(dirname, txt_in), 'r') as f:
        # Don't read entire file since we
        # are looping line by line
        #infile = f.read()# Read contents of file
        result = []
        for line in f:  # changed to file handle
            line = line.rstrip() # remove trailing '\n'
            # Only split once since you're only check the first word
            words = line.split(" ", maxsplit = 1)
            word = words[0]  # word 0 may change
            if word == "0":
                word = word.replace('0', '1')
            elif word=="1":
                word = word.replace('1', '2')
            else:
                pass
            # Update the word you modified
            words[0] = word  # update word 0
            # save new line into results
            # after converting back to string
            result.append(" ".join(words))

    with open(os.path.join(dirname, txt_in), 'w') as f:
        # Convert result list to string and write to file
        outfile = '\n'.join(result)
        f.write(outfile)
