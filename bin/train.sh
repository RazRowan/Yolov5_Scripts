#!/bin/bash

# Variable for the hyperparameters being used
hyp_path=$(echo '../data/hyps/hyp.scratch-low.yaml')

# Source Chau's python environment
source ../../python_env/bin/activate

# Run the train.py script
echo "Enter the path of the data (ex: ../data/weights/[DATASET]/): "
read data_path
echo "Enter the batch-size to train with (ex: 64): "
read batch_size
echo "Enter the name of this training run: "
read run_name
echo "Enter the number of epochs to train with (ex: 300): "
read num_epochs

yaml_path=${data_path}data.yaml

python ../train.py --data $yaml_path  --batch-size=$batch_size --name $run_name --epochs=$num_epochs --hyp $hyp_path

# Go to the data.yaml and get the train/test path
train_path=$(cat $yaml_path | head -n1 | sed -n 's/train: //p')
train_path=$(echo '.'"$train_path")
test_path=$(cat $yaml_path | head -n2 | sed -n 's/val: //p')
test_path=$(echo '.'"$test_path")


############## v Used to save the training information

# Count up the amount of images in the data set
#train_size=$(cd $train_path &&  ( ls | wc -l))
#test_size=$(cd $test_path &&  ( ls | wc -l))
#total_size=$(expr $train_size + $test_size)

# Actually receive the data from the hyp
#hyps=()
#while IFS= read -r line; do
#  hyps+=("$line")
#done < <(tail -n29 $hyp_path)

# Run the save_hyps.py
#python ./save_hyps.py $data_path $run_name $total_size $num_epochs "${hyps[@]}" 

############## ^ commented out because we don't really need to use it at the moment
