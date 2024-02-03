## This is used in other scripts to generate a random seed

import random
import string
import configparser


# Read the current brightness from the config file
config = configparser.ConfigParser()
config.read('config.ini')
yolov5_path = config.get('paths', 'yolov5_path')
scripts_path = config.get('paths', 'scripts_path')
training_data_path = config.get('paths', 'training_data_path')
num_of_files = int(config.get('parameters', 'default_num_of_files'))


def random_seed(project_name, length):
    # Define the characters that will be used
    characters = string.digits

    # Generate the random seed string
    seed_string = ''.join(random.choice(characters) for i in range(length))

    # Make a directory to hold the seeds
    folder_name = f"{scripts_path}bin/seeds/fold/"
    try:
        os.makedirs(folder_name)
    except Exception as e:
        print(f"Note: {folder_name} directory already exists")

    # Write seed to file
    with open(f"{folder_name}{project_name}_fold_random_seed.txt", 'w') as f:
        f.write(seed_string)

    return seed_string
