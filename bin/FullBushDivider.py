### FullBushDivider.py cuts up original dataset images (ex: 3200x3200) into
### 640x640 tiles. This results in better training performance due to its
### smaller size.

# USAGE: python ./FullBushDivider.py

from copy import deepcopy
import os
import csv
from PIL import Image

# Converts YOLOv5 data to XYXY coordinates
def YOLOv5ToXYXY(data):
    newdata = deepcopy(data)
    for box in newdata:
        x_center = float(box[1])
        y_center = float(box[2])
        half_width = float(box[3]) / 2
        half_height = float(box[4]) / 2
        box[1] = x_center - half_width
        box[2] = y_center - half_height
        box[3] = x_center + half_width
        box[4] = y_center + half_height
    return newdata

# Size to divide image into
img_dim = 640

# Path to the YOLOv5 blueberry annotations (directory should contain an images and labels folder that was exported from Roboflow)
dir_path=input('Path to the valid folder (ex: ../data/validation_data/DATASET): ')

#Folder to test
files = os.listdir(f"{dir_path}/valid/labels")

# Make directory if necessary
try:
    os.mkdir(dir_path+"/output_berries")
except Exception as e:
    print("Note: output_berries directory already exists")

pos = 0 

# Go through each annotation file
for file in files:  
    pos += 1
    #print(file)
    
    # Get path to blueberry annotation labels
    data_path = f'{dir_path}/valid/labels/{file}'
    
    # Get the current image
    image = Image.open(f'{dir_path}/valid/images/{file[:-3]}jpg')

    # Open blueberry annotation file
    with open(data_path, newline='') as csvfile:
        data = list(csv.reader(csvfile, delimiter=' ', quotechar='|'))
    
    # Convert the file to XYXY coordinates
    image_xyxy = YOLOv5ToXYXY(data)
    x, y = image.size
    x_scale = x / img_dim
    y_scale = y / img_dim
    
    for i in range(img_dim, x, img_dim):
        for j in range(img_dim, y, img_dim):
            berries = []
            low_x = (i - img_dim) / x
            low_y = (j - img_dim) / y
            high_x = i / x
            high_y = j / y
            
            for xyxy in image_xyxy:
                if (xyxy[3] + xyxy[1]) / 2 > low_x and (xyxy[3] + xyxy[1]) / 2 < high_x and (xyxy[4] + xyxy[2]) / 2 > low_y and (xyxy[4] + xyxy[2]) / 2 < high_y:
                    berries.append(xyxy)
            
            im = image.crop((i - img_dim, j - img_dim, i, j))
            
            #if not berries:
                #print(file)
                #im.save(f"output_berries/empty/{file[:-3]}{i - img_dim}.{j - img_dim}.jpg")
            
            # Save output in YOLOv5 format    
            with open(dir_path+"/output_berries/labels/{i - img_dim}.{j - img_dim}.{file}", 'w') as f:
                for berry in berries:
                    berry[1] = max(0, berry[1])
                    berry[2] = max(0, berry[2])
                    berry[3] = min(1, berry[3])
                    berry[4] = min(1, berry[4])
                    f.write(f"{berry[0]} {((berry[3] + berry[1]) / 2 - low_x) * x_scale} {((berry[4] + berry[2]) / 2 - low_y) * y_scale} {(berry[3] - berry[1]) * x_scale} {(berry[4] - berry[2]) * y_scale}\n")    
            
            # Save cropped image
            im.save(dir_path+"/output_berries/images/{i - img_dim}.{j - img_dim}.{file[:-3]}jpg")
