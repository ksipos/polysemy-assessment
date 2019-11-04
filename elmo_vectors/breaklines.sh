#!/bin/bash
for file in full_lines/*
do	
	word=$(echo $(echo $file | cut -d"_" -f3) | cut -d"." -f1)
	index_name="llines/""$word"".txt"
	cat $file | tr ' ' '\n' > tmp.txt
	sort -n tmp.txt > $index_name
	#rm $file
done
