# This is the script to be run by the lecturer after the lecture.
trap "exit" INT TERM ERR
trap "kill 0" EXIT

echo 'Processing transcribed audio and keyboad/mouse actions...'
python actionparser.py
python recordSplit.py

### added code
cd textFiles
ls -f . | wc -l>filenumber.txt  ### counts number of text files in textFiles and outputs it to a text file. number of files is # in text file minus 3
cd ..
mv textFiles/filenumber.txt filenumber.txt  ##moves filenumber.txt to parent directory 

python populatenotes.py

echo 'Complete!'
