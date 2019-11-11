mkdir workrepo
cd workrepo
git init
cp -r ../Feedback/. .
git add .
git commit -m commit
git archive -o ../feedback.zip @
#while IFS='' read -r line || [[ -n "$line" ]]; do
#    echo $line | tr -cd [:digit:] >> $line-num.txt
#done < "$1"
cd ..
rm -rf workrepo