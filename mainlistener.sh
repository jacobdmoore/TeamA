# Allows two pythons scripts to run simultaneously.

# This is the script to be run by the lecturer before the lecture.
# First program records audio, second one records keystrokes and outputs as action_key_tracker.txt.
python recordUI.py &
python keylistener.py &