# This script splits voice file for particular slide into smaller segments to improve conversion by Speech Recognition API
# and saves them in tempFiles folder
# Written by Varun Soni, (c) 2019
from pydub import AudioSegment
from AudioProject import convertToText
import os
def splitSlideVoice(fileName,slide):
    sound = AudioSegment.from_file(fileName)
    init=0
    final=15
    size=len(sound)/1000
    n=(size//15) + 1
    i=0
    if size<15:
        final=size
        reqVoice = sound[init*1000:final*1000]
        fileName=os.getcwd() + "/tempFiles/"  + str(final) + ".wav"
        reqVoice.export(fileName, format="wav")
        convertToText(fileName,slide)
    else:
        while i < n:            
            reqVoice = sound[init*1000:final*1000]
            fileName=os.getcwd() + "/tempFiles/"  + str(final) + ".wav"
            reqVoice.export(fileName, format="wav")
            convertToText(fileName,slide)
            test= size-final
            if test <15:
                init=final
                final=final + test
            else:
                print("I am here")
                init=final
                final=final+15
            i=i+1
    
                