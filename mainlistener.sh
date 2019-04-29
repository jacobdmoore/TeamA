# This is the script to be run by the lecturer before the lecture.

# Shell script asks user question, passes answer to Python.
read -r -p "Will you be using Google Slides to present today? [y/N] " response
case "$response" in
    [yY][eE][sS]|[yY]) 
        google_slides=1
        ;;
    *)
        google_slides=0
        ;;
esac

# Allows two pythons scripts to run simultaneously (both in background).
# Allows passing of KeyboardInterrupt to Python from shell.
# First program records audio, second one records keystrokes and outputs as action_key_tracker.txt.
trap "exit" INT TERM ERR
trap "kill 0" EXIT

python recordlecture.py &
python keylistener.py "$google_slides" &
echo 'Now recording! To cease recording, press CTRL + C.' &

wait