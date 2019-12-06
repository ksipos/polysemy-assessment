###### French
#
#name='../french_wikipedia_text'

###### English
name='../parsed_text.txt'
lang="en"

echo "Starting pipeline for language: " "$lang"
echo "Counting unigrams..."

gawk '{for(x=1;$x;++x)print tolower($x)}' "$name" | sed 's/ //g' | sort | uniq -c > "$lang""_tmp.txt"
cat "$lang""_tmp.txt" | sed -e 's/^[ \t]*//' > "$lang""_unigrams.txt"

echo "Sorting frequency list..."

sort -t ' ' -k1,1rn -k2,2 "$lang""_unigrams.txt" > "$lang""_sorted_unigrams.txt"
rm "$lang""_unigrams.txt"
rm "$lang""_tmp.txt"

echo "Preprocessing generated list..."

python preprocess_unigrams.py "$lang""_sorted_unigrams.txt"

echo "Exporting lines containing words..."

output="$lang""_sentenceLines/"
mkdir $output
while IFS= read -r line
do
	grep -n -w "$line" "$name"  | cut -d":" -f1 > "$output""$line"
done < "$lang""_wordlist.txt"

echo "Exporting selected sentences..." 

python extract_sentences_nov.py "$name" "$output" "$lang""_extracted_sentences" 3000

