#!/bin/bash

# Variable for the hyperparameters being used
hyp_path=$(echo '../data/hyps/hyp.scratch-low.yaml')

# Source Chau's python environment
source ../../python_env/bin/activate

# Vars needed to train the folds
echo "How many folds are there to train?"
read num_folds
echo "Enter the path of the Master Set (ex: ../data/weights/[MASTER_SET]/): "
read master_set_path

# Vars needed to store values used while training
echo "Enter the batch-size to train with (ex: 16): "
read batch_size
echo "Enter the number of epochs to train with (ex: 300): "
read num_epochs

# Additional var for naming Fold dirs
master_set_name=$(basename $master_set_path)

for (( i=1; i<=$num_folds; i++ ))
do
	run_name=${master_set_name}/Fold${i}
	fold_path=$master_set_path/Fold${i}/
	yaml_path=${fold_path}data.yaml

	nohup python ../train.py --data $yaml_path --batch-size=$batch_size --name $run_name --epochs=$num_epochs --hyp $hyp_path --save-period 50 --device $i  &

	# Go to the data.yaml and get the train/test path
	train_path=$(cat $yaml_path | head -n1 | sed -n 's/train: //p')
	train_path=$(echo '.'"$train_path")
	test_path=$(cat $yaml_path | head -n2 | sed -n 's/val: //p')
	test_path=$(echo '.'"$test_path")

	# Count up the amount of images in the data set
	#train_size=$(cd $train_path && ( ls | wc -l))
	#test_size=$(cd $test_path && ( ls | wc -l))
	#total_size=$(expr $train_size + $test_size)

	#hyps=()
	#while IFS= read -r line; do
	#  hyps+=("$line")
	#done < <(tail -n29 $hyp_path)

	#printf "\nDetails for fold${i}: \n"
	#echo "----------------------------------" 
	#printf "\n"
	#python ./save_hyps.py $fold_path $run_name $total_size $num_epochs "${hyps[@]}"
	##### ^ commented out because save_hyps isn't important right now, can change later

	printf "\n"
	echo "##################################"
	printf "Fold${i} training started...\n"
	echo "##################################"
	printf "\n"
done
