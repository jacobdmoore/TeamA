# This is the script to be run by the lecturer after the lecture.
trap "exit" INT TERM ERR
trap "kill 0" EXIT

echo 'Processing transcribed audio and keyboad/mouse actions...'
python actionparser.py
python recordSplit.py
python populatenotes.py
echo 'Complete!'
