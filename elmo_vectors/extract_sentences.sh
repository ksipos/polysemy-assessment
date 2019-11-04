#results=()
while read word
do
	tmp=$( grep -n --color -w "$word" sentences_full.txt | cut -f1 -d:)
	if [ ! -z "$tmp" ]
	then
		echo $tmp > "full_lines/lines_$word.txt"
	fi
done < "wordlist.txt"
