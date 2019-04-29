# This script deletes all the temporary files from tempFiles folder
# Written by Varun Soni, (c) 2019
import glob, os, os.path
def deleteTemp():    
    filelist = glob.glob(os.path.join(os.getcwd() + "/tempFiles/", "*.wav"))
    for f in filelist:
        os.remove(f)