### This script evaluates if a dataset is ready for training/validation. This is
### done by looking at the paths present in the data.yaml to see if they exist,
### if there is data located at those paths, and (in the case of training) if
### there is validation data alongside the training data. It will also tell you
### if the dataset has been split into tiles or not.

### USAGE: Not used directly; called by other scripts

import os
import yaml
from termcolor import colored


def evaluate_dataset(path_to_dataset, type_of_dataset, needs_to_be_tiled=True):
    dataset_name = os.path.basename(path_to_dataset[:-1])

    dataset_exists = os.path.exists(path_to_dataset)

    data_yaml_path = f"{path_to_dataset}data.yaml"
    data_yaml_exists = os.path.exists(data_yaml_path)

    print(data_yaml_path)
    print(data_yaml_exists)

    if "Fold" in dataset_name:
        # Gets the base_name in something like "/path/to/base_name/Fold1/"
        base_name = os.path.basename(os.path.dirname(path_to_dataset[:-1]))
        data_in_tiles = "640x640" in base_name
    else:
        # Otherwise, just look in dataset_name "/path/to/dataset_name/"
        data_in_tiles = "640x640" in dataset_name

    if needs_to_be_tiled and not data_in_tiles:
        print(colored(f"{dataset_name} has NOT been split into tiles! Please perform this step before training!", 'red'))
        return False

    if data_yaml_exists:
        with open(data_yaml_path, "r") as stream:
            try:
                # Load the YAML content
                yaml_content = yaml.safe_load(stream)

                train_path_exists = os.path.exists(yaml_content['train'])
                #print (f"Does {yaml_content['train']} exist? \tAnswer: {train_path_exists}")

                valid_path_exists = os.path.exists(yaml_content['val'])
                #print (f"Does {yaml_content['val']} exist? \tAnswer: {valid_path_exists}")

                test_path_exists = os.path.exists(yaml_content['test'])
                #print (f"Does {yaml_content['test']} exist? \tAnswer: {test_path_exists}")

                #print (f"Does {path_to_dataset} exist? \tAnswer: {dataset_exists}")
                #print (f"Does {data_yaml_path} exist? \tAnswer: {data_yaml_exists}")

                if type_of_dataset == "training":
                    if train_path_exists and valid_path_exists:
                        print(colored(f"{dataset_name} is ready for training!", 'green'))
                        return True
                    else:
                        print(colored(f"{dataset_name} is NOT ready for training.", 'red'))
                        return False
                elif type_of_dataset == "validating":
                    if valid_path_exists:
                        print(colored(f"{dataset_name} is ready for validating!", 'green'))
                        return True
                    else:
                        print(colored(f"{dataset_name} is NOT ready for validating.", 'red'))
                        return False
            except yaml.YAMLError as exc:
                print(exc)
                return False


if __name__ == "__main__":
   evaluate_dataset(path_to_dataset=input("Dataset : "), type_of_dataset=input("Type of dataset : "))
