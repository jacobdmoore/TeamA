# This script converts voice for particular slide and saves it as slide number in textFiles folder
# Written by Varun Soni, (c) 2019
import speech_recognition as sr
from deleteTemp import deleteTemp
import os
#defining index of microphone to be used
sr.Microphone(device_index=1)
def convertToText(textFile,slide):
    r=sr.Recognizer()
    audio_file= textFile
    fileName = os.getcwd() + "/textFiles/slide" + str(slide) + ".txt"
    file = open(fileName,'a')     
    with sr.AudioFile(audio_file)as source:
        audio= r.record(source)
    try:
        r.pause_threshold = 2.0
        r.operation_timeout = None
        text=r.recognize_google(audio)
    except:
        print("***")
    else:
        file.write(text +" ")
        file.close()
    deleteTemp()