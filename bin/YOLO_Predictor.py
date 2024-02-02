### YOLO_Predictor makes predictions on specified images using a specified weight file.

# USAGE: python ./YOLO_Predictor.py

# Imports
import torch
import cv2
import os
import pwd
from PIL import Image
import math
from ultralytics import YOLO
import numpy as np

def get_username():
    return pwd.getpwuid(os.getuid())[0]

# Read the current brightness from the config file
config = configparser.ConfigParser()
config.read('config.ini')
yolov5_path = config.get('paths', 'yolov5_path')

# INPUTS
change_parameters = input("Do you want to use different parameters for this run? (y/n)\n>")
if change_parameters == "y":
    # Defining weight file path
    weight_path = input("What is the path to the weight file you want to use? (relative path (ex: ../path/to/run/folder/best.pt) or full path)\n>")

    # Loading the model
    model = torch.hub.load(repo_or_dir='ultralytics/yolov5',
                           model='custom',
                           path=weight_path,
                           force_reload=True)

    # Model settings
    change_model_settings = input("Do you want to use different model settings for this run? (y/n)\n>")
    if change_model_settings == "y":
        model.conf = float(input("What model.conf do you want to use? (default is 0.1)\n>"))
        model.iou = float(input("What model.iou do you want to use? (default is 0.3)\n>"))
        model.agnostic = True if input("Enable model.agnostic? (default is True)\n>") == "True" else False
        model.multi_label = True if input("Enable model.multi_label? (default is False)\n>") == "True" else False
        model.hide_labels = True if input("Enable model.hide_labels? (no default)\n>") == "True" else False
        model.hide_conf = True if input("Enable model.hide_conf? (no default)\n>") == "True" else False

    # Path to the directory of images to make predictions on
    image_dir_path = input("What is the path (from yolov5 repo) to the images you want to make predictions on? (ex: predictions/datasets/)\n>")

    # Path to the directory you want to put the results
    result_path = input("Where would you like to send the results to? (ex: {yolov5_path}/predictions/results/)\n>")

    # Name of the directory containing the results
    result_dir_dataset = input("What is the name you want to give to this run? "
                               "\n(Note: the name will have the conf and iou added like so: 'NAME_c0.1_i0.3')\n>")
    result_dir = result_path + result_dir_dataset + "_c" + str(model.conf) + "_i" + str(model.iou)

    # Inference size
    box_dim = int(input("What is the image inference size? (default is 640)\n>"))

# Else case is essentially the default value. If you want to save time, change the values here.
else: 
    # Defining weight file path
    weight_path = f'{yolov5_path}/runs/train/Test_Export_640x640_300-epochs/weights/best.pt'

    # Loading the model
    model = torch.hub.load(repo_or_dir='ultralytics/yolov5',
                           model='custom',
                           path=weight_path,
                           force_reload=True)

    # Model settings
    model.conf = 0.1  # NMS (Non-Max Suppression) confidence threshold; (0.1 works well)
    model.iou = 0.3  # NMS IoU threshold; (0.3 works well)
    model.agnostic = True  # NMS class-agnostic (True works well)
    model.multi_label = False  # NMS multiple labels per box (False works well)
    model.hide_labels = False  # Hide the class labels on finished predictions
    model.hide_conf = False  # Hide the confidence labels on finished predictions

    # Path to the directory of images to make predictions on
    image_dir_path = f"{yolov5_path}predictions/datasets/P3-Prediction-Image/"

    # Path to the directory you want to put the results
    result_path = f"{yolov5_path}predictions/results/"

    # Name of the directory containing the results
    result_dir_dataset = "Test_Export_640x640_300-epochs"
    result_dir = result_path + result_dir_dataset + "_c" + str(model.conf) + "_i" + str(model.iou)

    # Inference size
    box_dim = 640


# Folder to test
files = os.listdir(image_dir_path)

# Make directory if necessary
try:
    os.mkdir(result_dir)
except Exception as e:
    print(f"Note: {result_dir} directory already exists")

f = open(f'{result_dir}/total_counts.txt', "a")
for i, file in enumerate(files):
    if str(file).endswith(("png", "PNG", "jpg", "JPG", "jpeg", "JPEG")):
        images = []
        im = Image.open(image_dir_path + file)
        for x in range(0, im.width, box_dim):
            for y in range(0, im.height, box_dim):
                images.append(im.crop((x, y, x+box_dim, y+box_dim)))

        x_dim = math.ceil(im.width/box_dim)
        y_dim = math.ceil(im.height/box_dim)

        results = model(images)

        image = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        pix = im.load()

        green_count = 0
        blue_count = 0
        for xi in range(x_dim):
            for yi in range(y_dim):
                boxes = results.xyxy[xi*y_dim + yi].cpu().numpy()

                x_offset = xi*box_dim
                y_offset = yi*box_dim

                for i, box_1 in enumerate(boxes):
                    box_1[0] = box_1[0] + x_offset
                    box_1[1] = box_1[1] + y_offset
                    box_1[2] = box_1[2] + x_offset
                    box_1[3] = box_1[3] + y_offset


                for box in boxes:
                    if box[5] == 1:
                        green_count += 1
                        cv2.rectangle(image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 0, 255), 2)
                    else:
                        blue_count += 1
                        cv2.rectangle(image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (255, 0, 0), 2)

        print(f'{file}: Green: {green_count}, Blue: {blue_count}', file=f)
        print(f'{file}: Green: {green_count}, Blue: {blue_count}')

        cv2.imwrite(f'{result_dir}/Output_{file}', image)
f.close()
