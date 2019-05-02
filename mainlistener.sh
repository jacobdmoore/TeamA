# This is the script to be run by the lecturer before the lecture.

# Shell script asks user if it can initialize, and then it creates the subfolders/files necessary.
read -r -p "Before recording, it is best for me to initialize the appropriate files and folders. This could result in old transcribed data being deleted accidentally. Proceed? [y/N]" response
case "$response" in
    [yY][eE][sS]|[yY]) 
        rm action_key_tracker.txt
        rm filenumber.txt
        rm full_keylog.txt
        rm timestamp_history.txt
        rm *_notes.pptx
        mkdir -p ./slideVoice
        mkdir -p ./tempFiles
        mkdir -p ./textFiles
        mkdir -p ./voiceFiles
        rm ./slideVoice/*
        rm ./tempFiles/*
        rm ./textFiles/*
        rm ./voiceFiles/*
        ;;
    *)
        exit 0
        ;;
esac

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

python newrecordlecture.py &
python keylistener.py "$google_slides" &
echo 'Now recording! To cease recording, press CTRL + C.' &

wait
