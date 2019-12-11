#!/bin/bash
source activate allennlp
weights="/data/home/cxypolop/Projects/Disambiguation/elmo_weights/elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5"
options="/data/home/cxypolop/Projects/Disambiguation/elmo_weights/elmo_2x4096_512_2048cnn_2xhighway_options.json"
vectors_path="/data/home/cxypolop/vectors2/"
for file in en_extracted_sentences/*
do	
	word=$(echo $(echo $file | cut -d"/" -f2) | cut -d"." -f1)
	echo $word
	file_name="$vectors_path""$word"".hdf5"
	reduced="$vectors_path""$word""_reduced.hdf5"
	sentences="en_extracted_sentences/""$word"".txt"
	if [ -f $reduced ]
	then
		echo "Skipping $word ..."
	else   
		echo $index_name $word
		echo "Processing $word ..."
		allennlp elmo --cuda-device 0 --weight-file $weights --options-file $options --top $sentences $file_name
##		allennlp elmo --top "$word"".txt" $file_name
		python reduce_vectors_unique.py $file_name
		rm $file_name
	fi
done
