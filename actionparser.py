# Interpret output from keyparser.py - based on action_key_tracker.txt,
# this script sorts the actions by type and translates that into slide number.
# Timestamp interpretation coming soon.
# Written by Jacob Moore, (c) 2019

with open('action_key_tracker.txt','r') as file:
    f = file.read()

lines_list = f.split('\n')[1::]

# Force any transcribed audio between start of program and start of presentation at Slide 0*.
slide_number = ['0*']
timestamp_start = []
timestamp_end = []
presentation_mode = 0
prev_shift = 0

for line in lines_list:
	# Extracts first set of characters before a space in each line, which corresponds to the action type.
    action_type = line.split(' ')[0]
    if not timestamp_start:
    	timestamp_start.append(0.0)
	
	# Valid actions outside of presentation mode.
    if presentation_mode == 0:
        timestamp = line.split(' ')[-1]
		# User hits F5 to enter presentation mode.
        if action_type == 'ENTER':
	    	# User hit shift before F5 -> enter at current slide.
            if prev_shift == 1:
                slide_number.append(slide_number[-2])
                timestamp_end.append(timestamp)
	    	# User only hit F5 -> enter at first slide.
            else:
                slide_number.append(0)
                timestamp_end.append(timestamp)

            presentation_mode = 1
            prev_shift = 0
        # User hits shift -> see what happens next...
        elif action_type == 'SHIFT':
            prev_shift = 1

	# Valid actions inside presentation mode.    	
    elif presentation_mode == 1:
        timestamp_start.append(timestamp)
        timestamp = line.split(' ')[-1]
	    # User hits escape -> exit presentation mode.
        if action_type == 'EXIT':
            presentation_mode = 0
            slide_number.append(str(slide_number[-1]) + '*')
            timestamp_end.append(timestamp)
            timestamp_start.append(timestamp)
            prev_shift = 0
        # User hits next -> slide number advanced.
        elif action_type == 'NEXT':
            slide_number.append(slide_number[-1] + 1)
            timestamp_end.append(timestamp)
            prev_shift = 0
        # User hits previous not on first slide -> slide number decreased.
        elif action_type == 'PREVIOUS' and slide_number[-1] > 0:
            slide_number.append(slide_number[-1] - 1)
            timestamp_end.append(timestamp)
            prev_shift = 0
        # User hits shift -> see what happens next...
        elif action_type == 'SHIFT':
            prev_shift = 1

timestamp_end.append(timestamp)

# Export timestamp history.
with open('timestamp_history.txt','w+') as file:
    header = 'Timestamp history'
    file.write(header)

for (number, start, end) in zip(slide_number, timestamp_start, timestamp_end):
    with open('timestamp_history.txt', 'a') as file:
            file.write('\nSlide ' + str(number) + ': ' + str(start) + ' <-> ' + str(end))