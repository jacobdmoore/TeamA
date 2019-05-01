# This script outputs sound file for slide from compelte lecture as per input by Keystroke program and saves it
# by the slide number in slideVoice folder
# Written by Varun Soni, (c) 2019
from pydub import AudioSegment
from splitSlideVoice import splitSlideVoice
import os
def recordSplit(a=75,b=165,slide=2):
    sound = AudioSegment.from_file(os.getcwd() + "/voiceFiles/lecture.wav")
    print(len(sound))
    reqVoice = sound[a*1000:b*1000]
    fileName= os.getcwd() + "/slideVoice/"  + str(slide) + ".wav"
    reqVoice.export(fileName, format="wav")
    splitSlideVoice(fileName,slide)
    print('completed slide',slide)

with open('timestamp_history.txt','r') as file:
    f = file.read()

lines_list = f.split('\n')[0::]
lines_list.pop(0)

timestamp_list = []

file_length = len(AudioSegment.from_file(os.getcwd() + "/voiceFiles/lecture.wav"))/1000

for line in lines_list:
    if line: #excludes any empty lines that might arise
        split_line = line.split(' ') #split up line by spaces
        start = split_line[-3] #start time is always 2nd to last word
        end = split_line[-1] #end time is always last word
        if end == 'end':
            end = file_length
        slide = split_line[1][:-1] #excludes colon
        timestamp_list.append((slide,start,end))

for slide, start, end in timestamp_list:
    recordSplit(float(start),float(end),slide)