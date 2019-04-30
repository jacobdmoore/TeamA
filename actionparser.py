# Interpret output from keyparser.py - based on action_key_tracker.txt,
# this script sorts the actions by type and translates that into slide number.
# Timestamp interpretation coming soon.
# Written by Jacob Moore, (c) 2019

def sublist_in_list(sublist,biglist):
    subtract_range = len(sublist)
    list_of_occurences = []
    for index in range(len(biglist) +1 - subtract_range):
        compare_sublist = [biglist[subindex] for subindex in range(index,index + subtract_range)]
        if compare_sublist == sublist:
            list_of_occurences.append(index)
    
    return list_of_occurences

with open('action_key_tracker.txt','r') as file:
    f = file.read()

lines_list = f.split('\n')[0::]
first_line = lines_list.pop(0)

if 'Google Slides' in first_line:
    google = True
else:
    google = False

# Google Sheets has different keyboard shortcuts from PowerPoint/LibreOffice.
if google:
    enter_actions_0 = ['CTRL','SHIFT','ENTER']
    enter_actions_current = ['CTRL','ENTER']
elif not google:
    enter_actions_0 = ['ENTER']
    enter_actions_current = ['SHIFT','ENTER']

timestamp_actions = ['EXIT','ENTER-C','ENTER-0','NEXT','PREVIOUS','ENTER']
exit_actions = ['EXIT']
next_actions = ['NEXT']
previous_actions = ['PREVIOUS']

# can figure out timestamps p easily by only following timestamp actions
# need to find a way of finding sequences of elements in list, could make it into one long list
# whenever F5 happens, look at elements before

# Force any transcribed audio between start of program and start of presentation at Slide 0*.
slide_number = []
timestamp_start = []
timestamp_end = []
presentation_mode = 1
action_time_list = [('EXIT','0.0')]

for line in lines_list:
    action_time_list.append((line.split(' ')[0],line.split(' ')[-1]))

action_list = []
time_list = []

for action_time in action_time_list:
    current_action = action_time[0]
    current_time = action_time[1]
    action_list.append(current_action)
    time_list.append(current_time)

# Figuring out action sequences (CTRL SHIFT ENTER, etc.)
indices_enter = sublist_in_list(enter_actions_current,action_list)

# Reverse order so as not to mess up indices.
#replace the elements with one enter-c
for index in reversed(indices_enter):
    seq_timestamp = time_list[index + len(enter_actions_current) - 1]
    for subindex in reversed(range(index,index + len(enter_actions_current))):
        del action_list[subindex]
        del time_list[subindex]
    action_list.insert(index,'ENTER-C')
    time_list.insert(index,seq_timestamp)

indices_enter_0 = sublist_in_list(enter_actions_0,action_list)
#replace the elements with one enter-0
for index in reversed(indices_enter_0):
    seq_timestamp = time_list[index + len(enter_actions_0) - 1]
    for subindex in reversed(range(index,index + len(enter_actions_0))):
        del action_list[subindex]
        del time_list[subindex]
    action_list.insert(index,'ENTER-0')
    time_list.insert(index,seq_timestamp)
		#replace the elements with one enter-0

for index, (action, time) in enumerate(zip(action_list,time_list)):

    #print(action,'at',time,'and presentation_mode=',presentation_mode)

    # Get rid of any actions that aren't timestamp-worthy.
    if action not in timestamp_actions:
        del action_list[index]
        del time_list[index]
        continue

    # End timestamps informed by next beginning.
    if len(timestamp_start) > 1:
        timestamp_end.append(timestamp_start[-1])

    # Since we've cleared out non-timestamp actions, we can append start times whenever we append slide.
    if presentation_mode == 1:
        if action in next_actions:
            slide_number.append(str(int(slide_number[-1]) + 1))
            timestamp_start.append(time)

        if action in previous_actions:
            slide_number.append(str(int(slide_number[-1]) - 1))
            timestamp_start.append(time)

        if action in exit_actions:
            presentation_mode = 0
            if slide_number:
                slide_number.append(str(slide_number[-1]) + '*')
                timestamp_start.append(time)
            else:
                slide_number.append('0*')
                timestamp_start.append(time)
            continue

    else:
        if action == 'ENTER-C':
            presentation_mode = 1
            slide_number.append(slide_number[-1].replace('*',''))
            timestamp_start.append(time)

        elif action in ['ENTER-0','ENTER']:
            presentation_mode = 1
            slide_number.append(str(0))
            timestamp_start.append(time)
        #else presentation mode remains 0
    
timestamp_end.append(timestamp_start[-1])
timestamp_end.append('end')

# Export timestamp history.
with open('timestamp_history.txt','w+') as file:
    header = 'Timestamp history'
    file.write(header)

for (number, start, end) in zip(slide_number, timestamp_start, timestamp_end):
    with open('timestamp_history.txt', 'a') as file:
            file.write('\nSlide ' + str(number) + ': ' + str(start) + ' <-> ' + str(end))