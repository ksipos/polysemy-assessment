#!/bin/bash
# Prerequisites: AllenNLP's ELMo module

if [ "$#" -ne 5 ]; then
    echo "Illegal number of parameters. Expected parameters: word_list_file, corpus_file, ELMo_weights, ELMo_options, output_directory"
    exit 2
fi

word_list=$1 # File with one word per line
corpus=$2
elmo_weights=$3
elmo_options=$4
output_directory=$5
mkdir "$output_directory"

lines_directory="$output_directory""/lines_index"
mkdir $lines_directory
while IFS= read -r line
do
	# Each line contains a word
	# GREP is used to find lines of the corpus that contain the word
	# -i : ignore case, -n: line number, -w: search for exact word
	# CUT is used to get just the line number and ignore the rest sentence
	# The line counting of GREP starts from '1' 
	grep -i -n -w "$line" $corpus  | cut -d":" -f1 > "$lines_directory/$line"
done < "$word_list"


sentences_directory="$output_directory""/sentences/"
vectors_directory="$output_directory""/vectors/"
reduced_vectors_directory="$output_directory""/reduced_vectors/"
mkdir $sentences_directory
mkdir $vectors_directory
mkdir $reduced_vectors_directory

# Python script that uses the given corpus, and the line indexes to pick 3000 sentences
python extract_sentences.py "$corpus" "$lines_directory" "$sentences_directory" 3000

for lines_file in "$lines_directory/"*
do	
	word=$(echo $(echo $file | cut -d"/" -f2) | cut -d"." -f1)
	echo "Current word: " $word
	vectors_file="$vectors_directory""$word"".hdf5"
	vectors_reduced_file="$reduced_vectors_directory""$word"".hdf5"
	
	if [ -f $vectors_reduced_file ] # Validate that the file has not already being parsed
	then
		echo "Skipping $word ..."
	else   
		echo "Processing $word ..."
		# Using AllenNLP's framework to get pass the sentence file through ELMo
		# The generated file has one vector per word on each sentence
		allennlp elmo --cuda-device 0 --weight-file $elmo_weights --options-file $elmo_options --top "$sentences_directory/""$word" $vectors_file
		# Python script used to discard the vectors of other words and keep only one vector per sentence
		python reduce_vectors_unique.py $vectors_file
		# Remove the file to save space
		rm $vectors_file
	fi
done
rmdir $vectors_directory
