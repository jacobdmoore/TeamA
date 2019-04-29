# This script sstarts the recording of the lecture, with options to quit gracefully.
# Written by Varun Soni, (c) 2019
import tkinter
import tkinter.messagebox
import pyaudio
import wave
import os
import signal

# Function that happens when KeyboardInterrupt occurs.
def quit_gracefully(*args):
    print('\n\nCeasing audio recording.')
    RecAUD.stop(guiAUD)
    exit(0);

# This allows CTRL + C to be communicated to Python through the shell.
signal.signal(signal.SIGINT, quit_gracefully)

class RecAUD:
    # Create a constructor to initialise object of RecAud
    def __init__(self, chunk=3024, frmat=pyaudio.paInt16, channels=2, rate=44100, py=pyaudio.PyAudio()):
        # Start Tkinter and set Title
        #self.main = tkinter.Tk()
        #self.collections = []
        #self.main.geometry('500x300')
        #self.main.title('Record')
        self.CHUNK = chunk
        self.FORMAT = frmat
        self.CHANNELS = channels
        self.RATE = rate
        self.p = py
        self.frames = []
        self.st = 1
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        # Set Frames
        #self.buttons = tkinter.Frame(self.main, padx=120, pady=20)
        # Pack Frame
        #self.buttons.pack(fill=tkinter.BOTH)
        # Start and Stop buttons
        #self.strt_rec = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text='Start Recording', command=lambda: self.start_record())
        #self.strt_rec.grid(row=0, column=0, padx=50, pady=5)
        #self.stop_rec = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text='Stop Recording', command=lambda: self.stop())
        #self.stop_rec.grid(row=1, column=0, columnspan=1, padx=50, pady=5)
        #tkinter.mainloop()
# Function to start recording 
    def start_record(self):
        self.st = 1
        self.frames = []
        stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        while self.st == 1:
            data = stream.read(self.CHUNK)
            self.frames.append(data)
            #self.main.update()
        stream.close()
        wf = wave.open(os.getcwd() + '/voiceFiles/lecture.wav', 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
#Function to stop recording 
    def stop(self):
        self.st = 0
# Create an object of the ProgramGUI class to begin the program.
guiAUD = RecAUD()

try:
    RecAUD.start_record(guiAUD)
except KeyboardInterrupt:
    quit_gracefully()


