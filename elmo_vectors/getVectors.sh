#!/bin/bash
source activate allennlp
weights="/data/home/cxypolop/Projects/Disambiguation/elmo_weights/elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5"
options="/data/home/cxypolop/Projects/Disambiguation/elmo_weights/elmo_2x4096_512_2048cnn_2xhighway_options.json"
for file in llines/*
do	
	word=$(echo $(echo $file | cut -d"/" -f2) | cut -d"." -f1)
	echo $word
	file_name="stored_vectors/""$word"".hdf5"
	reduced="stored_vectors/""$word""_reduced.hdf5"
	sentences="new_extracted/""$word"".txt"
	if [ -f $reduced ]
	then
		echo "Skipping $word ..."
	else   
		echo $index_name $word
		echo "Processing $word ..."
		allennlp elmo --weight-file $weights --options-file $options --top $sentences $file_name
		python reduce_vectors.py $file_name
		rm $file_name
	fi
done

