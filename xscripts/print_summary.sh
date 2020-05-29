

find ./xdata/in_data -iname "*.txt" -print0 | xargs -0 grep " modi "

for i in `ls *.txt`
do
    if [[ "$i" =~ .*".txt" ]]; then
        sed -ne 's/<[^>]*>//g' $i
    fi
done
